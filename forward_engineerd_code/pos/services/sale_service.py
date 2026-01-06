"""
Sale Service - Business logic for sales processing
"""

from typing import List, Optional, Dict
from decimal import Decimal
from datetime import datetime
from pos.models import Sale, SaleItem, Item, Employee, Coupon
from pos.repositories.sale_repository import SaleRepository
from pos.repositories.item_repository import ItemRepository
from pos.repositories.employee_repository import EmployeeRepository
from pos.config import SystemConfig


class SaleService:
    """Service for sale transaction operations"""
    
    def __init__(self):
        self.sale_repo = SaleRepository()
        self.item_repo = ItemRepository()
        self.employee_repo = EmployeeRepository()
    
    def create_sale(self, employee: Employee = None, coupon_code: str = None) -> Sale:
        """Create a new sale transaction"""
        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            except Coupon.DoesNotExist:
                pass  # Invalid coupon, continue without it
        
        return self.sale_repo.create(employee=employee, coupon=coupon)
    
    def add_item_to_sale(self, sale: Sale, item_id: int, quantity: int) -> Dict:
        """Add item to sale with validation"""
        item = self.item_repo.get_by_id(item_id)
        if not item:
            return {'success': False, 'message': 'Item not found'}
        
        if not item.is_available_for_sale(quantity):
            return {
                'success': False, 
                'message': f'Insufficient stock. Available: {item.stock_sale}'
            }
        
        sale_item = self.sale_repo.add_item(sale, item, quantity)
        self.sale_repo.calculate_total(sale, SystemConfig.get_tax_rate())
        
        return {
            'success': True,
            'sale_item': sale_item,
            'sale': sale
        }
    
    def remove_item_from_sale(self, sale: Sale, item_id: int) -> bool:
        """Remove item from sale"""
        item = self.item_repo.get_by_id(item_id)
        if not item:
            return False
        
        success = self.sale_repo.remove_item(sale, item)
        if success:
            self.sale_repo.calculate_total(sale, SystemConfig.get_tax_rate())
        return success
    
    def apply_coupon(self, sale: Sale, coupon_code: str) -> Dict:
        """Apply coupon to sale"""
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            sale.coupon = coupon
            sale.save()
            self.sale_repo.calculate_total(sale, SystemConfig.get_tax_rate())
            return {'success': True, 'message': 'Coupon applied successfully'}
        except Coupon.DoesNotExist:
            return {'success': False, 'message': 'Invalid coupon code'}
    
    def finalize_sale(self, sale: Sale) -> Dict:
        """Finalize sale and update inventory"""
        if sale.items.count() == 0:
            return {'success': False, 'message': 'Cannot finalize empty sale'}
        
        # Check all items are still available
        for sale_item in sale.items.all():
            if not sale_item.item.is_available_for_sale(sale_item.quantity):
                return {
                    'success': False,
                    'message': f'Item {sale_item.item.name} is no longer available'
                }
        
        # Update inventory
        success = self.sale_repo.finalize(sale)
        if success:
            # Log activity if employee exists
            if sale.employee:
                self.employee_repo.log_activity(sale.employee, 'sale_completed')
            
            return {
                'success': True,
                'sale': sale,
                'message': 'Sale completed successfully'
            }
        
        return {'success': False, 'message': 'Failed to finalize sale'}
    
    def get_sale(self, sale_id: int) -> Optional[Sale]:
        """Get sale by ID"""
        return self.sale_repo.get_by_id(sale_id)
    
    def get_sales_by_employee(self, employee: Employee) -> List[Sale]:
        """Get sales by employee"""
        return self.sale_repo.get_by_employee(employee)
    
    def get_sales_by_date_range(self, start_date: datetime, 
                                end_date: datetime) -> List[Sale]:
        """Get sales within date range"""
        return self.sale_repo.get_by_date_range(start_date, end_date)
    
    def calculate_total(self, sale: Sale) -> Sale:
        """Recalculate sale total"""
        return self.sale_repo.calculate_total(sale, SystemConfig.get_tax_rate())

