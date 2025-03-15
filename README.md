# Seafood Backend

Sistema de gestión para empresas de mariscos desarrollado con Django.

## Características

### Inventario
- Gestión de productos y categorías
- Control de stock
- Sistema de códigos únicos para productos
- Seguimiento de lotes
- Control de calidad HACCP
- Registro de incidencias
- Historial de cambios en productos

### Características Técnicas
- Django 5.1.7
- Django REST Framework
- Autenticación JWT
- Redis para cache
- Celery para tareas asíncronas
- Simple History para auditoría
- Swagger/OpenAPI para documentación de API
- Bootstrap 4 para la interfaz
- Soporte para imágenes de productos

## Configuración del Entorno

1. Clonar el repositorio
```bash
git clone <repository-url>
cd seafood_backend
```

2. Crear y activar entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos
```bash
python manage.py migrate
```

5. Crear superusuario
```bash
python manage.py createsuperuser
```

6. Iniciar el servidor Redis
```bash
redis-server
```

7. Iniciar Celery
```bash
celery -A seafood_project worker -l info
```

8. Iniciar el servidor de desarrollo
```bash
python manage.py runserver 8001
```

## Estructura del Proyecto

```
seafood_backend/
├── api/                 # Aplicación para API REST
├── clientes/           # Gestión de clientes
├── dashboard/          # Panel de control principal
├── finanzas/          # Gestión financiera
├── informes/          # Generación de informes
├── inventario/        # Gestión de inventario
│   ├── models.py      # Modelos de datos
│   ├── views.py       # Vistas
│   └── urls.py        # URLs
├── pedidos/           # Gestión de pedidos
├── proveedores/       # Gestión de proveedores
├── static/            # Archivos estáticos
├── templates/         # Plantillas HTML
└── seafood_project/   # Configuración principal
```

## Modelos Principales

### Inventario
- Producto
- Categoría
- PuntoControlHACCP
- RegistroCalidad
- Incidencia

## API REST

La API REST está documentada usando Swagger/OpenAPI y disponible en:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## Seguridad

- Autenticación basada en JWT
- CORS configurado para desarrollo local
- CSRF habilitado
- Permisos basados en usuarios autenticados

## Licencia

[Especificar licencia]

## Soporte

[Información de contacto para soporte]
