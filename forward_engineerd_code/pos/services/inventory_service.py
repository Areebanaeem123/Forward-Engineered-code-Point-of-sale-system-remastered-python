"""
Inventory Service - Business logic for inventory management
"""

from typing import List, Optional, Dict
from decimal import Decimal
from pos.models import Item
from pos.repositories.item_repository import ItemRepository
from pos.config import SystemConfig


class InventoryService:
    """Service for inventory management operations"""
    
    def __init__(self):
        self.item_repo = ItemRepository()
    
    def get_item(self, item_id: int) -> Optional[Item]:
        """Get item by ID"""
        return self.item_repo.get_by_id(item_id)
    
    def get_all_items(self) -> List[Item]:
        """Get all items"""
        return self.item_repo.get_all()
    
    def search_items(self, query: str) -> List[Item]:
        """Search items by name"""
        return self.item_repo.search_by_name(query)
    
    def get_available_for_sale(self) -> List[Item]:
        """Get items available for sale"""
        return self.item_repo.get_available_for_sale()
    
    def get_available_for_rental(self) -> List[Item]:
        """Get items available for rental"""
        return self.item_repo.get_available_for_rental()
    
    def create_item(self, item_id: int, name: str, price: float, 
                   stock_sale: int = 0, stock_rental: int = 0, 
                   item_type: str = 'Both') -> Item:
        """Create a new item with validation"""
        # Validation
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        if stock_sale < 0 or stock_rental < 0:
            raise ValueError("Stock cannot be negative")
        if item_type not in ['Sale', 'Rental', 'Both']:
            raise ValueError("Invalid item type")
        
        # Check if item_id already exists
        if self.item_repo.get_by_id(item_id):
            raise ValueError(f"Item with ID {item_id} already exists")
        
        return self.item_repo.create(
            item_id=item_id,
            name=name,
            price=price,
            stock_sale=stock_sale,
            stock_rental=stock_rental,
            item_type=item_type
        )
    
    def update_item_stock(self, item_id: int, stock_type: str, 
                         quantity: int, decrease: bool = True) -> bool:
        """Update item stock (sale or rental)"""
        item = self.item_repo.get_by_id(item_id)
        if not item:
            return False
        
        if stock_type == 'sale':
            if decrease and not item.is_available_for_sale(quantity):
                return False
            return self.item_repo.update_stock_sale(item_id, quantity, decrease)
        elif stock_type == 'rental':
            if decrease and not item.is_available_for_rental(quantity):
                return False
            return self.item_repo.update_stock_rental(item_id, quantity, decrease)
        
        return False
    
    def check_stock_availability(self, item_id: int, quantity: int, 
                                transaction_type: str) -> bool:
        """Check if item is available in required quantity"""
        item = self.item_repo.get_by_id(item_id)
        if not item:
            return False
        
        if transaction_type == 'sale':
            return item.is_available_for_sale(quantity)
        elif transaction_type == 'rental':
            return item.is_available_for_rental(quantity)
        
        return False
    
    def get_low_stock_items(self, threshold: int = 10) -> List[Item]:
        """Get items with low stock"""
        items = self.item_repo.get_all()
        return [item for item in items 
                if item.stock_sale < threshold or item.stock_rental < threshold]
    
    def delete_item(self, item_id: int) -> bool:
        """Delete an item"""
        return self.item_repo.delete(item_id)

