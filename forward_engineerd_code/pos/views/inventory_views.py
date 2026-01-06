"""
Inventory Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from pos.views.auth_views import employee_login_required
from pos.forms.item_forms import ItemForm
from pos.services.inventory_service import InventoryService
from pos.models import Item


def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and user.is_staff


@employee_login_required
def item_list_view(request):
    """List all items"""
    inventory_service = InventoryService()
    items = inventory_service.get_all_items()
    
    context = {
        'items': items,
    }
    return render(request, 'pos/item_list.html', context)


@employee_login_required
def item_create_view(request):
    """Create new item"""
    if not request.session.get('is_admin', False):
        messages.error(request, 'Access denied. Admin only.')
        return redirect('pos:item_list')
    
    inventory_service = InventoryService()
    
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            try:
                item = inventory_service.create_item(
                    item_id=form.cleaned_data['item_id'],
                    name=form.cleaned_data['name'],
                    price=float(form.cleaned_data['price']),
                    stock_sale=form.cleaned_data['stock_sale'],
                    stock_rental=form.cleaned_data['stock_rental'],
                    item_type=form.cleaned_data['item_type']
                )
                messages.success(request, 'Item created successfully')
                return redirect('pos:item_detail', item_id=item.item_id)
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ItemForm()
    
    context = {
        'form': form,
    }
    return render(request, 'pos/item_create.html', context)


@employee_login_required
def item_detail_view(request, item_id):
    """View item details"""
    inventory_service = InventoryService()
    item = inventory_service.get_item(item_id)
    
    if not item:
        messages.error(request, 'Item not found')
        return redirect('pos:item_list')
    
    context = {
        'item': item,
    }
    return render(request, 'pos/item_detail.html', context)


@employee_login_required
def item_update_view(request, item_id):
    """Update item"""
    if not request.session.get('is_admin', False):
        messages.error(request, 'Access denied. Admin only.')
        return redirect('pos:item_list')
    
    inventory_service = InventoryService()
    item = inventory_service.get_item(item_id)
    
    if not item:
        messages.error(request, 'Item not found')
        return redirect('pos:item_list')
    
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully')
            return redirect('pos:item_detail', item_id=item.item_id)
    else:
        form = ItemForm(instance=item)
    
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'pos/item_update.html', context)

