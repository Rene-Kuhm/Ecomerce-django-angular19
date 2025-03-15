from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Sum, Avg, Count
from datetime import datetime, timedelta
from django.utils import timezone

from inventario.models import Producto, PuntoControlHACCP, RegistroCalidad, Incidencia
from pedidos.models import Pedido, DetallePedido, Vehiculo, RutaEntrega
from clientes.models import Cliente
from proveedores.models import Proveedor
from informes.models import (
    Informe, PrediccionDemanda, IndicadorDesempeno, 
    RegistroKPI, RegistroSostenibilidad, CertificacionAmbiental
)
from dashboard.models import Empleado, Capacitacion, Turno
from finanzas.models import CuentaContable, AsientoContable, Factura, Pago

@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Get API root information",
    responses={200: 'API information retrieved successfully'}
)
def index(request):
    return Response({
        'mensaje': 'API del Sistema de Gestión de Mariscos',
        'versión': '1.0',
        'endpoints': {
            'inventario': '/api/inventario/',
            'pedidos': '/api/pedidos/',
            'clientes': '/api/clientes/',
            'proveedores': '/api/proveedores/',
            'informes': '/api/informes/',
        }
    })

@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Get inventory information",
    responses={
        200: 'Inventory data retrieved successfully',
        401: 'Authentication credentials were not provided'
    }
)
def get_inventario(request):
    productos = Producto.objects.all()
    data = {
        'total_productos': productos.count(),
        'productos_activos': productos.filter(activo=True).count(),
        'productos_stock_bajo': productos.filter(cantidad_stock__lte=10).count(),
    }
    return Response(data)

@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Get orders information",
    responses={
        200: 'Orders data retrieved successfully',
        401: 'Authentication credentials were not provided'
    }
)
def get_pedidos(request):
    pedidos = Pedido.objects.all()
    data = {
        'total_pedidos': pedidos.count(),
        'pedidos_pendientes': pedidos.filter(estado='pendiente').count(),
        'pedidos_completados': pedidos.filter(estado='completado').count(),
    }
    return Response(data)

@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Get clients information",
    responses={
        200: 'Clients data retrieved successfully',
        401: 'Authentication credentials were not provided'
    }
)
def get_clientes(request):
    clientes = Cliente.objects.all()
    data = {
        'total_clientes': clientes.count(),
        'clientes_activos': clientes.filter(activo=True).count(),
    }
    return Response(data)

@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Get suppliers information",
    responses={
        200: 'Suppliers data retrieved successfully',
        401: 'Authentication credentials were not provided'
    }
)
def get_proveedores(request):
    proveedores = Proveedor.objects.all()
    data = {
        'total_proveedores': proveedores.count(),
        'proveedores_activos': proveedores.filter(activo=True).count(),
    }
    return Response(data)

@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Get reports information",
    responses={
        200: 'Reports data retrieved successfully',
        401: 'Authentication credentials were not provided'
    }
)
def get_informes(request):
    informes = Informe.objects.all()
    data = {
        'total_informes': informes.count(),
        'tipos_informe': dict(Informe.TIPO_CHOICES),
    }
    return Response(data)

class ProductoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Producto.objects.all()
    
    @swagger_auto_schema(
        operation_description="Obtener lista de productos con filtros",
        manual_parameters=[
            openapi.Parameter(
                'activo', openapi.IN_QUERY,
                description="Filtrar por estado activo/inactivo",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'stock_bajo', openapi.IN_QUERY,
                description="Filtrar productos con stock bajo",
                type=openapi.TYPE_BOOLEAN
            )
        ]
    )
    def list(self, request):
        queryset = self.get_queryset()
        if 'activo' in request.query_params:
            queryset = queryset.filter(activo=request.query_params['activo'])
        if request.query_params.get('stock_bajo') == 'true':
            queryset = queryset.filter(cantidad_stock__lte=10)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    @swagger_auto_schema(
        operation_description="Ajustar stock de un producto",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'cantidad': openapi.Schema(type=openapi.TYPE_INTEGER),
                'motivo': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def ajustar_stock(self, request, pk=None):
        producto = self.get_object()
        cantidad = request.data.get('cantidad')
        motivo = request.data.get('motivo')
        
        if not cantidad:
            return Response(
                {'error': 'Se requiere la cantidad'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        producto.cantidad_stock += int(cantidad)
        producto.save()
        
        return Response({
            'mensaje': 'Stock actualizado correctamente',
            'nuevo_stock': producto.cantidad_stock
        })

class PedidoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Pedido.objects.all()
    
    @swagger_auto_schema(
        operation_description="Obtener estadísticas de pedidos",
        responses={200: openapi.Response('Estadísticas de pedidos')}
    )
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        hoy = timezone.now()
        mes_pasado = hoy - timedelta(days=30)
        
        stats = {
            'total_pedidos': self.get_queryset().count(),
            'pedidos_mes': self.get_queryset().filter(
                fecha_pedido__gte=mes_pasado
            ).count(),
            'monto_total_mes': self.get_queryset().filter(
                fecha_pedido__gte=mes_pasado
            ).aggregate(total=Sum('total'))['total'],
            'estado_pedidos': self.get_queryset().values('estado').annotate(
                total=Count('id')
            )
        }
        
        return Response(stats)

class RutaEntregaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RutaEntrega.objects.all()
    
    @swagger_auto_schema(
        operation_description="Optimizar rutas de entrega",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'fecha': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                'vehiculo_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        )
    )
    @action(detail=False, methods=['post'])
    def optimizar(self, request):
        fecha = request.data.get('fecha')
        vehiculo_id = request.data.get('vehiculo_id')
        
        # Aquí iría la lógica de optimización de rutas
        # Utilizando algoritmos como el del viajante (TSP)
        
        return Response({
            'mensaje': 'Ruta optimizada correctamente',
            'rutas': []  # Aquí irían las rutas optimizadas
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    operation_description="Obtener dashboard analítico",
    responses={200: openapi.Response('Dashboard analítico')}
)
def dashboard_analitico(request):
    hoy = timezone.now()
    mes_pasado = hoy - timedelta(days=30)
    
    # Ventas
    ventas_stats = Pedido.objects.filter(
        fecha_pedido__gte=mes_pasado
    ).aggregate(
        total_ventas=Sum('total'),
        promedio_venta=Avg('total'),
        total_pedidos=Count('id')
    )
    
    # Productos
    productos_stats = {
        'total_productos': Producto.objects.count(),
        'productos_activos': Producto.objects.filter(activo=True).count(),
        'productos_stock_bajo': Producto.objects.filter(cantidad_stock__lte=10).count()
    }
    
    # KPIs
    kpis = RegistroKPI.objects.filter(
        fecha__gte=mes_pasado
    ).select_related('indicador')
    
    return Response({
        'ventas': ventas_stats,
        'productos': productos_stats,
        'kpis': [
            {
                'nombre': kpi.indicador.nombre,
                'valor': float(kpi.valor),
                'estado': kpi.estado()
            }
            for kpi in kpis
        ]
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    operation_description="Obtener predicciones de demanda",
    manual_parameters=[
        openapi.Parameter(
            'producto_id',
            openapi.IN_QUERY,
            description="ID del producto",
            type=openapi.TYPE_INTEGER
        )
    ]
)
def predicciones_demanda(request):
    producto_id = request.query_params.get('producto_id')
    predicciones = PrediccionDemanda.objects.all()
    
    if producto_id:
        predicciones = predicciones.filter(producto_id=producto_id)
    
    return Response([
        {
            'producto': p.producto.nombre,
            'demanda_predicha': float(p.demanda_predicha),
            'precision': float(p.precision_modelo),
            'fecha_inicio': p.fecha_inicio,
            'fecha_fin': p.fecha_fin
        }
        for p in predicciones
    ])