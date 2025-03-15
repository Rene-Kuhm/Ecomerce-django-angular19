from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("inventario/", include("inventario.urls")),
    path("pedidos/", include("pedidos.urls")),
    path("clientes/", include("clientes.urls")),
    path("proveedores/", include("proveedores.urls")),
    path("informes/", include("informes.urls")),
    path("api/", include("api.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='api_index'),
    path('inventario/', views.get_inventario, name='api_inventario'),
    path('pedidos/', views.get_pedidos, name='api_pedidos'),
    path('clientes/', views.get_clientes, name='api_clientes'),
    path('proveedores/', views.get_proveedores, name='api_proveedores'),
    path('informes/', views.get_informes, name='api_informes'),
]
