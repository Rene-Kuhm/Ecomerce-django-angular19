from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="inventario"),
    path("producto/crear/", views.producto_crear, name="producto_crear"),
    path("producto/<int:pk>/editar/", views.producto_editar, name="producto_editar"),
    path("producto/<int:pk>/eliminar/", views.producto_eliminar, name="producto_eliminar"),
    path("producto/<int:pk>/ajustar-stock/", views.ajustar_stock, name="ajustar_stock"),
]
