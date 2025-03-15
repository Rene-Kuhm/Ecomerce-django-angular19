from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from datetime import datetime, timedelta
from inventario.models import Producto
from pedidos.models import Pedido, DetallePedido
from clientes.models import Cliente

@login_required
def index(request):
    # Obtener fecha actual y de ayer
    hoy = timezone.now().date()
    ayer = hoy - timedelta(days=1)
    
    # Ventas del día y cambio porcentual
    ventas_hoy = Pedido.objects.filter(
        fecha_pedido__date=hoy
    ).aggregate(
        total=Sum('total', default=0)
    )['total']
    
    ventas_ayer = Pedido.objects.filter(
        fecha_pedido__date=ayer
    ).aggregate(
        total=Sum('total', default=0)
    )['total']
    
    if ventas_ayer > 0:
        sales_change = ((ventas_hoy - ventas_ayer) / ventas_ayer) * 100
    else:
        sales_change = 0
    
    # Estadísticas de pedidos
    pending_orders = Pedido.objects.filter(estado='pendiente').count()
    processing_orders = Pedido.objects.filter(estado='en_proceso').count()
    
    # Productos con stock bajo y totales
    low_stock_threshold = 10  # Definir umbral de stock bajo
    low_stock_products = Producto.objects.filter(stock__lte=low_stock_threshold).count()
    total_products = Producto.objects.count()
    active_products = Producto.objects.filter(activo=True).count()
    
    # Estadísticas de clientes
    total_customers = Cliente.objects.count()
    active_customers = Cliente.objects.filter(activo=True).count()
    
    # Ventas mensuales para el gráfico
    monthly_sales = list(Pedido.objects.annotate(
        month=TruncMonth('fecha_pedido')
    ).values('month').annotate(
        total=Sum('total')
    ).order_by('month').values('month', 'total'))
    
    # Formatear datos para el gráfico
    for item in monthly_sales:
        item['month'] = item['month'].strftime('%B %Y')
        item['total'] = float(item['total'])
    
    # Productos más vendidos
    top_products = DetallePedido.objects.values(
        'producto__nombre'
    ).annotate(
        ventas_totales=Sum(F('cantidad') * F('precio_unitario'))
    ).order_by('-ventas_totales')[:5]
    
    # Formatear productos más vendidos
    top_products = [
        {'name': item['producto__nombre'], 'sales': float(item['ventas_totales'])}
        for item in top_products
    ]
    
    context = {
        'daily_sales': ventas_hoy,
        'sales_change': round(sales_change, 1),
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'low_stock_products': low_stock_products,
        'total_products': total_products,
        'active_products': active_products,
        'total_customers': total_customers,
        'active_customers': active_customers,
        'monthly_sales': monthly_sales,
        'top_products': top_products,
    }
    
    return render(request, 'dashboard/index.html', context)
