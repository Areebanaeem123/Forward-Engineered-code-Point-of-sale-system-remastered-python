"""
Rental Service - Business logic for rental management
"""

from typing import List, Optional, Dict
from datetime import date, timedelta
from decimal import Decimal
from pos.models import Rental, Customer, Item, ReturnTransaction, ReturnItem
from pos.repositories.rental_repository import RentalRepository
from pos.repositories.customer_repository import CustomerRepository
from pos.repositories.item_repository import ItemRepository
from pos.repositories.employee_repository import EmployeeRepository
from pos.config import SystemConfig


class RentalService:
    """Service for rental transaction operations"""
    
    def __init__(self):
        self.rental_repo = RentalRepository()
        self.customer_repo = CustomerRepository()
        self.item_repo = ItemRepository()
        self.employee_repo = EmployeeRepository()
    
    def create_rental(self, phone_number: str, item_id: int, 
                     quantity: int, employee=None) -> Dict:
        """Create a new rental with validation"""
        # Get or create customer
        customer, created = self.customer_repo.get_or_create(phone_number)
        
        # Get item
        item = self.item_repo.get_by_id(item_id)
        if not item:
            return {'success': False, 'message': 'Item not found'}
        
        # Check availability
        if not item.is_available_for_rental(quantity):
            return {
                'success': False,
                'message': f'Insufficient rental stock. Available: {item.stock_rental}'
            }
        
        # Create rental
        rental = self.rental_repo.create(customer, item, quantity)
        
        # Update inventory
        self.item_repo.update_stock_rental(item_id, quantity, decrease=True)
        
        # Log activity
        if employee:
            self.employee_repo.log_activity(employee, 'rental_created')
        
        return {
            'success': True,
            'rental': rental,
            'message': 'Rental created successfully'
        }
    
    def get_outstanding_rentals(self, phone_number: str) -> List[Rental]:
        """Get outstanding rentals for a customer"""
        customer = self.customer_repo.get_by_phone(phone_number)
        if not customer:
            return []
        return self.rental_repo.get_outstanding_by_customer(customer)
    
    def process_return(self, rental_id: int, employee=None) -> Dict:
        """Process rental return with late fee calculation"""
        rental = self.rental_repo.get_by_id(rental_id)
        if not rental:
            return {'success': False, 'message': 'Rental not found'}
        
        if rental.is_returned:
            return {'success': False, 'message': 'Rental already returned'}
        
        # Calculate late fee
        days_late = rental.calculate_days_late()
        late_fee = rental.calculate_late_fee()
        
        # Mark as returned
        self.rental_repo.return_rental(rental)
        
        # Create return transaction
        return_transaction = ReturnTransaction.objects.create(
            transaction_time=date.today(),
            total_refund=Decimal('0.00'),  # No refund for rentals
            late_fee_total=late_fee,
            employee=employee
        )
        
        # Create return item
        ReturnItem.objects.create(
            return_transaction=return_transaction,
            rental=rental,
            item=rental.item,
            quantity=rental.quantity,
            days_late=days_late,
            late_fee=late_fee
        )
        
        # Log activity
        if employee:
            self.employee_repo.log_activity(employee, 'rental_returned')
        
        return {
            'success': True,
            'rental': rental,
            'return_transaction': return_transaction,
            'late_fee': late_fee,
            'days_late': days_late,
            'message': 'Return processed successfully'
        }
    
    def get_overdue_rentals(self) -> List[Rental]:
        """Get all overdue rentals"""
        return self.rental_repo.get_overdue()
    
    def get_all_outstanding_rentals(self) -> List[Rental]:
        """Get all outstanding rentals"""
        return self.rental_repo.get_all_outstanding()
    
    def get_rental(self, rental_id: int) -> Optional[Rental]:
        """Get rental by ID"""
        return self.rental_repo.get_by_id(rental_id)

