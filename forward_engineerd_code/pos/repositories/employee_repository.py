"""
Employee Repository - Abstracts employee-related database operations
"""

from typing import List, Optional
from pos.models import Employee, EmployeeLog
from datetime import datetime


class EmployeeRepository:
    """Repository for Employee model operations"""
    
    @staticmethod
    def get_by_username(username: str) -> Optional[Employee]:
        """Get employee by username"""
        try:
            return Employee.objects.get(username=username)
        except Employee.DoesNotExist:
            return None
    
    @staticmethod
    def authenticate(username: str, password: str) -> Optional[Employee]:
        """Authenticate employee"""
        try:
            employee = Employee.objects.get(username=username)
            if employee.check_password(password):
                return employee
        except Employee.DoesNotExist:
            pass
        return None
    
    @staticmethod
    def create(username: str, first_name: str, last_name: str, 
               position: str, password: str) -> Employee:
        """Create a new employee"""
        employee = Employee.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            position=position,
            password=password
        )
        employee.is_staff = (position == 'Admin')
        employee.save()
        return employee
    
    @staticmethod
    def log_activity(employee: Employee, action: str) -> EmployeeLog:
        """Log employee activity"""
        return EmployeeLog.objects.create(
            employee=employee,
            action=action,
            timestamp=datetime.now()
        )
    
    @staticmethod
    def get_all() -> List[Employee]:
        """Get all employees"""
        return list(Employee.objects.all())
    
    @staticmethod
    def get_by_position(position: str) -> List[Employee]:
        """Get employees by position"""
        return list(Employee.objects.filter(position=position))
    
    @staticmethod
    def get_activity_logs(employee: Employee = None) -> List[EmployeeLog]:
        """Get activity logs"""
        if employee:
            return list(EmployeeLog.objects.filter(employee=employee))
        return list(EmployeeLog.objects.all())

