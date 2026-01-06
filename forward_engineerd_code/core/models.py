from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Employee(models.Model):
    """Employee model with authentication fields"""
    POSITION_CHOICES = [
        ('Admin', 'Admin'),
        ('Cashier', 'Cashier'),
    ]
    
    username = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    password_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'employees'
        indexes = [
            models.Index(fields=['position'], name='idx_employees_position'),
        ]
    
    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"


class Item(models.Model):
    """Item model with dual stock tracking for sales and rentals"""
    ITEM_TYPE_CHOICES = [
        ('Sale', 'Sale'),
        ('Rental', 'Rental'),
        ('Both', 'Both'),
    ]
    
    item_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock_sale = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    stock_rental = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'items'
        indexes = [
            models.Index(fields=['item_id'], name='idx_items_item_id'),
            models.Index(fields=['name'], name='idx_items_name'),
        ]
    
    def __str__(self):
        return f"{self.item_id} - {self.name}"


class Customer(models.Model):
    """Customer model with phone number as unique identifier"""
    phone_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customers'
        indexes = [
            models.Index(fields=['phone_number'], name='idx_customers_phone'),
        ]
    
    def __str__(self):
        return self.phone_number


class Sale(models.Model):
    """Sale transaction model"""
    transaction_time = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        db_column='employee_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sales'
        indexes = [
            models.Index(fields=['transaction_time'], name='idx_sales_transaction_time'),
            models.Index(fields=['employee'], name='idx_sales_employee'),
        ]
    
    def __str__(self):
        return f"Sale {self.id} - ${self.total_amount}"


class SaleItem(models.Model):
    """Individual items in a sale transaction"""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'sale_items'
        unique_together = [['sale', 'item']]
    
    def __str__(self):
        return f"Sale {self.sale_id} - {self.item.name} x{self.quantity}"


class Rental(models.Model):
    """Rental transaction model"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    rental_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rentals'
        indexes = [
            models.Index(fields=['customer', 'is_returned'], name='idx_rentals_customer_returned'),
            models.Index(fields=['due_date'], name='idx_rentals_due_date'),
            models.Index(fields=['item'], name='idx_rentals_item'),
        ]
    
    def __str__(self):
        return f"Rental {self.id} - {self.customer.phone_number} - {self.item.name}"


class Coupon(models.Model):
    """Coupon model for discount codes"""
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'coupons'
        indexes = [
            models.Index(fields=['code'], name='idx_coupons_code'),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"


class EmployeeLog(models.Model):
    """Employee activity log for login/logout events"""
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        db_column='employee_id'
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'employee_logs'
        indexes = [
            models.Index(fields=['employee', 'timestamp'], name='idx_employee_logs_employee_timestamp'),
            models.Index(fields=['action'], name='idx_employee_logs_action'),
        ]
    
    def __str__(self):
        return f"{self.employee.username} - {self.action} at {self.timestamp}"


class ReturnTransaction(models.Model):
    """Return transaction model for processing rental returns"""
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True
    )
    trans_time = models.DateTimeField()
    total_refund = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    late_fee_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'return_transactions'
    
    def __str__(self):
        return f"Return {self.id} - ${self.late_fee_total}"


class ReturnItem(models.Model):
    """Individual items in a return transaction"""
    return_transaction = models.ForeignKey(
        ReturnTransaction,
        on_delete=models.CASCADE,
        related_name='items'
    )
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    days_late = models.IntegerField(default=0)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        db_table = 'return_items'
    
    def __str__(self):
        return f"Return {self.return_transaction_id} - {self.item.name} x{self.quantity}"
