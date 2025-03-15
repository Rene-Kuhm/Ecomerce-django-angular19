#!/bin/bash

# Definición de colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # Sin Color

echo -e "${GREEN}=== SOLUCIÓN DEFINITIVA: SISTEMA DE GESTIÓN DE MARISCOS ===${NC}"

# Verificar ubicación actual
CURRENT_DIR=$(pwd)
PROJECT_BASE=$(dirname "$CURRENT_DIR")
BACKUP_DIR="${PROJECT_BASE}/seafood_backup_$(date +%Y%m%d%H%M%S)"

# Crear copia de seguridad del proyecto actual
echo -e "${YELLOW}Creando copia de seguridad del proyecto actual en: ${BACKUP_DIR}${NC}"
mkdir -p "$BACKUP_DIR"
cp -R * "$BACKUP_DIR/"

# Crear nuevo proyecto
echo -e "${YELLOW}Recreando el proyecto desde cero...${NC}"

# Activar entorno virtual existente o crear uno nuevo
if [ -d "venv" ]; then
    echo -e "${YELLOW}Utilizando entorno virtual existente...${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}Creando nuevo entorno virtual...${NC}"
    python3 -m venv venv
    source venv/bin/activate
fi

# Instalar dependencias requeridas
echo -e "${YELLOW}Instalando dependencias...${NC}"
pip install --upgrade pip
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install django-filter
pip install django-crispy-forms
pip install crispy-bootstrap4
pip install pillow
pip install django-import-export
pip install django-simple-history
pip install whitenoise
pip install gunicorn
pip install python-decouple
pip install dj-database-url

# Crear estructura de proyecto fresca
echo -e "${YELLOW}Creando estructura de proyecto fresca...${NC}"

# Crear proyecto Django si no existe
if [ ! -d "seafood_project" ]; then
    django-admin startproject seafood_project .
fi

# Crear aplicaciones en español
for app in dashboard inventario pedidos clientes proveedores informes api
do
    echo -e "${YELLOW}Creando aplicación $app...${NC}"
    if [ ! -d "$app" ]; then
        python manage.py startapp $app
    fi
    
    # Asegurar que existan directorios para migrations
    mkdir -p $app/migrations
    touch $app/migrations/__init__.py
done

# Crear estructura de directorios para templates y static
mkdir -p templates/{dashboard,inventario,pedidos,clientes,proveedores,informes,common,registration}
mkdir -p static/{css,js,images}
mkdir -p media/{productos,usuarios}

# Configurar settings.py
echo -e "${YELLOW}Configurando settings.py...${NC}"
cat > seafood_project/settings.py << EOF
import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$(python -c "import secrets; print(secrets.token_hex(32))")'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Aplicaciones de terceros
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap4',
    'import_export',
    'simple_history',
    
    # Aplicaciones propias
    'dashboard',
    'inventario',
    'pedidos',
    'clientes',
    'proveedores',
    'informes',
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
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# Login URL
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
EOF

# Configurar urls.py principal
echo -e "${YELLOW}Configurando urls.py principal...${NC}"
cat > seafood_project/urls.py << EOF
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('inventario/', include('inventario.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('clientes/', include('clientes.urls')),
    path('proveedores/', include('proveedores.urls')),
    path('informes/', include('informes.urls')),
    path('api/', include('api.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
EOF

# Configurar urls.py de cada aplicación
for app in dashboard inventario pedidos clientes proveedores informes api
do
    echo -e "${YELLOW}Configurando urls.py para $app...${NC}"
    cat > $app/urls.py << EOF
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='$app'),
]
EOF
done

# Configurar views.py básico para cada aplicación
for app in dashboard inventario pedidos clientes proveedores informes
do
    echo -e "${YELLOW}Configurando views.py para $app...${NC}"
    cat > $app/views.py << EOF
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {
        'titulo': '$(echo ${app^})',
    }
    return render(request, '$app/index.html', context)
EOF
done

# Configurar API views
echo -e "${YELLOW}Configurando views.py para api...${NC}"
cat > api/views.py << EOF
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_root(request):
    return Response({
        'mensaje': 'API de Sistema de Gestión de Mariscos',
        'versión': '1.0',
    })
EOF

# Crear templates básicos
echo -e "${YELLOW}Creando templates básicos...${NC}"

# Template base
cat > templates/base.html << EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema de Gestión de Mariscos{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'dashboard' %}">Sistema de Mariscos</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'dashboard' %}">Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'inventario' %}">Inventario</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'pedidos' %}">Pedidos</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'clientes' %}">Clientes</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'proveedores' %}">Proveedores</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'informes' %}">Informes</a>
                    </li>
                </ul>
                {% if user.is_authenticated %}
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'admin:index' %}">Admin</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'logout' %}">Cerrar sesión</a>
                    </li>
                </ul>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>

    <footer class="bg-dark text-white text-center py-3 mt-5">
        <div class="container">
            <p class="mb-0">Sistema de Gestión de Mariscos &copy; 2025</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
