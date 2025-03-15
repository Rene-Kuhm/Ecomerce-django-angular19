#!/bin/bash

# Terminal colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting setup of Seafood Company Backend System${NC}"

# Create project directory
echo -e "${YELLOW}Creating project directory...${NC}"
mkdir -p seafood_backend
cd seafood_backend

# Create and activate virtual environment
echo -e "${YELLOW}Setting up Python virtual environment...${NC}"
python -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing Django and required packages...${NC}"
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install django-filter
pip install django-crispy-forms
pip install django-admin-interface
pip install pillow
pip install pandas
pip install django-import-export
pip install django-simple-history
pip install whitenoise
pip install gunicorn
pip install python-decouple
pip install dj-database-url

# Create requirements file
pip freeze > requirements.txt

# Create Django project
echo -e "${YELLOW}Creating Django project structure...${NC}"
django-admin startproject seafood_project .

# Create Django apps
echo -e "${YELLOW}Creating application modules...${NC}"
python manage.py startapp dashboard
python manage.py startapp inventory
python manage.py startapp orders
python manage.py startapp customers
python manage.py startapp suppliers
python manage.py startapp reports
python manage.py startapp api

# Create directory structure
echo -e "${YELLOW}Creating additional directory structure...${NC}"
mkdir -p templates/dashboard
mkdir -p templates/inventory
mkdir -p templates/orders
mkdir -p templates/customers
mkdir -p templates/suppliers
mkdir -p templates/reports
mkdir -p templates/common

mkdir -p static/css
mkdir -p static/js
mkdir -p static/images
mkdir -p static/vendor/bootstrap
mkdir -p static/vendor/jquery
mkdir -p static/vendor/chart.js

mkdir -p media/products
mkdir -p media/profiles

# Configure settings.py
echo -e "${YELLOW}Configuring Django project settings...${NC}"
cat > seafood_project/settings.py << EOF
import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-REPLACE_WITH_YOUR_SECRET_KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'import_export',
    'simple_history',
    
    # Custom apps
    'dashboard',
    'inventory',
    'orders',
    'customers',
    'suppliers',
    'reports',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'seafood_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'seafood_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Login URL
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
EOF

# Create base URL configuration
echo -e "${YELLOW}Setting up URL configuration...${NC}"
cat > seafood_project/urls.py << EOF
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('inventory/', include('inventory.urls')),
    path('orders/', include('orders.urls')),
    path('customers/', include('customers.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('reports/', include('reports.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
EOF

# Create inventory models
echo -e "${YELLOW}Creating inventory models...${NC}"
cat > inventory/models.py << EOF
from django.db import models
from simple_history.models import HistoricalRecords

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilograms'),
        ('lb', 'Pounds'),
        ('unit', 'Unit'),
        ('box', 'Box'),
    ]
    
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
    @property
    def profit_margin(self):
        if self.cost > 0:
            return ((self.price - self.cost) / self.price) * 100
        return 0

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory_info')
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_restock_date = models.DateField(blank=True, null=True)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name_plural = "Inventory"
    
    def __str__(self):
        return f"Inventory for {self.product.name}"
    
    @property
    def needs_restock(self):
        return self.product.stock_quantity < self.minimum_stock
EOF

# Create supplier models
echo -e "${YELLOW}Creating supplier models...${NC}"
cat > suppliers/models.py << EOF
from django.db import models
from simple_history.models import HistoricalRecords

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name

class Purchase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ordered', 'Ordered'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]
    
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchases')
    purchase_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"PO-{self.id} - {self.supplier.name}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        # Update purchase total
        purchase = self.purchase
        purchase.total_amount = sum(item.total_price for item in purchase.items.all())
        purchase.save()
EOF

# Create customer models
echo -e "${YELLOW}Creating customer models...${NC}"
cat > customers/models.py << EOF
from django.db import models
from simple_history.models import HistoricalRecords

class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
        ('restaurant', 'Restaurant'),
        ('distributor', 'Distributor'),
    ]
    
    name = models.CharField(max_length=200)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='retail')
    contact_person = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
