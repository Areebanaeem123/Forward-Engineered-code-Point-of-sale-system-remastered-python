"""
Rental Views
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from pos.views.auth_views import employee_login_required
from pos.forms.rental_forms import RentalForm, ReturnForm
from pos.services.rental_service import RentalService
from pos.services.inventory_service import InventoryService
from pos.repositories.employee_repository import EmployeeRepository


@employee_login_required
def rental_create_view(request):
    """Create new rental"""
    rental_service = RentalService()
    inventory_service = InventoryService()
    employee_repo = EmployeeRepository()
    
    employee = employee_repo.get_by_username(request.session.get('employee_id'))
    
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            result = rental_service.create_rental(
                phone_number=form.cleaned_data['phone_number'],
                item_id=form.cleaned_data['item_id'],
                quantity=form.cleaned_data['quantity'],
                employee=employee
            )
            if result['success']:
                messages.success(request, result['message'])
                return redirect('pos:rental_list')
            else:
                messages.error(request, result['message'])
    else:
        form = RentalForm()
    
    available_items = inventory_service.get_available_for_rental()
    context = {
        'form': form,
        'available_items': available_items,
    }
    return render(request, 'pos/rental_create.html', context)


@employee_login_required
def rental_return_view(request):
    """Process rental return"""
    rental_service = RentalService()
    employee_repo = EmployeeRepository()
    
    employee = employee_repo.get_by_username(request.session.get('employee_id'))
    
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            # Get outstanding rentals for customer
            outstanding = rental_service.get_outstanding_rentals(
                form.cleaned_data['phone_number']
            )
            
            if not outstanding:
                messages.error(request, 'No outstanding rentals found for this customer')
                return redirect('pos:rental_return')
            
            # Find rental by ID
            rental_id = form.cleaned_data.get('rental_id')
            if rental_id:
                result = rental_service.process_return(rental_id, employee)
                if result['success']:
                    messages.success(
                        request,
                        f"Return processed! Late fee: ${result['late_fee']}"
                    )
                    return redirect('pos:rental_list')
                else:
                    messages.error(request, result['message'])
            else:
                messages.error(request, 'Please select a rental to return')
        else:
            # Show outstanding rentals for phone number
            phone_number = request.POST.get('phone_number')
            if phone_number:
                outstanding = rental_service.get_outstanding_rentals(phone_number)
                context = {
                    'form': form,
                    'outstanding_rentals': outstanding,
                    'phone_number': phone_number,
                }
                return render(request, 'pos/rental_return.html', context)
    else:
        form = ReturnForm()
    
    context = {
        'form': form,
    }
    return render(request, 'pos/rental_return.html', context)


@employee_login_required
def rental_list_view(request):
    """List all rentals"""
    rental_service = RentalService()
    rentals = rental_service.get_all_outstanding_rentals()
    
    context = {
        'rentals': rentals,
    }
    return render(request, 'pos/rental_list.html', context)

