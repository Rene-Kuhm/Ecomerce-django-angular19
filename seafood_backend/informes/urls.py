from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="informes"),
    path("generar/", views.generar_informe, name="generar_informe"),
]