EOF

# Create order models
echo -e "${YELLOW}Creating order models...${NC}"
cat > orders/models.py << EOF
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from customers.models import Customer
from inventory.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    shipping_address = models.TextField(blank=True, null=True)
    shipping_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_orders')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_orders')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"
    
    def save(self, *args, **kwargs):
        # Calculate totals
        self.subtotal = sum(item.total_price for item in self.items.all()) if self.pk else 0
        self.total = self.subtotal + self.tax + self.shipping_cost
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        # Update order totals
        self.order.save()
EOF

# Create dashboard views
echo -e "${YELLOW}Creating dashboard views...${NC}"
cat > dashboard/views.py << EOF
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField, Avg
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from datetime import datetime, timedelta

from inventory.models import Product, Category
from orders.models import Order, OrderItem
from customers.models import Customer
from suppliers.models import Supplier, Purchase

@login_required
def dashboard(request):
    # Get current date and date ranges
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    last_month_end = start_of_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    
    # Sales statistics
    monthly_sales = Order.objects.filter(
        order_date__gte=start_of_month
    ).aggregate(
        total=Sum('total')
    )['total'] or 0
    
    last_month_sales = Order.objects.filter(
        order_date__gte=last_month_start,
        order_date__lt=start_of_month
    ).aggregate(
        total=Sum('total')
    )['total'] or 0
    
    sales_change = 0
    if last_month_sales > 0:
        sales_change = ((monthly_sales - last_month_sales) / last_month_sales) * 100
    
    # Inventory statistics
    low_stock_products = Product.objects.filter(
        inventory_info__minimum_stock__gt=F('stock_quantity')
    ).count()
    
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    
    # Customer statistics
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(is_active=True).count()
    
    # Order statistics
    pending_orders = Order.objects.filter(status='pending').count()
    processing_orders = Order.objects.filter(status='processing').count()
    
    # Top selling products
    top_products = OrderItem.objects.filter(
        order__order_date__gte=start_of_month
    ).values(
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_sales=Sum('total_price')
    ).order_by('-total_sales')[:5]
    
    # Sales over time (last 30 days)
    thirty_days_ago = today - timedelta(days=30)
    daily_sales = Order.objects.filter(
        order_date__gte=thirty_days_ago
    ).annotate(
        day=TruncDay('order_date')
    ).values('day').annotate(
        total=Sum('total')
    ).order_by('day')
    
    context = {
        'monthly_sales': monthly_sales,
        'sales_change': sales_change,
        'low_stock_products': low_stock_products,
        'total_products': total_products,
        'active_products': active_products,
        'total_customers': total_customers,
        'active_customers': active_customers,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'top_products': top_products,
        'daily_sales': daily_sales,
    }
    
    return render(request, 'dashboard/index.html', context)
EOF

# Create dashboard URLs
echo -e "${YELLOW}Setting up dashboard URLs...${NC}"
cat > dashboard/urls.py << EOF
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
EOF

# Create dashboard templates
echo -e "${YELLOW}Creating dashboard templates...${NC}"
mkdir -p templates/dashboard

