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
