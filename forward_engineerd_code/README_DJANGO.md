# Django POS System - Setup and Usage Guide

## Overview

This is a complete reengineered Point of Sale (POS) system built with Django 5+, migrating from a legacy Java application. The system features a modern web-based interface, database-backed architecture, and comprehensive business logic.

## Features

- **Sales Processing**: Create sales, add items, apply coupons, calculate tax
- **Rental Management**: Create rentals, track due dates, process returns with late fees
- **Inventory Management**: View and manage items, track stock levels
- **Customer Management**: Track customers and their rental history
- **Employee Management**: Admin and Cashier roles with authentication
- **Activity Logging**: Track employee activities
- **Reporting**: View sales history and rental records

## Technology Stack

- **Backend**: Python 3.x, Django 5+
- **Database**: SQLite (default, can migrate to PostgreSQL)
- **Frontend**: Django Templates + Bootstrap 5
- **Architecture**: MVT (Model-View-Template) with Service Layer and Repository Pattern

## Project Structure

```
pos_system/
├── manage.py
├── requirements.txt
├── pos/                          # Main POS application
│   ├── models.py                 # Database models
│   ├── services/                 # Business logic layer
│   ├── repositories/             # Data access layer
│   ├── views/                    # View controllers
│   ├── forms/                    # Django forms
│   ├── templates/pos/            # HTML templates
│   ├── static/pos/              # Static files (CSS, JS)
│   ├── urls.py                   # URL routing
│   └── admin.py                  # Admin interface
├── legacy/                       # Legacy data migration
│   └── data_importer.py         # Import script
└── pos_system/                   # Django project settings
    ├── settings.py
    └── urls.py
```

## Installation

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### 2. Setup Steps

#### Step 1: Activate Virtual Environment

```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Step 4: Import Legacy Data (Optional)

```bash
python legacy/data_importer.py
```

This will import data from the legacy `.txt` files into the Django database.

#### Step 5: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

#### Step 6: Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### Login

1. Navigate to `http://127.0.0.1:8000/`
2. Enter username and password
3. Default employees (from legacy data):
   - Admin: `110001` / `1`
   - Cashier: `110002` / `lehigh2016`

### Dashboard

After login, you'll see the dashboard with options to:
- Create new sale
- Create new rental
- View inventory
- Process returns
- Admin functions (if admin)

### Creating a Sale

1. Click "New Sale" from dashboard
2. Enter Item ID and quantity
3. Click "Add Item"
4. Optionally apply a coupon
5. Click "Complete Sale" to finalize

### Creating a Rental

1. Click "New Rental" from dashboard
2. Enter customer phone number
3. Enter Item ID and quantity
4. Click "Create Rental"

### Processing Returns

1. Click "Process Return" from dashboard
2. Enter customer phone number
3. Select rental to return
4. System calculates late fees automatically

## Default Data

After running the data importer, you'll have:
- **Employees**: From `employeeDatabase.txt`
- **Items**: From `itemDatabase.txt`
- **Customers**: From `userDatabase.txt`
- **Rentals**: From `userDatabase.txt`
- **Coupons**: From `couponNumber.txt`

## Architecture

### Layers

1. **Presentation Layer**: Django Templates + Views
2. **Business Logic Layer**: Service classes
3. **Data Access Layer**: Repository classes + Django ORM
4. **Data Persistence**: SQLite database

### Design Patterns

- **Singleton**: SystemConfig for centralized configuration
- **Repository**: Abstract database operations
- **Service Layer**: Centralize business logic
- **Observer**: Activity logging, stock alerts

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
```

### Applying Migrations

```bash
python manage.py migrate
```

### Accessing Admin Panel

1. Navigate to `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials

## Troubleshooting

### Database Issues

If you encounter database errors:
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading

```bash
python manage.py collectstatic
```

### Import Errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Production Deployment

For production deployment:

1. **Use PostgreSQL** instead of SQLite
2. **Set DEBUG = False** in settings.py
3. **Configure ALLOWED_HOSTS**
4. **Set up proper SECRET_KEY**
5. **Use a production WSGI server** (e.g., Gunicorn)
6. **Set up static file serving** (e.g., WhiteNoise or Nginx)

## Documentation

- **Architecture Documentation**: See `ARCHITECTURE_DOCUMENTATION.md`
- **Migration Plan**: See `FORWARD_ENGINEERING_PLAN.md`
- **Data Restructuring**: See `DATA_RESTRUCTURING_REPORT.md`

## Support

For issues or questions, refer to the documentation files or Django's official documentation at https://docs.djangoproject.com/

