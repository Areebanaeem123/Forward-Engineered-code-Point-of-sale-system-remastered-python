"""
Django Models for Point-of-Sale System
Migrated from .txt file-based storage to relational database
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator
from decimal import Decimal


class EmployeeManager(BaseUserManager):
    """Custom manager for Employee model"""
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Employee(AbstractBaseUser):
    """
    Employee model - migrated from employeeDatabase.txt
    Format: username position firstName lastName password
    """
    username = models.CharField(max_length=50, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=20, choices=[
        ('Admin', 'Admin'),
        ('Cashier', 'Cashier')
    ])
    password_hash = models.CharField(max_length=128)  # Django's password hashing
    
    # Django authentication fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = EmployeeManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'position']
    
    class Meta:
        db_table = 'employees'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Item(models.Model):
    """
    Item model - migrated from itemDatabase.txt and rentalDatabase.txt
    Format: itemID itemName price amount
    """
    ITEM_TYPE_CHOICES = [
        ('Sale', 'Sale'),
        ('Rental', 'Rental'),
        ('Both', 'Both')
    ]
    
    item_id = models.IntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, 
                                validators=[MinValueValidator(Decimal('0.01'))])
    stock_sale = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    stock_rental = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES, default='Both')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'items'
        ordering = ['item_id']
        indexes = [
            models.Index(fields=['item_id']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.name} (ID: {self.item_id})"


class Customer(models.Model):
    """
    Customer model - migrated from userDatabase.txt
    Format: phoneNumber itemID1,returnDate1,returned1 itemID2,returnDate2,returned2...
    """
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customers'
        ordering = ['phone_number']
        indexes = [
            models.Index(fields=['phone_number']),
        ]
    
    def __str__(self):
        return f"Customer: {self.phone_number}"


class Rental(models.Model):
    """
    Rental model - normalized from userDatabase.txt
    Represents a single rental transaction
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='rentals')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='rentals')
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    rental_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rentals'
        ordering = ['-rental_date']
        indexes = [
            models.Index(fields=['customer', 'is_returned']),
            models.Index(fields=['due_date']),
            models.Index(fields=['item']),
        ]
    
    def __str__(self):
        status = "Returned" if self.is_returned else "Active"
        return f"Rental #{self.id}: {self.item.name} - {status}"


class Sale(models.Model):
    """
    Sale model - migrated from saleInvoiceRecord.txt
    Represents a completed sale transaction
    """
    transaction_time = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sales'
        ordering = ['-transaction_time']
        indexes = [
            models.Index(fields=['transaction_time']),
            models.Index(fields=['employee']),
        ]
    
    def __str__(self):
        return f"Sale #{self.id} - ${self.total_amount}"


class SaleItem(models.Model):
    """
    SaleItem model - junction table for Sales and Items
    Represents items in a sale transaction
    """
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'sale_items'
        unique_together = [['sale', 'item']]
    
    def __str__(self):
        return f"{self.item.name} x{self.quantity} in Sale #{self.sale.id}"


class ReturnTransaction(models.Model):
    """
    ReturnTransaction model - migrated from returnSale.txt
    Represents a return transaction
    """
    transaction_time = models.DateTimeField()
    total_refund = models.DecimalField(max_digits=10, decimal_places=2)
    late_fee_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'return_transactions'
        ordering = ['-transaction_time']
    
    def __str__(self):
        return f"Return #{self.id} - ${self.total_refund}"


class ReturnItem(models.Model):
    """
    ReturnItem model - junction table for ReturnTransactions and Items
    """
    return_transaction = models.ForeignKey(ReturnTransaction, on_delete=models.CASCADE, 
                                          related_name='items')
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    days_late = models.IntegerField(default=0)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        db_table = 'return_items'
    
    def __str__(self):
        return f"Return Item: {self.item.name}"


class Coupon(models.Model):
    """
    Coupon model - migrated from couponNumber.txt
    Format: one coupon code per line
    """
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'coupons'
        indexes = [
            models.Index(fields=['code']),
        ]
    
    def __str__(self):
        return f"Coupon: {self.code}"


class EmployeeLog(models.Model):
    """
    EmployeeLog model - migrated from employeeLogfile.txt
    Format: name (username position) logs into POS System. Time: yyyy-MM-dd HH:mm:ss.SSS
    """
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'employee_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['employee', 'timestamp']),
            models.Index(fields=['action']),
        ]
    
    def __str__(self):
        return f"{self.employee.username} - {self.action} at {self.timestamp}"