# Create base template
cat > templates/base.html << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Seafood Management System{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            {% if user.is_authenticated %}
            <!-- Sidebar -->
            <nav id="sidebar" class="col-md-3 col-lg-2 d-md-block bg-dark sidebar collapse">
                <div class="position-sticky pt-3">
                    <div class="px-3 py-4 text-white">
                        <h4>Seafood Management</h4>
                    </div>
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link text-white" href="{% url 'dashboard' %}">
                                <i class="bi bi-speedometer2 me-2"></i>Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-white" href="#">
                                <i class="bi bi-box me-2"></i>Inventory
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-white" href="#">
                                <i class="bi bi-cart me-2"></i>Orders
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-white" href="#">
                                <i class="bi bi-people me-2"></i>Customers
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-white" href="#">
                                <i class="bi bi-truck me-2"></i>Suppliers
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-white" href="#">
                                <i class="bi bi-graph-up me-2"></i>Reports
                            </a>
                        </li>
                        <li class="nav-item mt-3">
                            <a class="nav-link text-white" href="{% url 'logout' %}">
                                <i class="bi bi-box-arrow-right me-2"></i>Logout
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>
            <!-- Main content -->
            <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                    <h1 class="h2">{% block header %}Dashboard{% endblock %}</h1>
                    <div class="btn-toolbar mb-2 mb-md-0">
                        {% block page_actions %}{% endblock %}
                    </div>
                </div>
                
                {% if messages %}
                <div class="messages">
                    {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
                
                {% block content %}{% endblock %}
            </main>
            {% else %}
            <main class="col-12">
                {% block auth_content %}{% endblock %}
            </main>
            {% endif %}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.3.0/dist/chart.umd.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
EOF

# Create dashboard index template
cat > templates/dashboard/index.html << EOF
{% extends 'base.html' %}

{% block title %}Dashboard - Seafood Management System{% endblock %}

{% block content %}
<div class="row">
    <!-- Sales Summary Card -->
    <div class="col-md-3 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                            Monthly Sales</div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">\${{ monthly_sales|floatformat:2 }}</div>
                        <div class="mt-2 text-muted small">
                            {% if sales_change > 0 %}
                            <span class="text-success"><i class="bi bi-arrow-up"></i> {{ sales_change|floatformat:1 }}%</span> from last month
                            {% elif sales_change < 0 %}
                            <span class="text-danger"><i class="bi bi-arrow-down"></i> {{ sales_change|floatformat:1|abs }}%</span> from last month
                            {% else %}
                            No change from last month
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-auto">
                        <i class="bi bi-currency-dollar fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Low Stock Card -->
    <div class="col-md-3 mb-4">
        <div class="card border-left-warning shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                            Low Stock Items</div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">{{ low_stock_products }}</div>
                        <div class="mt-2 text-muted small">
                            Out of {{ total_products }} total products
                        </div>
                    </div>
                    <div class="col-auto">
                        <i class="bi bi-exclamation-triangle fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Pending Orders Card -->
    <div class="col-md-3 mb-4">
        <div class="card border-left-info shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                            Pending Orders</div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">{{ pending_orders }}</div>
                        <div class="mt-2 text-muted small">
                            {{ processing_orders }} orders in processing
                        </div>
                    </div>
                    <div class="col-auto">
                        <i class="bi bi-clipboard-check fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Active Customers Card -->
    <div class="col-md-3 mb-4">
        <div class="card border-left-success shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                            Active Customers</div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">{{ active_customers }}</div>
                        <div class="mt-2 text-muted small">
                            Out of {{ total_customers }} total customers
                        </div>
                    </div>
                    <div class="col-auto">
                        <i class="bi bi-people fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <!-- Sales Chart -->
    <div class="col-xl-8 col-lg-7">
        <div class="card shadow mb-4">
            <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                <h6 class="m-0 font-weight-bold text-primary">Sales Overview</h6>
            </div>
            <div class="card-body">
                <div class="chart-area">
                    <canvas id="salesChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- Top Products Chart -->
    <div class="col-xl-4 col-lg-5">
        <div class="card shadow mb-4">
            <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                <h6 class="m-0 font-weight-bold text-primary">Top Selling Products</h6>
            </div>
            <div class="card-body">
                <div class="chart-pie pt-4 pb-2">
                    <canvas id="topProductsChart"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Sales Chart
        const salesCtx = document.getElementById('salesChart').getContext('2d');
        const salesChart = new Chart(salesCtx, {
            type: 'line',
            data: {
                labels: [
                    {% for item in daily_sales %}
                    '{{ item.day|date:"M d" }}',
                    {% endfor %}
                ],
                datasets: [{
                    label: 'Daily Sales',
                    data: [
                        {% for item in daily_sales %}
                        {{ item.total }},
                        {% endfor %}
                    ],
                    backgroundColor: 'rgba(78, 115, 223, 0.05)',
                    borderColor: 'rgba(78, 115, 223, 1)',
                    pointRadius: 3,
                    pointBackgroundColor: 'rgba(78, 115, 223, 1)',
                    pointBorderColor: 'rgba(78, 115, 223, 1)',
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: 'rgba(78, 115, 223, 1)',
                    pointHoverBorderColor: 'rgba(78, 115, 223, 1)',
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    tension: 0.3
                }]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '\$' + value;
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

        // Top Products Chart
        const productsCtx = document.getElementById('topProductsChart').getContext('2d');
        const productsChart = new Chart(productsCtx, {
            type: 'doughnut',
            data: {
                labels: [
                    {% for product in top_products %}
                    '{{ product.product__name }}',
                    {% endfor %}
                ],
                datasets: [{
                    data: [
                        {% for product in top_products %}
                        {{ product.total_sales }},
                        {% endfor %}
                    ],
                    backgroundColor: [
                        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b'
                    ],
                    hoverBackgroundColor: [
                        '#2e59d9', '#17a673', '#2c9faf', '#dda20a', '#be2617'
                    ],
                    hoverBorderColor: 'rgba(234, 236, 244, 1)',
                }]
            },
            options: {
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                cutout: '70%'
            }
        });
    });
</script>
{% endblock %}
EOF

# Create login template
cat > templates/dashboard/login.html << EOF
{% extends 'base.html' %}

{% block title %}Login - Seafood Management System{% endblock %}

{% block auth_content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-xl-10 col-lg-12 col-md-9">
            <div class="card o-hidden border-0 shadow-lg my-5">
                <div class="card-body p-0">
                    <div class="row">
                        <div class="col-lg-6 d-none d-lg-block bg-login-image">
                            <!-- Can add a seafood image here -->
                        </div>
                        <div class="col-lg-6">
                            <div class="p-5">
                                <div class="text-center">
                                    <h1 class="h4 text-gray-900 mb-4">Welcome to Seafood Management System</h1>
                                </div>
                                <form class="user" method="post">
                                    {% csrf_token %}
                                    <div class="form-group mb-3">
                                        <input type="text" class="form-control form-control-user" name="username" placeholder="Username">
                                    </div>
                                    <div class="form-group mb-3">
                                        <input type="password" class="form-control form-control-user" name="password" placeholder="Password">
                                    </div>
                                    <button type="submit" class="btn btn-primary btn-user btn-block">
                                        Login
                                    </button>
                                </form>
                                {% if form.errors %}
                                <div class="mt-3 alert alert-danger">
                                    Your username and password didn't match. Please try again.
                                </div>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# Setup admin.py files
echo -e "${YELLOW}Setting up admin interfaces...${NC}"

# Inventory admin
cat > inventory/admin.py << EOF
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Product, Inventory

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)

class InventoryInline(admin.StackedInline):
    model = Inventory
    can_delete = False
    extra = 1

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'stock_quantity', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'sku')
    inlines = [InventoryInline]
    list_editable = ('price', 'is_active')
EOF

# Suppliers admin
cat > suppliers/admin.py << EOF
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Supplier, Purchase, PurchaseItem

@admin.register(Supplier)
class SupplierAdmin(ImportExportModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'contact_person', 'email')

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1

@admin.register(Purchase)
class PurchaseAdmin(ImportExportModelAdmin):
    list_display = ('id', 'supplier', 'purchase_date', 'status', 'total_amount')
    list_filter = ('status', 'purchase_date')
    search_fields = ('supplier__name',)
    inlines = [PurchaseItemInline]
EOF

# Customers admin
cat > customers/admin.py << EOF
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ('name', 'customer_type', 'contact_person', 'phone', 'email', 'is_active')
    list_filter = ('customer_type', 'is_active')
    search_fields = ('name', 'contact_person', 'email')
EOF

# Orders admin
cat > orders/admin.py << EOF
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'status', 'payment_status', 'total')
    list_filter = ('status', 'payment_status', 'order_date')
    search_fields = ('customer__name',)
    inlines = [OrderItemInline]
    readonly_fields = ('subtotal', 'total')
EOF

# Create API app
echo -e "${YELLOW}Setting up API for React frontend...${NC}"

# API URLs
cat > api/urls.py << EOF
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'suppliers', views.SupplierViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
EOF

# API views
cat > api/views.py << EOF
from rest_framework import viewsets, permissions
from inventory.models import Product, Category
from customers.models import Customer
from orders.models import Order
from suppliers.models import Supplier
from .serializers import (
    ProductSerializer, CategorySerializer, 
    CustomerSerializer, OrderSerializer,
    SupplierSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'sku', 'description']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['customer_type', 'is_active']
    search_fields = ['name', 'contact_person', 'email']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'payment_status']
    search_fields = ['customer__name']

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['is_active']
    search_fields = ['name', 'contact_person', 'email']
