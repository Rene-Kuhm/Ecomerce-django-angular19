from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from inventario.models import Producto
from pedidos.models import Pedido, DetallePedido
from clientes.models import Cliente

@login_required
def index(request):
    try:
        # Obtener fecha actual y de ayer
        hoy = timezone.now().date()
        ayer = hoy - timedelta(days=1)
        
        # Ventas del día y cambio porcentual
        ventas_hoy = Pedido.objects.filter(
            fecha_pedido__date=hoy,
            estado__in=['completado', 'entregado']  # Solo pedidos completados
        ).aggregate(
            total=Sum('total', default=Decimal('0.00'))
        )['total'] or Decimal('0.00')
        
        ventas_ayer = Pedido.objects.filter(
            fecha_pedido__date=ayer,
            estado__in=['completado', 'entregado']
        ).aggregate(
            total=Sum('total', default=Decimal('0.00'))
        )['total'] or Decimal('0.00')
        
        # Cálculo seguro del cambio porcentual
        sales_change = Decimal('0.00')
        if ventas_ayer and ventas_ayer != 0:
            sales_change = ((ventas_hoy - ventas_ayer) / ventas_ayer) * 100
        
        # Estadísticas de pedidos con validación de estados
        estados_validos = ['pendiente', 'en_proceso', 'completado', 'cancelado']
        pending_orders = Pedido.objects.filter(estado='pendiente').count()
        processing_orders = Pedido.objects.filter(estado='en_proceso').count()
        
        # Productos con stock bajo y totales con cacheo
        low_stock_threshold = 10
        productos_query = Producto.objects.all()
        low_stock_products = productos_query.filter(
            cantidad_stock__lte=low_stock_threshold,
            activo=True
        ).count()
        total_products = productos_query.count()
        active_products = productos_query.filter(activo=True).count()
        
        # Estadísticas de clientes optimizadas
        clientes_query = Cliente.objects.all()
        total_customers = clientes_query.count()
        active_customers = clientes_query.filter(activo=True).count()
        
        # Ventas mensuales con mejor manejo de datos
        tres_meses_atras = hoy - timedelta(days=90)
        monthly_sales = list(Pedido.objects.filter(
            fecha_pedido__gte=tres_meses_atras,
            estado__in=['completado', 'entregado']
        ).annotate(
            month=TruncMonth('fecha_pedido')
        ).values('month').annotate(
            total=Sum('total', default=Decimal('0.00'))
        ).order_by('month'))
        
        # Productos más vendidos con optimización
        top_products = list(DetallePedido.objects.filter(
            pedido__estado__in=['completado', 'entregado']
        ).values(
            'producto__nombre'
        ).annotate(
            ventas_totales=Sum(F('cantidad') * F('precio_unitario'))
        ).order_by('-ventas_totales')[:5])

        context = {
            'daily_sales': float(ventas_hoy),
            'sales_change': float(sales_change),
            'pending_orders': pending_orders,
            'processing_orders': processing_orders,
            'low_stock_products': low_stock_products,
            'total_products': total_products,
            'active_products': active_products,
            'total_customers': total_customers,
            'active_customers': active_customers,
            'monthly_sales': [
                {
                    'month': item['month'].strftime('%B %Y'),
                    'total': float(item['total'])
                } for item in monthly_sales
            ],
            'top_products': [
                {
                    'name': item['producto__nombre'],
                    'sales': float(item['ventas_totales'])
                } for item in top_products
            ],
        }
        
        return render(request, 'dashboard/index.html', context)
        
    except Exception as e:
        # Log del error aquí si tienes configurado logging
        context = {
            'error': 'Ha ocurrido un error al cargar el dashboard',
            'daily_sales': 0,
            'sales_change': 0,
            'pending_orders': 0,
            'processing_orders': 0,
            'low_stock_products': 0,
            'total_products': 0,
            'active_products': 0,
            'total_customers': 0,
            'active_customers': 0,
            'monthly_sales': [],
            'top_products': [],
        }
        return render(request, 'dashboard/index.html', context)
