from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="proveedores"),
    path("crear/", views.proveedor_crear, name="proveedor_crear"),
    path("<int:pk>/editar/", views.proveedor_editar, name="proveedor_editar"),
    path("<int:pk>/eliminar/", views.proveedor_eliminar, name="proveedor_eliminar"),
    path("<int:pk>/activar/", views.proveedor_activar, name="proveedor_activar"),
]
