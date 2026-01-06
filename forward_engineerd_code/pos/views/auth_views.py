"""
Authentication Views
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from functools import wraps
from pos.forms.auth_forms import LoginForm
from pos.services.employee_service import EmployeeService


def employee_login_required(view_func):
    """Decorator to check if employee is logged in via session"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'employee_id' not in request.session:
            return redirect('pos:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_view(request):
    """Login view"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            employee_service = EmployeeService()
            result = employee_service.authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            
            if result['success']:
                employee = result['employee']
                # Use Django's session framework
                request.session['employee_id'] = employee.username
                request.session['employee_name'] = employee.full_name
                request.session['employee_position'] = employee.position
                request.session['is_admin'] = result['is_admin']
                
                messages.success(request, f'Welcome, {employee.full_name}!')
                
                if result['is_admin']:
                    return redirect('pos:dashboard')
                else:
                    return redirect('pos:dashboard')
            else:
                messages.error(request, result['message'])
    else:
        form = LoginForm()
    
    return render(request, 'pos/login.html', {'form': form})


@employee_login_required
def logout_view(request):
    """Logout view"""
    if 'employee_id' in request.session:
        from pos.services.employee_service import EmployeeService
        employee_service = EmployeeService()
        from pos.repositories.employee_repository import EmployeeRepository
        employee_repo = EmployeeRepository()
        employee = employee_repo.get_by_username(request.session['employee_id'])
        if employee:
            employee_service.logout(employee)
    
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('pos:login')


@employee_login_required
def dashboard_view(request):
    """Dashboard view"""
    context = {
        'employee_name': request.session.get('employee_name', 'User'),
        'employee_position': request.session.get('employee_position', 'Cashier'),
        'is_admin': request.session.get('is_admin', False),
    }
    return render(request, 'pos/dashboard.html', context)

