"""
Sale Repository - Abstracts sale-related database operations
"""

from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from pos.models import Sale, SaleItem, Item, Employee


class SaleRepository:
    """Repository for Sale model operations"""
    
    @staticmethod
    def get_by_id(sale_id: int) -> Optional[Sale]:
        """Get sale by ID"""
        try:
            return Sale.objects.get(id=sale_id)
        except Sale.DoesNotExist:
            return None
    
    @staticmethod
    def create(employee: Employee = None, coupon=None) -> Sale:
        """Create a new sale"""
        return Sale.objects.create(
            transaction_time=datetime.now(),
            total_amount=Decimal('0.00'),
            subtotal=Decimal('0.00'),
            tax_amount=Decimal('0.00'),
            discount_amount=Decimal('0.00'),
            employee=employee,
            coupon=coupon
        )
    
    @staticmethod
    def add_item(sale: Sale, item: Item, quantity: int) -> SaleItem:
        """Add item to sale"""
        unit_price = item.price
        subtotal = unit_price * quantity
        
        sale_item, created = SaleItem.objects.get_or_create(
            sale=sale,
            item=item,
            defaults={
                'quantity': quantity,
                'unit_price': unit_price,
                'subtotal': subtotal
            }
        )
        
        if not created:
            sale_item.quantity += quantity
            sale_item.subtotal = sale_item.unit_price * sale_item.quantity
            sale_item.save()
        
        return sale_item
    
    @staticmethod
    def remove_item(sale: Sale, item: Item) -> bool:
        """Remove item from sale"""
        try:
            sale_item = SaleItem.objects.get(sale=sale, item=item)
            sale_item.delete()
            return True
        except SaleItem.DoesNotExist:
            return False
    
    @staticmethod
    def calculate_total(sale: Sale, tax_rate: float = 1.06, discount_rate: float = 1.0) -> Sale:
        """Calculate and update sale total"""
        subtotal = sum(item.subtotal for item in sale.items.all())
        
        # Apply discount if coupon exists
        if sale.coupon and sale.coupon.is_active:
            discount_rate = sale.coupon.get_discount_rate()
        
        discount_amount = subtotal * (1 - discount_rate)
        discounted_subtotal = subtotal - discount_amount
        tax_amount = discounted_subtotal * (tax_rate - 1)
        total_amount = discounted_subtotal + tax_amount
        
        sale.subtotal = subtotal
        sale.discount_amount = discount_amount
        sale.tax_amount = tax_amount
        sale.total_amount = total_amount
        sale.save()
        
        return sale
    
    @staticmethod
    def finalize(sale: Sale) -> bool:
        """Finalize sale and update inventory"""
        from pos.repositories.item_repository import ItemRepository
        
        try:
            # Update inventory for each item
            for sale_item in sale.items.all():
                ItemRepository.update_stock_sale(
                    sale_item.item.item_id,
                    sale_item.quantity,
                    decrease=True
                )
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_all() -> List[Sale]:
        """Get all sales"""
        return list(Sale.objects.all())
    
    @staticmethod
    def get_by_employee(employee: Employee) -> List[Sale]:
        """Get sales by employee"""
        return list(Sale.objects.filter(employee=employee))
    
    @staticmethod
    def get_by_date_range(start_date: datetime, end_date: datetime) -> List[Sale]:
        """Get sales within date range"""
        return list(Sale.objects.filter(
            transaction_time__gte=start_date,
            transaction_time__lte=end_date
        ))

