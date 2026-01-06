"""
Custom Authentication Backend for Employee Model
"""

from pos.models import Employee


class EmployeeBackend:
    """
    Custom authentication backend for Employee model
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            employee = Employee.objects.get(username=username)
            if employee.check_password(password) and employee.is_active:
                return employee
        except Employee.DoesNotExist:
            return None
        return None
    
    def get_user(self, user_id):
        try:
            return Employee.objects.get(pk=user_id)
        except Employee.DoesNotExist:
            return None

