# Django Suit5

**Modern theme for Django admin interface built with Bootstrap 5.**

Django Suit5 is a modern, sleek admin interface theme for Django. It provides a clean and responsive design that enhances the default Django admin experience.

## Features

- **Bootstrap 5** - Built on the latest Bootstrap framework for modern styling and responsive design
- **Bootstrap Icons** - Integrated icon library for consistent, scalable icons
- **Dark Mode** - Built-in dark theme support with automatic toggle
- **CSS Custom Properties** - Theme variables for easy customization
- **SCSS Source** - Full SCSS source files for advanced customization
- **Sortable Inlines** - Drag-and-drop sorting for inline models
- **Custom Widgets** - Enhanced date/time pickers and form widgets
- **Responsive Layout** - Mobile-friendly admin interface

## Requirements

- Django 2.2+
- Python 3.7+

## Installation

```bash
pip install django-suit5
```

Add `suit5` to your `INSTALLED_APPS` before `django.contrib.admin`:

```python
INSTALLED_APPS = [
    'suit5',
    'django.contrib.admin',
    'django.contrib.auth',
    # ...
]
```

## Configuration

Configure Django Suit5 in your `settings.py`:

```python
SUIT_CONFIG = {
    'ADMIN_NAME': 'My Admin',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
}
```

## Development

### Building CSS

The project uses SCSS for styling. To compile:

```bash
# Install dependencies
npm install

# Build CSS (compressed)
npm run build:css

# Build CSS (expanded for debugging)
npm run build:css:expanded

# Watch for changes
npm run watch:css
```

### Project Structure

```
suit5/
├── static/suit5/
│   ├── css/           # Compiled CSS
│   ├── scss/          # SCSS source files
│   ├── js/            # JavaScript files
│   ├── bootstrap5/    # Bootstrap 5 assets
│   └── icons/         # Bootstrap Icons
├── templates/admin/   # Admin template overrides
└── widgets.py         # Custom form widgets
```

## License

Django Suit5 is licensed under [Creative Commons Attribution-NonCommercial 3.0](http://creativecommons.org/licenses/by-nc/3.0/).

## Links

- Documentation: http://django-suit.readthedocs.org/
- Support: http://djangosuit.com/support/
- Issues: https://github.com/darklow/django-suit/issues
