"""
Admin Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from pos.views.auth_views import employee_login_required
from pos.forms.employee_forms import EmployeeForm
from pos.services.employee_service import EmployeeService
from pos.models import Employee


def is_admin(request):
    """Check if user is admin"""
    return request.session.get('is_admin', False)


@employee_login_required
def employee_list_view(request):
    """List all employees"""
    if not request.session.get('is_admin', False):
        messages.error(request, 'Access denied. Admin only.')
        return redirect('pos:dashboard')
    
    employee_service = EmployeeService()
    employees = employee_service.get_all_employees()
    
    context = {
        'employees': employees,
    }
    return render(request, 'pos/employee_list.html', context)


@employee_login_required
def employee_create_view(request):
    """Create new employee"""
    if not request.session.get('is_admin', False):
        messages.error(request, 'Access denied. Admin only.')
        return redirect('pos:dashboard')
    
    employee_service = EmployeeService()
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            result = employee_service.create_employee(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                position=form.cleaned_data['position'],
                password=form.cleaned_data['password']
            )
            if result['success']:
                messages.success(request, result['message'])
                return redirect('pos:employee_list')
            else:
                messages.error(request, result['message'])
    else:
        form = EmployeeForm()
    
    context = {
        'form': form,
    }
    return render(request, 'pos/employee_create.html', context)


@employee_login_required
def employee_update_view(request, username):
    """Update employee"""
    if not request.session.get('is_admin', False):
        messages.error(request, 'Access denied. Admin only.')
        return redirect('pos:dashboard')
    
    employee = get_object_or_404(Employee, username=username)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            if form.cleaned_data['password']:
                employee.set_password(form.cleaned_data['password'])
            form.save()
            messages.success(request, 'Employee updated successfully')
            return redirect('pos:employee_list')
    else:
        form = EmployeeForm(instance=employee)
    
    context = {
        'form': form,
        'employee': employee,
    }
    return render(request, 'pos/employee_update.html', context)