EOF

# Template de login
cat > templates/registration/login.html << EOF
{% extends 'base.html' %}

{% block title %}Iniciar Sesión | Sistema de Gestión de Mariscos{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0">Iniciar Sesión</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label for="id_username" class="form-label">Usuario</label>
                        <input type="text" name="username" id="id_username" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label for="id_password" class="form-label">Contraseña</label>
                        <input type="password" name="password" id="id_password" class="form-control" required>
                    </div>
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">Ingresar</button>
                    </div>
                </form>
                
                {% if form.errors %}
                <div class="alert alert-danger mt-3">
                    Usuario o contraseña incorrectos. Por favor intente nuevamente.
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# Template para cada aplicación
for app in dashboard inventario pedidos clientes proveedores informes
do
    app_title=$(echo ${app^})  # Capitalizar
    cat > templates/$app/index.html << EOF
{% extends 'base.html' %}

{% block title %}${app_title} | Sistema de Gestión de Mariscos{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header bg-primary text-white">
        <h2>${app_title}</h2>
    </div>
    <div class="card-body">
        <p>Bienvenido al módulo de ${app_title}.</p>
        <p>Aquí podrá gestionar toda la información relacionada con ${app_title}.</p>
    </div>
</div>
{% endblock %}
EOF
done

# Template especial para dashboard
cat > templates/dashboard/index.html << EOF
{% extends 'base.html' %}

{% block title %}Dashboard | Sistema de Gestión de Mariscos{% endblock %}

{% block content %}
<h1 class="mb-4">Panel de Control</h1>

<div class="row">
    <div class="col-md-4 mb-4">
        <div class="card bg-primary text-white">
            <div class="card-body">
                <h5 class="card-title">Inventario</h5>
                <p class="card-text">Gestión de productos y existencias</p>
                <a href="{% url 'inventario' %}" class="btn btn-light">Acceder</a>
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-4">
        <div class="card bg-success text-white">
            <div class="card-body">
                <h5 class="card-title">Pedidos</h5>
                <p class="card-text">Control de órdenes y envíos</p>
                <a href="{% url 'pedidos' %}" class="btn btn-light">Acceder</a>
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-4">
        <div class="card bg-info text-white">
            <div class="card-body">
                <h5 class="card-title">Clientes</h5>
                <p class="card-text">Administración de clientes</p>
                <a href="{% url 'clientes' %}" class="btn btn-light">Acceder</a>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-4 mb-4">
        <div class="card bg-warning">
            <div class="card-body">
                <h5 class="card-title">Proveedores</h5>
                <p class="card-text">Gestión de proveedores</p>
                <a href="{% url 'proveedores' %}" class="btn btn-dark">Acceder</a>
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-4">
        <div class="card bg-danger text-white">
            <div class="card-body">
                <h5 class="card-title">Informes</h5>
                <p class="card-text">Reportes y estadísticas</p>
                <a href="{% url 'informes' %}" class="btn btn-light">Acceder</a>
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-4">
        <div class="card bg-secondary text-white">
            <div class="card-body">
                <h5 class="card-title">Administración</h5>
                <p class="card-text">Panel de administración</p>
                <a href="{% url 'admin:index' %}" class="btn btn-light">Acceder</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# Limpiar base de datos existente
echo -e "${YELLOW}Eliminando base de datos existente...${NC}"
if [ -f "db.sqlite3" ]; then
    rm db.sqlite3
fi

# Ejecutar migraciones
echo -e "${YELLOW}Ejecutando migraciones...${NC}"
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
echo -e "${YELLOW}Creando superusuario...${NC}"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

echo -e "${GREEN}¡Configuración completada con éxito!${NC}"
echo -e "${GREEN}Ahora puede ejecutar el servidor:${NC}"
echo -e "${YELLOW}python manage.py runserver${NC}"
echo -e "${GREEN}Acceda al panel de administración: http://127.0.0.1:8000/admin/${NC}"
echo -e "${GREEN}Usuario: admin${NC}"
echo -e "${GREEN}Contraseña: admin${NC}"