EOF

# API serializers
cat > api/serializers.py << EOF
from rest_framework import serializers
from inventory.models import Product, Category
from customers.models import Customer
from orders.models import Order, OrderItem
from suppliers.models import Supplier, Purchase

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Product
        fields = '__all__'
        extra_fields = ['category_name']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'total_price', 'notes']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source='customer.name')
    
    class Meta:
        model = Order
        fields = '__all__'
        extra_fields = ['customer_name', 'items']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
EOF

# Create __init__.py files for all apps
echo -e "${YELLOW}Creating __init__.py files...${NC}"
touch dashboard/__init__.py
touch inventory/__init__.py
touch orders/__init__.py
touch customers/__init__.py
touch suppliers/__init__.py
touch reports/__init__.py
touch api/__init__.py

# Create apps.py files
echo -e "${YELLOW}Creating apps.py files...${NC}"
for app in dashboard inventory orders customers suppliers reports api; do
    cat > ${app}/apps.py << EOF
from django.apps import AppConfig

class $(echo ${app^})Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '${app}'
EOF
done

# Run migrations and setup
echo -e "${YELLOW}Running initial migrations...${NC}"
python manage.py makemigrations dashboard inventory orders customers suppliers reports
python manage.py migrate

# Create superuser
echo -e "${YELLOW}Creating superuser...${NC}"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Create README.md
cat > README.md << EOF
# Seafood Company Management System

