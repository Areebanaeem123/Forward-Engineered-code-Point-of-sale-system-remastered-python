"""
Sale Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from pos.views.auth_views import employee_login_required
from django.http import JsonResponse
from pos.forms.sale_forms import SaleItemForm, CouponForm
from pos.services.sale_service import SaleService
from pos.services.inventory_service import InventoryService
from pos.repositories.employee_repository import EmployeeRepository
from pos.models import Sale


@employee_login_required
def sale_create_view(request):
    """Create new sale"""
    sale_service = SaleService()
    inventory_service = InventoryService()
    employee_repo = EmployeeRepository()
    
    # Get current employee
    employee = employee_repo.get_by_username(request.session.get('employee_id'))
    
    # Get or create current sale from session
    sale_id = request.session.get('current_sale_id')
    if sale_id:
        sale = sale_service.get_sale(sale_id)
        if not sale:
            sale = sale_service.create_sale(employee=employee)
            request.session['current_sale_id'] = sale.id
    else:
        sale = sale_service.create_sale(employee=employee)
        request.session['current_sale_id'] = sale.id
    
    if request.method == 'POST':
        if 'add_item' in request.POST:
            item_form = SaleItemForm(request.POST)
            if item_form.is_valid():
                result = sale_service.add_item_to_sale(
                    sale,
                    item_form.cleaned_data['item_id'],
                    item_form.cleaned_data['quantity']
                )
                if result['success']:
                    messages.success(request, 'Item added to sale')
                else:
                    messages.error(request, result['message'])
                return redirect('pos:sale_create')
        
        elif 'apply_coupon' in request.POST:
            coupon_form = CouponForm(request.POST)
            if coupon_form.is_valid():
                result = sale_service.apply_coupon(
                    sale,
                    coupon_form.cleaned_data['coupon_code']
                )
                if result['success']:
                    messages.success(request, result['message'])
                else:
                    messages.error(request, result['message'])
                return redirect('pos:sale_create')
        
        elif 'remove_item' in request.POST:
            item_id = request.POST.get('item_id')
            if sale_service.remove_item_from_sale(sale, int(item_id)):
                messages.success(request, 'Item removed from sale')
            else:
                messages.error(request, 'Failed to remove item')
            return redirect('pos:sale_create')
        
        elif 'finalize' in request.POST:
            result = sale_service.finalize_sale(sale)
            if result['success']:
                messages.success(request, f"Sale completed! Total: ${sale.total_amount}")
                del request.session['current_sale_id']
                return redirect('pos:sale_detail', sale_id=sale.id)
            else:
                messages.error(request, result['message'])
                return redirect('pos:sale_create')
    
    item_form = SaleItemForm()
    coupon_form = CouponForm()
    available_items = inventory_service.get_available_for_sale()
    
    context = {
        'sale': sale,
        'item_form': item_form,
        'coupon_form': coupon_form,
        'available_items': available_items,
    }
    return render(request, 'pos/sale_create.html', context)


@employee_login_required
def sale_detail_view(request, sale_id):
    """View sale details"""
    sale = get_object_or_404(Sale, id=sale_id)
    context = {
        'sale': sale,
    }
    return render(request, 'pos/sale_detail.html', context)


@employee_login_required
def sale_list_view(request):
    """List all sales"""
    sale_service = SaleService()
    sales = sale_service.sale_repo.get_all()
    
    context = {
        'sales': sales,
    }
    return render(request, 'pos/sale_list.html', context)

