#!/usr/bin/env python
"""
Setup script for the Django Suit demo project.
Creates database, superuser, and sample data.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from testapp.models import Category, Product, Customer, Order, OrderItem, SiteSettings
from decimal import Decimal
from django.utils import timezone
import random


def create_superuser():
    """Create admin superuser."""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )
        print("Created superuser: admin / admin")
    else:
        print("Superuser 'admin' already exists")


def create_categories():
    """Create sample categories."""
    categories = [
        {'name': 'Electronics', 'slug': 'electronics', 'description': 'Electronic devices and gadgets'},
        {'name': 'Clothing', 'slug': 'clothing', 'description': 'Fashion and apparel'},
        {'name': 'Books', 'slug': 'books', 'description': 'Books and publications'},
        {'name': 'Home & Garden', 'slug': 'home-garden', 'description': 'Home and garden products'},
        {'name': 'Sports', 'slug': 'sports', 'description': 'Sports equipment and accessories'},
    ]

    created = 0
    for cat_data in categories:
        cat, is_created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if is_created:
            created += 1

    # Add subcategories
    electronics = Category.objects.get(slug='electronics')
    sub_categories = [
        {'name': 'Smartphones', 'slug': 'smartphones', 'parent': electronics},
        {'name': 'Laptops', 'slug': 'laptops', 'parent': electronics},
        {'name': 'Accessories', 'slug': 'accessories', 'parent': electronics},
    ]

    for sub_data in sub_categories:
        cat, is_created = Category.objects.get_or_create(
            slug=sub_data['slug'],
            defaults=sub_data
        )
        if is_created:
            created += 1

    print(f"Created {created} categories")


def create_products():
    """Create sample products."""
    products_data = [
        {
            'name': 'iPhone 15 Pro',
            'slug': 'iphone-15-pro',
            'category': 'smartphones',
            'price': Decimal('999.00'),
            'sale_price': Decimal('949.00'),
            'sku': 'IPH15PRO-001',
            'stock_quantity': 50,
            'status': 'published',
            'is_featured': True,
            'description': 'The latest iPhone with advanced camera system and A17 Pro chip.',
        },
        {
            'name': 'MacBook Pro 14"',
            'slug': 'macbook-pro-14',
            'category': 'laptops',
            'price': Decimal('1999.00'),
            'sku': 'MBP14-001',
            'stock_quantity': 25,
            'status': 'published',
            'is_featured': True,
            'description': 'Powerful laptop for professionals with M3 Pro chip.',
        },
        {
            'name': 'AirPods Pro',
            'slug': 'airpods-pro',
            'category': 'accessories',
            'price': Decimal('249.00'),
            'sale_price': Decimal('199.00'),
            'sku': 'APP-001',
            'stock_quantity': 100,
            'status': 'published',
            'description': 'Premium wireless earbuds with active noise cancellation.',
        },
        {
            'name': 'Samsung Galaxy S24',
            'slug': 'samsung-galaxy-s24',
            'category': 'smartphones',
            'price': Decimal('799.00'),
            'sku': 'SGS24-001',
            'stock_quantity': 40,
            'status': 'published',
            'description': 'Flagship Android smartphone with AI features.',
        },
        {
            'name': 'USB-C Hub',
            'slug': 'usb-c-hub',
            'category': 'accessories',
            'price': Decimal('49.99'),
            'sku': 'USBC-HUB-001',
            'stock_quantity': 200,
            'status': 'published',
            'description': 'Multi-port USB-C hub with HDMI, USB-A, and SD card reader.',
        },
        {
            'name': 'Wireless Mouse',
            'slug': 'wireless-mouse',
            'category': 'accessories',
            'price': Decimal('29.99'),
            'sku': 'WM-001',
            'stock_quantity': 150,
            'status': 'draft',
            'description': 'Ergonomic wireless mouse with long battery life.',
        },
    ]

    created = 0
    for prod_data in products_data:
        category = Category.objects.get(slug=prod_data.pop('category'))
        prod, is_created = Product.objects.get_or_create(
            slug=prod_data['slug'],
            defaults={**prod_data, 'category': category}
        )
        if is_created:
            created += 1

    print(f"Created {created} products")


def create_customers():
    """Create sample customers."""
    customers_data = [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '+1-555-0101',
            'city': 'New York',
            'country': 'USA',
            'membership': 'gold',
        },
        {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone': '+1-555-0102',
            'city': 'Los Angeles',
            'country': 'USA',
            'membership': 'platinum',
        },
        {
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'email': 'bob.johnson@example.com',
            'phone': '+1-555-0103',
            'city': 'Chicago',
            'country': 'USA',
            'membership': 'silver',
        },
        {
            'first_name': 'Alice',
            'last_name': 'Williams',
            'email': 'alice.williams@example.com',
            'phone': '+1-555-0104',
            'city': 'Houston',
            'country': 'USA',
            'membership': 'basic',
        },
    ]

    created = 0
    for cust_data in customers_data:
        cust, is_created = Customer.objects.get_or_create(
            email=cust_data['email'],
            defaults=cust_data
        )
        if is_created:
            created += 1

    print(f"Created {created} customers")


def create_orders():
    """Create sample orders."""
    customers = list(Customer.objects.all())
    products = list(Product.objects.filter(status='published'))

    if not customers or not products:
        print("No customers or products to create orders")
        return

    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    payment_methods = ['credit_card', 'paypal', 'bank_transfer']

    created = 0
    for i in range(10):
        order_number = f"ORD-{timezone.now().strftime('%Y%m%d')}-{i+1:04d}"

        if Order.objects.filter(order_number=order_number).exists():
            continue

        customer = random.choice(customers)
        status = random.choice(statuses)
        payment = random.choice(payment_methods)

        # Calculate totals
        num_items = random.randint(1, 3)
        order_products = random.sample(products, min(num_items, len(products)))

        subtotal = Decimal('0.00')
        items_data = []
        for prod in order_products:
            qty = random.randint(1, 3)
            price = prod.sale_price if prod.sale_price else prod.price
            items_data.append({
                'product': prod,
                'quantity': qty,
                'unit_price': price,
                'total_price': price * qty
            })
            subtotal += price * qty

        tax = subtotal * Decimal('0.08')
        shipping = Decimal('9.99') if subtotal < Decimal('100') else Decimal('0')
        total = subtotal + tax + shipping

        order = Order.objects.create(
            order_number=order_number,
            customer=customer,
            status=status,
            payment_method=payment,
            subtotal=subtotal,
            tax=tax.quantize(Decimal('0.01')),
            shipping_cost=shipping,
            total=total.quantize(Decimal('0.01')),
            shipping_address=f"{customer.first_name} {customer.last_name}\n123 Main St\n{customer.city}, {customer.country}",
            is_paid=status in ['shipped', 'delivered'],
            paid_at=timezone.now() if status in ['shipped', 'delivered'] else None,
        )

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        created += 1

    print(f"Created {created} orders")


def create_site_settings():
    """Create site settings."""
    settings, created = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'Django Suit Demo Store',
            'tagline': 'Your one-stop shop for everything',
            'contact_email': 'contact@example.com',
            'contact_phone': '+1-555-0100',
            'address': '123 Demo Street\nDemo City, DC 12345',
            'meta_description': 'Django Suit demo e-commerce store',
        }
    )
    if created:
        print("Created site settings")
    else:
        print("Site settings already exist")


def main():
    """Run all setup tasks."""
    print("\n=== Django Suit Demo Setup ===\n")

    from django.core.management import call_command
    print("Running migrations...")
    call_command('migrate', verbosity=0)

    create_superuser()
    create_categories()
    create_products()
    create_customers()
    create_orders()
    create_site_settings()

    print("\n=== Setup Complete ===")
    print("\nRun the development server with:")
    print("  cd example && python manage.py runserver")
    print("\nLogin at http://localhost:8000/admin/")
    print("  Username: admin")
    print("  Password: admin")
    print("")


if __name__ == '__main__':
    main()
