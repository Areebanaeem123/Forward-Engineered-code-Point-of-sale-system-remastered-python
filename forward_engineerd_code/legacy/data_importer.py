"""
Legacy Data Importer
Migrates data from .txt files to Django database
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_system.settings')
django.setup()

from pos.models import Employee, Item, Customer, Rental, Coupon, EmployeeLog
from pos.config import SystemConfig
from django.contrib.auth.hashers import make_password


def import_employees():
    """Import employees from employeeDatabase.txt"""
    file_path = SystemConfig.EMPLOYEE_DB
    count = 0
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split()
                if len(parts) >= 5:
                    username = parts[0]
                    position = parts[1]
                    first_name = parts[2]
                    last_name = parts[3]
                    password = parts[4]
                    
                    # Check if employee already exists
                    if not Employee.objects.filter(username=username).exists():
                        Employee.objects.create_user(
                            username=username,
                            first_name=first_name,
                            last_name=last_name,
                            position=position,
                            password=password,
                            is_staff=(position == 'Admin')
                        )
                        count += 1
                        print(f"Imported employee: {username}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    
    return count


def import_items():
    """Import items from itemDatabase.txt"""
    file_path = SystemConfig.ITEM_DB
    count = 0
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split()
                if len(parts) >= 4:
                    item_id = int(parts[0])
                    name = parts[1]
                    price = float(parts[2])
                    amount = int(parts[3])
                    
                    # Check if item already exists
                    if not Item.objects.filter(item_id=item_id).exists():
                        Item.objects.create(
                            item_id=item_id,
                            name=name,
                            price=Decimal(str(price)),
                            stock_sale=amount,
                            stock_rental=amount,
                            item_type='Both'
                        )
                        count += 1
                        print(f"Imported item: {name} (ID: {item_id})")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    
    return count


def import_customers():
    """Import customers from userDatabase.txt"""
    file_path = SystemConfig.USER_DB
    count = 0
    
    try:
        with open(file_path, 'r') as f:
            # Skip first line (header)
            next(f, None)
            
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split()
                if len(parts) >= 1:
                    phone_number = parts[0]
                    
                    # Check if customer already exists
                    if not Customer.objects.filter(phone_number=phone_number).exists():
                        Customer.objects.create(phone_number=phone_number)
                        count += 1
                        print(f"Imported customer: {phone_number}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    
    return count


def import_rentals():
    """Import rentals from userDatabase.txt"""
    file_path = SystemConfig.USER_DB
    count = 0
    
    try:
        with open(file_path, 'r') as f:
            # Skip first line (header)
            next(f, None)
            
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    phone_number = parts[0]
                    
                    # Get or create customer
                    customer, _ = Customer.objects.get_or_create(phone_number=phone_number)
                    
                    # Parse rental entries (format: itemID,returnDate,returned)
                    for i in range(1, len(parts)):
                        rental_data = parts[i].split(',')
                        if len(rental_data) >= 3:
                            item_id = int(rental_data[0])
                            return_date_str = rental_data[1]
                            is_returned = rental_data[2].lower() == 'true'
                            
                            # Parse date (MM/dd/yy)
                            try:
                                return_date = datetime.strptime(return_date_str, '%m/%d/%y').date()
                                rental_date = return_date - timedelta(days=SystemConfig.get_rental_period_days())
                                due_date = return_date
                                
                                # Get item
                                try:
                                    item = Item.objects.get(item_id=item_id)
                                    
                                    # Check if rental already exists
                                    if not Rental.objects.filter(
                                        customer=customer,
                                        item=item,
                                        rental_date=rental_date
                                    ).exists():
                                        Rental.objects.create(
                                            customer=customer,
                                            item=item,
                                            quantity=1,
                                            rental_date=rental_date,
                                            due_date=due_date,
                                            return_date=return_date if is_returned else None,
                                            is_returned=is_returned
                                        )
                                        count += 1
                                        print(f"Imported rental: {item.name} for {phone_number}")
                                except Item.DoesNotExist:
                                    print(f"Item {item_id} not found, skipping rental")
                            except ValueError:
                                print(f"Invalid date format: {return_date_str}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    
    return count


def import_coupons():
    """Import coupons from couponNumber.txt"""
    file_path = SystemConfig.COUPON_DB
    count = 0
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                code = line
                
                # Check if coupon already exists
                if not Coupon.objects.filter(code=code).exists():
                    Coupon.objects.create(
                        code=code,
                        discount_percentage=Decimal('10.00'),
                        is_active=True
                    )
                    count += 1
                    print(f"Imported coupon: {code}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    
    return count


def main():
    """Main import function"""
    print("=" * 50)
    print("Legacy Data Import")
    print("=" * 50)
    
    print("\n1. Importing Employees...")
    emp_count = import_employees()
    print(f"   Imported {emp_count} employees")
    
    print("\n2. Importing Items...")
    item_count = import_items()
    print(f"   Imported {item_count} items")
    
    print("\n3. Importing Customers...")
    cust_count = import_customers()
    print(f"   Imported {cust_count} customers")
    
    print("\n4. Importing Rentals...")
    rental_count = import_rentals()
    print(f"   Imported {rental_count} rentals")
    
    print("\n5. Importing Coupons...")
    coupon_count = import_coupons()
    print(f"   Imported {coupon_count} coupons")
    
    print("\n" + "=" * 50)
    print("Import Complete!")
    print("=" * 50)
    print(f"Total imported:")
    print(f"  - Employees: {emp_count}")
    print(f"  - Items: {item_count}")
    print(f"  - Customers: {cust_count}")
    print(f"  - Rentals: {rental_count}")
    print(f"  - Coupons: {coupon_count}")


if __name__ == '__main__':
    main()

