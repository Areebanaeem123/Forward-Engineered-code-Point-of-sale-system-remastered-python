"""
URL Configuration for POS app
"""

from django.urls import path
from pos.views import (
    login_view, logout_view, dashboard_view,
    sale_create_view, sale_detail_view, sale_list_view,
    rental_create_view, rental_return_view, rental_list_view,
    item_list_view, item_create_view, item_detail_view, item_update_view,
    employee_list_view, employee_create_view, employee_update_view,
)

app_name = 'pos'

urlpatterns = [
    # Authentication
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Sales
    path('sale/create/', sale_create_view, name='sale_create'),
    path('sale/<int:sale_id>/', sale_detail_view, name='sale_detail'),
    path('sale/list/', sale_list_view, name='sale_list'),
    
    # Rentals
    path('rental/create/', rental_create_view, name='rental_create'),
    path('rental/return/', rental_return_view, name='rental_return'),
    path('rental/list/', rental_list_view, name='rental_list'),
    
    # Inventory
    path('item/list/', item_list_view, name='item_list'),
    path('item/create/', item_create_view, name='item_create'),
    path('item/<int:item_id>/', item_detail_view, name='item_detail'),
    path('item/<int:item_id>/update/', item_update_view, name='item_update'),
    
    # Admin
    path('employee/list/', employee_list_view, name='employee_list'),
    path('employee/create/', employee_create_view, name='employee_create'),
    path('employee/<str:username>/update/', employee_update_view, name='employee_update'),
]

