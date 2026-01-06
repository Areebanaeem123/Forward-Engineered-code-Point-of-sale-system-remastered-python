"""
Data Migration Script
Migrates data from .txt files to Django database
Run this script after initial migration: python manage.py shell < data_migration.py
"""

import os
import sys
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db import transaction

# Import models
from pos_system.models import (
    Employee, Item, Customer, Rental, Sale, SaleItem,
    ReturnTransaction, ReturnItem, Coupon, EmployeeLog
)


def parse_date(date_str):
    """Parse date from MM/dd/yy format"""
    try:
        return datetime.strptime(date_str, '%m/%d/%y').date()
    except ValueError:
        # Try alternative format
        try:
            return datetime.strptime(date_str, '%m/%d/%Y').date()
        except ValueError:
            print(f"Warning: Could not parse date: {date_str}")
            return datetime.now().date()


def migrate_employees(file_path='Database/employeeDatabase.txt'):
    """Migrate employees from employeeDatabase.txt"""
    print("Migrating employees...")
    count = 0
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found")
        return
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) < 5:
                print(f"Warning: Invalid employee line: {line}")
                continue
            
            username = parts[0]
            position = parts[1]
            first_name = parts[2]
            last_name = parts[3]
            password = parts[4]
            
            # Check if employee already exists
            if Employee.objects.filter(username=username).exists():
                print(f"Employee {username} already exists, skipping...")
                continue
            
            Employee.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                position=position,
                password_hash=make_password(password),
                is_staff=(position == 'Admin')
            )
            count += 1
    
    print(f"Migrated {count} employees")


def migrate_items(file_path='Database/itemDatabase.txt', item_type='Sale'):
    """Migrate items from itemDatabase.txt or rentalDatabase.txt"""
    print(f"Migrating {item_type} items...")
    count = 0
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found")
        return
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) < 4:
                print(f"Warning: Invalid item line: {line}")
                continue
            
            try:
                item_id = int(parts[0])
                name = parts[1]
                price = float(parts[2])
                amount = int(parts[3])
                
                # Check if item already exists
                item, created = Item.objects.get_or_create(
                    item_id=item_id,
                    defaults={
                        'name': name,
                        'price': price,
                        'item_type': item_type,
                    }
                )
                
                if created:
                    if item_type == 'Sale':
                        item.stock_sale = amount
                    elif item_type == 'Rental':
                        item.stock_rental = amount
                    else:
                        item.stock_sale = amount
                        item.stock_rental = amount
                    item.save()
                    count += 1
                else:
                    # Update existing item
                    if item_type == 'Sale':
                        item.stock_sale = amount
                    elif item_type == 'Rental':
                        item.stock_rental = amount
                    item.save()
                    
            except (ValueError, IndexError) as e:
                print(f"Warning: Error parsing item line '{line}': {e}")
                continue
    
    print(f"Migrated {count} {item_type} items")


def migrate_customers_and_rentals(file_path='Database/userDatabase.txt'):
    """Migrate customers and rentals from userDatabase.txt"""
    print("Migrating customers and rentals...")
    customer_count = 0
    rental_count = 0
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found")
        return
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
        # Skip header line
        if lines:
            lines = lines[1:]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) < 1:
                continue
            
            try:
                phone_number = parts[0]
                
                # Get or create customer
                customer, created = Customer.objects.get_or_create(
                    phone_number=phone_number
                )
                if created:
                    customer_count += 1
                
                # Parse rental entries (format: itemID,returnDate,returned)
                if len(parts) > 1:
                    for rental_entry in parts[1:]:
                        rental_parts = rental_entry.split(',')
                        if len(rental_parts) < 3:
                            continue
                        
                        try:
                            item_id = int(rental_parts[0])
                            return_date_str = rental_parts[1]
                            returned_str = rental_parts[2]
                            
                            # Parse dates
                            due_date = parse_date(return_date_str)
                            rental_date = due_date - timedelta(days=14)  # Assume 14-day rental period
                            
                            # Check if item exists
                            try:
                                item = Item.objects.get(item_id=item_id)
                            except Item.DoesNotExist:
                                print(f"Warning: Item {item_id} not found, skipping rental")
                                continue
                            
                            # Check if rental already exists
                            is_returned = returned_str.lower() == 'true'
                            return_date = None
                            if is_returned:
                                return_date = parse_date(return_date_str)
                            
                            # Create rental record
                            Rental.objects.get_or_create(
                                customer=customer,
                                item=item,
                                due_date=due_date,
                                defaults={
                                    'rental_date': rental_date,
                                    'return_date': return_date,
                                    'is_returned': is_returned,
                                    'quantity': 1,
                                }
                            )
                            rental_count += 1
                            
                        except (ValueError, IndexError) as e:
                            print(f"Warning: Error parsing rental entry '{rental_entry}': {e}")
                            continue
                            
            except (ValueError, IndexError) as e:
                print(f"Warning: Error parsing customer line '{line}': {e}")
                continue
    
    print(f"Migrated {customer_count} customers and {rental_count} rentals")


def migrate_coupons(file_path='Database/couponNumber.txt'):
    """Migrate coupons from couponNumber.txt"""
    print("Migrating coupons...")
    count = 0
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found")
        return
    
    with open(file_path, 'r') as f:
        for line in f:
            code = line.strip()
            if not code:
                continue
            
            Coupon.objects.get_or_create(code=code)
            count += 1
    
    print(f"Migrated {count} coupons")


def migrate_employee_logs(file_path='Database/employeeLogfile.txt'):
    """Migrate employee logs from employeeLogfile.txt"""
    print("Migrating employee logs...")
    count = 0
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found")
        return
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse format: "name (username position) logs into POS System. Time: yyyy-MM-dd HH:mm:ss.SSS"
            try:
                if 'logs into' in line:
                    action = 'login'
                elif 'logs out' in line:
                    action = 'logout'
                else:
                    continue
                
                # Extract timestamp
                if 'Time: ' in line:
                    time_str = line.split('Time: ')[1].strip()
                    timestamp = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
                    
                    # Extract username (between parentheses)
                    if '(' in line and ')' in line:
                        username_part = line.split('(')[1].split(')')[0]
                        username = username_part.split()[0]
                        
                        try:
                            employee = Employee.objects.get(username=username)
                            EmployeeLog.objects.create(
                                employee=employee,
                                action=action,
                                timestamp=timestamp
                            )
                            count += 1
                        except Employee.DoesNotExist:
                            print(f"Warning: Employee {username} not found for log entry")
                            
            except (ValueError, IndexError) as e:
                print(f"Warning: Error parsing log line '{line}': {e}")
                continue
    
    print(f"Migrated {count} employee logs")


def run_migration():
    """Run all migrations"""
    print("=" * 50)
    print("Starting Data Migration from .txt files to Django Database")
    print("=" * 50)
    
    with transaction.atomic():
        migrate_employees()
        migrate_items('Database/itemDatabase.txt', 'Sale')
        migrate_items('Database/rentalDatabase.txt', 'Rental')
        migrate_customers_and_rentals()
        migrate_coupons()
        migrate_employee_logs()
    
    print("=" * 50)
    print("Data Migration Complete!")
    print("=" * 50)


if __name__ == '__main__':
    run_migration()

