"""
Rental Repository - Abstracts rental-related database operations
"""

from typing import List, Optional
from datetime import date, timedelta
from decimal import Decimal
from pos.models import Rental, Customer, Item, Employee
from pos.config import SystemConfig


class RentalRepository:
    """Repository for Rental model operations"""
    
    @staticmethod
    def get_by_id(rental_id: int) -> Optional[Rental]:
        """Get rental by ID"""
        try:
            return Rental.objects.get(id=rental_id)
        except Rental.DoesNotExist:
            return None
    
    @staticmethod
    def create(customer: Customer, item: Item, quantity: int, 
               rental_date: date = None) -> Rental:
        """Create a new rental"""
        if rental_date is None:
            rental_date = date.today()
        
        due_date = rental_date + timedelta(days=SystemConfig.get_rental_period_days())
        
        return Rental.objects.create(
            customer=customer,
            item=item,
            quantity=quantity,
            rental_date=rental_date,
            due_date=due_date
        )
    
    @staticmethod
    def get_outstanding_by_customer(customer: Customer) -> List[Rental]:
        """Get outstanding rentals for a customer"""
        return list(Rental.objects.filter(
            customer=customer,
            is_returned=False
        ))
    
    @staticmethod
    def get_all_outstanding() -> List[Rental]:
        """Get all outstanding rentals"""
        return list(Rental.objects.filter(is_returned=False))
    
    @staticmethod
    def get_overdue() -> List[Rental]:
        """Get all overdue rentals"""
        return list(Rental.objects.filter(
            is_returned=False,
            due_date__lt=date.today()
        ))
    
    @staticmethod
    def return_rental(rental: Rental, return_date: date = None) -> Rental:
        """Mark rental as returned"""
        if return_date is None:
            return_date = date.today()
        
        rental.is_returned = True
        rental.return_date = return_date
        rental.late_fee = rental.calculate_late_fee()
        rental.save()
        
        # Update inventory
        from pos.repositories.item_repository import ItemRepository
        ItemRepository.update_stock_rental(
            rental.item.item_id,
            rental.quantity,
            decrease=False
        )
        
        return rental
    
    @staticmethod
    def calculate_late_fees(rental: Rental) -> Decimal:
        """Calculate late fees for a rental"""
        return rental.calculate_late_fee()
    
    @staticmethod
    def get_all() -> List[Rental]:
        """Get all rentals"""
        return list(Rental.objects.all())
    
    @staticmethod
    def get_by_customer(customer: Customer) -> List[Rental]:
        """Get all rentals for a customer"""
        return list(Rental.objects.filter(customer=customer))

