"""
Item Repository - Abstracts item-related database operations
"""

from typing import List, Optional
from django.db.models import Q
from pos.models import Item


class ItemRepository:
    """Repository for Item model operations"""
    
    @staticmethod
    def get_by_id(item_id: int) -> Optional[Item]:
        """Get item by item_id"""
        try:
            return Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return None
    
    @staticmethod
    def get_all() -> List[Item]:
        """Get all items"""
        return list(Item.objects.all())
    
    @staticmethod
    def get_available_for_sale() -> List[Item]:
        """Get items available for sale"""
        return list(Item.objects.filter(
            Q(item_type='Sale') | Q(item_type='Both'),
            stock_sale__gt=0
        ))
    
    @staticmethod
    def get_available_for_rental() -> List[Item]:
        """Get items available for rental"""
        return list(Item.objects.filter(
            Q(item_type='Rental') | Q(item_type='Both'),
            stock_rental__gt=0
        ))
    
    @staticmethod
    def search_by_name(name: str) -> List[Item]:
        """Search items by name"""
        return list(Item.objects.filter(name__icontains=name))
    
    @staticmethod
    def create(item_id: int, name: str, price: float, stock_sale: int = 0, 
               stock_rental: int = 0, item_type: str = 'Both') -> Item:
        """Create a new item"""
        return Item.objects.create(
            item_id=item_id,
            name=name,
            price=price,
            stock_sale=stock_sale,
            stock_rental=stock_rental,
            item_type=item_type
        )
    
    @staticmethod
    def update_stock_sale(item_id: int, quantity: int, decrease: bool = True) -> bool:
        """Update sale stock"""
        try:
            item = Item.objects.get(item_id=item_id)
            if decrease:
                item.stock_sale = max(0, item.stock_sale - quantity)
            else:
                item.stock_sale += quantity
            item.save()
            return True
        except Item.DoesNotExist:
            return False
    
    @staticmethod
    def update_stock_rental(item_id: int, quantity: int, decrease: bool = True) -> bool:
        """Update rental stock"""
        try:
            item = Item.objects.get(item_id=item_id)
            if decrease:
                item.stock_rental = max(0, item.stock_rental - quantity)
            else:
                item.stock_rental += quantity
            item.save()
            return True
        except Item.DoesNotExist:
            return False
    
    @staticmethod
    def delete(item_id: int) -> bool:
        """Delete an item"""
        try:
            item = Item.objects.get(item_id=item_id)
            item.delete()
            return True
        except Item.DoesNotExist:
            return False

