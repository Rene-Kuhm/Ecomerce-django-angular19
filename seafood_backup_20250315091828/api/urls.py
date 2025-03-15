from django.urls import path, include
from rest_framework.routers import DefaultRouter

# DefaultRouter para la API
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
