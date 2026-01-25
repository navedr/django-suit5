# Django Suit Demo Project

Example Django project to test the Bootstrap 5 migration of Django Suit.

## Requirements

- Python 3.8+
- Django 2.2+ (tested with 2.2, works with 3.x and 4.x)

## Quick Start

1. Create a virtual environment:
```bash
cd example
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the setup script (creates database, migrations, sample data):
```bash
python setup_demo.py
```

4. Start the development server:
```bash
python manage.py runserver
```

5. Open http://localhost:8000/admin/ and login with:
   - **Username:** admin
   - **Password:** admin

## Features Demonstrated

### Models
- **Categories** - Hierarchical categories with parent/child relationships
- **Products** - Products with various field types, inlines for images and attributes
- **Customers** - Customer management with fieldsets
- **Orders** - Order management with line items (inline)
- **Site Settings** - Singleton model for site configuration

### Admin Features
- List views with filters, search, date hierarchy
- Fieldsets with collapse functionality
- Tabular and stacked inlines
- Raw ID fields for foreign keys
- Custom admin actions
- Status badges with colors
- Form validation
- Dark theme support (click moon icon in header)

## Testing the Bootstrap 5 Migration

After setting up, test the following:

1. **Login Page** - Check styling and form layout
2. **Dashboard** - Verify menu icons and layout
3. **List Views** - Test tables, filters, pagination
4. **Change Forms** - Test fieldsets, inlines, widgets
5. **Dark Theme** - Click the theme toggle in the header
6. **Alerts** - Messages should display correctly
7. **Date/Time Widgets** - Calendar and clock popups
8. **Search** - Quick search in the left sidebar

## Troubleshooting

If static files aren't loading, run:
```bash
python manage.py collectstatic
```

Or ensure `DEBUG = True` in settings for development.
