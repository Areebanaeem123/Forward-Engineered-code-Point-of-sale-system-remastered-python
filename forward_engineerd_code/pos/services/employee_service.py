"""
Employee Service - Business logic for employee management and authentication
"""

from typing import List, Optional, Dict
from pos.models import Employee, EmployeeLog
from pos.repositories.employee_repository import EmployeeRepository
from pos.config import SystemConfig


class EmployeeService:
    """Service for employee management and authentication"""
    
    def __init__(self):
        self.employee_repo = EmployeeRepository()
    
    def authenticate(self, username: str, password: str) -> Dict:
        """Authenticate employee"""
        employee = self.employee_repo.authenticate(username, password)
        if not employee:
            return {
                'success': False,
                'message': 'Invalid username or password'
            }
        
        # Log login
        self.employee_repo.log_activity(employee, 'login')
        
        return {
            'success': True,
            'employee': employee,
            'position': employee.position,
            'is_admin': employee.position == 'Admin'
        }
    
    def logout(self, employee: Employee) -> bool:
        """Logout employee and log activity"""
        self.employee_repo.log_activity(employee, 'logout')
        return True
    
    def create_employee(self, username: str, first_name: str, last_name: str,
                       position: str, password: str) -> Dict:
        """Create a new employee with validation"""
        # Validation
        if position not in ['Admin', 'Cashier']:
            return {
                'success': False,
                'message': 'Invalid position. Must be Admin or Cashier'
            }
        
        if self.employee_repo.get_by_username(username):
            return {
                'success': False,
                'message': 'Username already exists'
            }
        
        employee = self.employee_repo.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            position=position,
            password=password
        )
        
        return {
            'success': True,
            'employee': employee,
            'message': 'Employee created successfully'
        }
    
    def get_employee(self, username: str) -> Optional[Employee]:
        """Get employee by username"""
        return self.employee_repo.get_by_username(username)
    
    def get_all_employees(self) -> List[Employee]:
        """Get all employees"""
        return self.employee_repo.get_all()
    
    def get_employees_by_position(self, position: str) -> List[Employee]:
        """Get employees by position"""
        return self.employee_repo.get_by_position(position)
    
    def get_activity_logs(self, employee: Employee = None) -> List[EmployeeLog]:
        """Get activity logs"""
        return self.employee_repo.get_activity_logs(employee)
    
    def is_admin(self, employee: Employee) -> bool:
        """Check if employee is admin"""
        return employee.position == 'Admin'
    
    def is_cashier(self, employee: Employee) -> bool:
        """Check if employee is cashier"""
        return employee.position == 'Cashier'

