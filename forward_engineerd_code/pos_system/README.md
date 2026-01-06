# POS System - Django Reengineering

This is a forward-engineered Django web application based on a legacy Java POS system.

## Project Structure

```
pos_system/                 # Django project root
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
├── pos_system/           # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI configuration
└── core/                 # Core POS functionality app
    ├── models.py        # Database models
    ├── views.py         # View controllers
    ├── admin.py         # Admin interface
    ├── services/        # Business logic layer
    ├── repositories/    # Data access layer
    ├── templates/       # HTML templates
    └── static/          # CSS, JS, images
```

## Setup Instructions

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run development server:**
   ```bash
   python manage.py runserver
   ```

## Testing

Run tests using pytest:
```bash
pytest
```

Run property-based tests with Hypothesis:
```bash
pytest -v
```

## Technology Stack

- **Framework:** Django 4.2
- **Database:** SQLite (development) / PostgreSQL (production)
- **Testing:** pytest, pytest-django, Hypothesis, factory-boy
- **Architecture:** MVT with service and repository layers
