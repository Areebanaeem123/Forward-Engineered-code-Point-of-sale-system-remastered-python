"""
Customer Service - Business logic for customer management
"""

from typing import List, Optional
from pos.models import Customer, Rental
from pos.repositories.customer_repository import CustomerRepository
from pos.repositories.rental_repository import RentalRepository


class CustomerService:
    """Service for customer management operations"""
    
    def __init__(self):
        self.customer_repo = CustomerRepository()
        self.rental_repo = RentalRepository()
    
    def get_or_create_customer(self, phone_number: str) -> tuple[Customer, bool]:
        """Get existing customer or create new one"""
        return self.customer_repo.get_or_create(phone_number)
    
    def customer_exists(self, phone_number: str) -> bool:
        """Check if customer exists"""
        return self.customer_repo.exists(phone_number)
    
    def get_customer(self, phone_number: str) -> Optional[Customer]:
        """Get customer by phone number"""
        return self.customer_repo.get_by_phone(phone_number)
    
    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        return self.customer_repo.get_all()
    
    def get_customers_with_outstanding_rentals(self) -> List[Customer]:
        """Get customers with outstanding rentals"""
        return self.customer_repo.get_with_outstanding_rentals()
    
    def get_customer_rentals(self, phone_number: str) -> List[Rental]:
        """Get all rentals for a customer"""
        customer = self.customer_repo.get_by_phone(phone_number)
        if not customer:
            return []
        return self.rental_repo.get_by_customer(customer)
    
    def get_customer_outstanding_rentals(self, phone_number: str) -> List[Rental]:
        """Get outstanding rentals for a customer"""
        customer = self.customer_repo.get_by_phone(phone_number)
        if not customer:
            return []
        return self.rental_repo.get_outstanding_by_customer(customer)

