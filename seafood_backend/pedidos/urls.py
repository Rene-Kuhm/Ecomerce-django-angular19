from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="pedidos"),
    path("crear/", views.pedido_crear, name="pedido_crear"),
    path("<int:pk>/", views.pedido_detalle, name="pedido_detalle"),
    path("<int:pk>/estado/", views.pedido_estado, name="pedido_estado"),
    path("<int:pk>/cancelar/", views.pedido_cancelar, name="pedido_cancelar"),
]