A comprehensive backend system for managing seafood business operations.

## Features

- Dashboard with business analytics
- Inventory management
- Order processing
- Customer management
- Supplier management
- API for React frontend integration

## Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: \`pip install -r requirements.txt\`
4. Run migrations: \`python manage.py migrate\`
5. Create superuser: \`python manage.py createsuperuser\`
6. Start the development server: \`python manage.py runserver\`

## Default Credentials

- Username: admin
- Password: admin

*Note: Change the default password before deploying to production*

## API Documentation

The API is available at \`/api/\` with authentication required.
Swagger documentation is available at \`/swagger/\`.

## License

Private - For internal use only
EOF

# Create launch script
cat > run.sh << EOF
#!/bin/bash
source venv/bin/activate
python manage.py runserver
EOF
chmod +x run.sh

# Final setup and info
echo -e "${GREEN}Setup complete!${NC}"
echo -e "${GREEN}To run the development server:${NC}"
echo -e "${YELLOW}cd seafood_backend${NC}"
echo -e "${YELLOW}source venv/bin/activate${NC}"
echo -e "${YELLOW}python manage.py runserver${NC}"
echo -e "${GREEN}Access the admin panel at: http://127.0.0.1:8000/admin/${NC}"
echo -e "${GREEN}Dashboard available at: http://127.0.0.1:8000/${NC}"
echo -e "${GREEN}Default login: admin / admin${NC}"