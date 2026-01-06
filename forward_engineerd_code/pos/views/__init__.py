"""
Views for POS System
"""

from .auth_views import login_view, logout_view, dashboard_view
from .sale_views import sale_create_view, sale_detail_view, sale_list_view
from .rental_views import rental_create_view, rental_return_view, rental_list_view
from .inventory_views import item_list_view, item_create_view, item_detail_view, item_update_view
from .admin_views import employee_list_view, employee_create_view, employee_update_view

__all__ = [
    'login_view',
    'logout_view',
    'dashboard_view',
    'sale_create_view',
    'sale_detail_view',
    'sale_list_view',
    'rental_create_view',
    'rental_return_view',
    'rental_list_view',
    'item_list_view',
    'item_create_view',
    'item_detail_view',
    'item_update_view',
    'employee_list_view',
    'employee_create_view',
    'employee_update_view',
]

