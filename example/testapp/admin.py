"""
Admin configuration for test models.
Showcases various Django admin features with Django Suit5.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Product, ProductImage, ProductAttribute,
    Customer, Order, OrderItem, SiteSettings
)


# Inlines
class ProductImageInline(admin.TabularInline):
    """Tabular inline for product images."""
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'sort_order']


class ProductAttributeInline(admin.TabularInline):
    """Tabular inline for product attributes."""
    model = ProductAttribute
    extra = 2
    fields = ['name', 'value']


class OrderItemInline(admin.TabularInline):
    """Tabular inline for order items."""
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']
    raw_id_fields = ['product']
    fields = ['product', 'quantity', 'unit_price', 'total_price']


# Admin classes
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin with hierarchical display."""
    list_display = ['name', 'parent', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    ordering = ['name']

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'parent')
        }),
        ('Details', {
            'fields': ('description', 'is_active'),
            'classes': ('collapse',)
        }),
    )

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin with tabs and inlines."""
    list_display = [
        'name', 'category', 'price', 'sale_price', 'stock_quantity',
        'status', 'is_featured', 'created_at'
    ]
    list_filter = ['status', 'is_featured', 'category', 'created_at']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['status', 'is_featured']
    raw_id_fields = ['category']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [ProductImageInline, ProductAttributeInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'sale_price'),
            'description': 'Set the product pricing. Sale price is optional.'
        }),
        ('Inventory', {
            'fields': ('sku', 'stock_quantity', 'weight'),
        }),
        ('Status', {
            'fields': ('status', 'is_featured', 'publish_date'),
        }),
        ('Media', {
            'fields': ('image', 'tags'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Customer admin with fieldsets."""
    list_display = [
        'full_name', 'email', 'membership', 'is_active',
        'order_count', 'date_joined'
    ]
    list_filter = ['membership', 'is_active', 'country', 'date_joined']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_editable = ['membership', 'is_active']
    ordering = ['last_name', 'first_name']

    fieldsets = (
        ('Personal Information', {
            'fields': (('first_name', 'last_name'), 'email', 'phone', 'birth_date')
        }),
        ('Address', {
            'fields': ('address', ('city', 'postal_code'), 'country'),
        }),
        ('Account', {
            'fields': ('membership', 'is_active', 'date_joined'),
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Name'
    full_name.admin_order_field = 'last_name'

    def order_count(self, obj):
        return obj.orders.count()
    order_count.short_description = 'Orders'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin with status colors and inlines."""
    list_display = [
        'order_number', 'customer', 'status_badge', 'payment_method',
        'total', 'is_paid', 'created_at'
    ]
    list_filter = ['status', 'payment_method', 'is_paid', 'created_at']
    search_fields = ['order_number', 'customer__first_name', 'customer__last_name', 'customer__email']
    raw_id_fields = ['customer']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    fieldsets = (
        (None, {
            'fields': ('order_number', 'customer', 'status')
        }),
        ('Payment', {
            'fields': ('payment_method', 'is_paid', 'paid_at'),
        }),
        ('Totals', {
            'fields': (('subtotal', 'tax', 'shipping_cost'), 'total'),
        }),
        ('Shipping', {
            'fields': ('shipping_address', 'shipped_at'),
        }),
        ('Billing', {
            'fields': ('billing_address',),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'pending': 'warning',
            'processing': 'info',
            'shipped': 'primary',
            'delivered': 'success',
            'cancelled': 'danger',
            'refunded': 'secondary',
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Site settings admin (singleton)."""
    list_display = ['site_name', 'contact_email', 'maintenance_mode']

    fieldsets = (
        ('General', {
            'fields': ('site_name', 'tagline')
        }),
        ('Contact', {
            'fields': ('contact_email', 'contact_phone', 'address'),
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Features', {
            'fields': (
                'maintenance_mode', 'allow_registration',
                'enable_reviews', 'items_per_page'
            ),
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
