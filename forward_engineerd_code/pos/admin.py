"""
Django Admin Configuration for POS System
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from pos.models import (
    Employee, Item, Customer, Rental, Sale, SaleItem,
    ReturnTransaction, ReturnItem, Coupon, EmployeeLog
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Admin interface for Employee model"""
    list_display = ['username', 'first_name', 'last_name', 'position', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['position', 'is_staff', 'is_active']
    search_fields = ['username', 'first_name', 'last_name']
    ordering = ['username']
    
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('POS Information', {'fields': ('position',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
    )
    
    def save_model(self, request, obj, form, change):
        """Override to handle password hashing"""
        if 'password' in form.changed_data and form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])
        elif not change:  # New user
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Admin interface for Item model"""
    list_display = ['item_id', 'name', 'price', 'stock_sale', 'stock_rental', 'item_type']
    list_filter = ['item_type']
    search_fields = ['name', 'item_id']
    ordering = ['item_id']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin interface for Customer model"""
    list_display = ['phone_number', 'created_at']
    search_fields = ['phone_number']
    ordering = ['phone_number']


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    """Admin interface for Rental model"""
    list_display = ['id', 'customer', 'item', 'quantity', 'rental_date', 'due_date', 'is_returned']
    list_filter = ['is_returned', 'rental_date']
    search_fields = ['customer__phone_number', 'item__name']
    ordering = ['-rental_date']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """Admin interface for Sale model"""
    list_display = ['id', 'transaction_time', 'total_amount', 'employee']
    list_filter = ['transaction_time']
    search_fields = ['employee__username']
    ordering = ['-transaction_time']


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    """Admin interface for SaleItem model"""
    list_display = ['id', 'sale', 'item', 'quantity', 'subtotal']
    list_filter = ['sale__transaction_time']
    search_fields = ['item__name']


@admin.register(ReturnTransaction)
class ReturnTransactionAdmin(admin.ModelAdmin):
    """Admin interface for ReturnTransaction model"""
    list_display = ['id', 'transaction_time', 'total_refund', 'late_fee_total']
    list_filter = ['transaction_time']
    ordering = ['-transaction_time']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Admin interface for Coupon model"""
    list_display = ['code', 'discount_percentage', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['code']


@admin.register(EmployeeLog)
class EmployeeLogAdmin(admin.ModelAdmin):
    """Admin interface for EmployeeLog model"""
    list_display = ['id', 'employee', 'action', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['employee__username']
    ordering = ['-timestamp']
