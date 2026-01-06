"""
Django Models for Point-of-Sale System
Migrated from .txt file-based storage to relational database
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator
from decimal import Decimal
from datetime import date, timedelta


class EmployeeManager(BaseUserManager):
    """Custom manager for Employee model"""
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('position', 'Admin')
        return self.create_user(username, password, **extra_fields)


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
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_perm(self, perm, obj=None):
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return self.is_staff


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
    
    def is_available_for_sale(self, quantity=1):
        """Check if item is available for sale"""
        return self.stock_sale >= quantity and self.item_type in ['Sale', 'Both']
    
    def is_available_for_rental(self, quantity=1):
        """Check if item is available for rental"""
        return self.stock_rental >= quantity and self.item_type in ['Rental', 'Both']


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
    
    def get_outstanding_rentals(self):
        """Get all outstanding (not returned) rentals for this customer"""
        return self.rentals.filter(is_returned=False)


class Rental(models.Model):
    """
    Rental model - normalized from userDatabase.txt
    Represents a single rental transaction
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='rentals')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='rentals')
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    rental_date = models.DateField(default=date.today)
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
    
    def calculate_days_late(self):
        """Calculate days late if overdue"""
        if self.is_returned or date.today() <= self.due_date:
            return 0
        return (date.today() - self.due_date).days
    
    def calculate_late_fee(self, late_fee_rate=0.1):
        """Calculate late fee based on days late"""
        days_late = self.calculate_days_late()
        if days_late > 0:
            return Decimal(str(self.item.price * self.quantity * late_fee_rate * days_late))
        return Decimal('0.00')


class Sale(models.Model):
    """
    Sale model - migrated from saleInvoiceRecord.txt
    Represents a completed sale transaction
    """
    transaction_time = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
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
    transaction_time = models.DateTimeField(auto_now_add=True)
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
    
    def get_discount_rate(self):
        """Get discount rate as decimal (e.g., 0.90 for 10% off)"""
        return Decimal('1.00') - (self.discount_percentage / Decimal('100'))


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
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'employee_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['employee', 'timestamp'], name='idx_emp_logs_emp_ts'),
            models.Index(fields=['action'], name='idx_emp_logs_action'),
        ]
    
    def __str__(self):
        return f"{self.employee.username} - {self.action} at {self.timestamp}"
