# Seafood Company Management System

Sistema integral de gestión para empresas de mariscos, con backend en Django y API REST para integración con frontend.

## Características Principales

- **Dashboard Analítico**: Visualización de métricas clave del negocio
- **Gestión de Inventario**: Control de productos y stock
- **Procesamiento de Pedidos**: Sistema completo de gestión de órdenes
- **Gestión de Clientes**: Base de datos y perfiles de clientes
- **Gestión de Proveedores**: Administración de proveedores y compras
- **Generación de Informes**: Reportes personalizables de ventas, inventario y más
- **API REST**: Endpoints documentados para integración con frontend

## Requisitos del Sistema

- Python 3.8+
- Django 3.2+
- Django REST Framework
- Base de datos SQLite (por defecto)

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone [url-del-repositorio]
   cd seafood_backend
   ```

2. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar la base de datos:
   ```bash
   python manage.py migrate
   ```

5. Crear superusuario:
   ```bash
   python manage.py createsuperuser
   ```

6. Iniciar servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## Documentación de la API

### Endpoints Principales

#### Autenticación
- `POST /api/login/`: Iniciar sesión
- `POST /api/logout/`: Cerrar sesión

#### Inventario
- `GET /api/inventario/`: Listar productos
- `POST /api/inventario/`: Crear nuevo producto
- `GET /api/inventario/{id}/`: Obtener detalles de producto
- `PUT /api/inventario/{id}/`: Actualizar producto
- `DELETE /api/inventario/{id}/`: Eliminar producto
- `PATCH /api/inventario/{id}/ajustar-stock/`: Ajustar stock de producto

#### Pedidos
- `GET /api/pedidos/`: Listar pedidos
- `POST /api/pedidos/`: Crear nuevo pedido
- `GET /api/pedidos/{id}/`: Obtener detalles de pedido
- `PUT /api/pedidos/{id}/`: Actualizar pedido
- `PATCH /api/pedidos/{id}/estado/`: Actualizar estado de pedido
- `DELETE /api/pedidos/{id}/`: Cancelar pedido

#### Clientes
- `GET /api/clientes/`: Listar clientes
- `POST /api/clientes/`: Registrar nuevo cliente
- `GET /api/clientes/{id}/`: Obtener perfil de cliente
- `PUT /api/clientes/{id}/`: Actualizar información de cliente
- `DELETE /api/clientes/{id}/`: Eliminar cliente

#### Proveedores
- `GET /api/proveedores/`: Listar proveedores
- `POST /api/proveedores/`: Registrar nuevo proveedor
- `GET /api/proveedores/{id}/`: Obtener detalles de proveedor
- `PUT /api/proveedores/{id}/`: Actualizar información de proveedor
- `DELETE /api/proveedores/{id}/`: Eliminar proveedor

#### Informes
- `GET /api/informes/`: Listar informes
- `POST /api/informes/`: Generar nuevo informe
- `GET /api/informes/{id}/`: Obtener informe específico

### Formatos de Respuesta

Todas las respuestas de la API siguen el siguiente formato:

```json
{
    "status": "success|error",
    "data": {
        // Datos de la respuesta
    },
    "message": "Mensaje descriptivo"
}
```

### Autenticación

La API utiliza autenticación basada en tokens JWT. Para hacer peticiones autenticadas:

1. Obtener token mediante POST a `/api/login/`
2. Incluir el token en el header de las peticiones:
   ```
   Authorization: Bearer <token>
   ```

### Códigos de Estado

- 200: Petición exitosa
- 201: Recurso creado exitosamente
- 400: Error en la petición
- 401: No autorizado
- 403: Acceso prohibido
- 404: Recurso no encontrado
- 500: Error interno del servidor

## Seguridad

- Todas las rutas de la API requieren autenticación
- CORS está habilitado para permitir peticiones desde el frontend
- Las contraseñas se almacenan hasheadas
- Los tokens JWT expiran después de 24 horas

## Configuraciones del Proyecto

El proyecto incluye las siguientes configuraciones principales:

- REST Framework con paginación
- CORS habilitado
- Manejo de archivos media y static
- Sistema de autenticación personalizado
- Validaciones de datos
- Manejo de errores personalizado

## Entorno de Desarrollo

### Variables de Entorno (.env)

```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Credenciales por Defecto

- Usuario: admin
- Contraseña: admin

**IMPORTANTE**: Cambiar las credenciales por defecto antes de desplegar en producción.

## Contribución

1. Fork del repositorio
2. Crear rama para nueva característica
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

## Licencia

Privada - Solo para uso interno

## Soporte

Para soporte técnico o reportar problemas, por favor crear un issue en el repositorio.
