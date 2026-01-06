"""
Customer Repository - Abstracts customer-related database operations
"""

from typing import List, Optional
from pos.models import Customer


class CustomerRepository:
    """Repository for Customer model operations"""
    
    @staticmethod
    def get_by_phone(phone_number: str) -> Optional[Customer]:
        """Get customer by phone number"""
        try:
            return Customer.objects.get(phone_number=phone_number)
        except Customer.DoesNotExist:
            return None
    
    @staticmethod
    def exists(phone_number: str) -> bool:
        """Check if customer exists"""
        return Customer.objects.filter(phone_number=phone_number).exists()
    
    @staticmethod
    def create(phone_number: str) -> Customer:
        """Create a new customer"""
        return Customer.objects.create(phone_number=phone_number)
    
    @staticmethod
    def get_or_create(phone_number: str) -> tuple[Customer, bool]:
        """Get existing customer or create new one"""
        return Customer.objects.get_or_create(phone_number=phone_number)
    
    @staticmethod
    def get_all() -> List[Customer]:
        """Get all customers"""
        return list(Customer.objects.all())
    
    @staticmethod
    def get_with_outstanding_rentals() -> List[Customer]:
        """Get customers with outstanding rentals"""
        return list(Customer.objects.filter(rentals__is_returned=False).distinct())

