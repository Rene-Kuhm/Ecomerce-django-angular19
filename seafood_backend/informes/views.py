from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg, F, ExpressionWrapper, DecimalField
from .models import Informe
from pedidos.models import Pedido, DetallePedido
from inventario.models import Producto
from clientes.models import Cliente
from proveedores.models import Proveedor
from datetime import datetime, timedelta
from django.utils import timezone

@login_required
def index(request):
    informes = Informe.objects.all()
    context = {
        'informes': informes,
        'titulo': 'Informes y Estadísticas'
    }
    return render(request, 'informes/index.html', context)

@login_required
def generar_informe(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        titulo = request.POST.get('titulo')
        
        if tipo == 'ventas':
            contenido = generar_informe_ventas()
        elif tipo == 'inventario':
            contenido = generar_informe_inventario()
        elif tipo == 'clientes':
            contenido = generar_informe_clientes()
        elif tipo == 'proveedores':
            contenido = generar_informe_proveedores()
        
        Informe.objects.create(
            titulo=titulo,
            tipo=tipo,
            creado_por=request.user,
            contenido=contenido
        )
        
        messages.success(request, 'Informe generado exitosamente.')
        return redirect('informes')
        
    return render(request, 'informes/generar_informe.html')

def generar_informe_ventas():
    ahora = timezone.now()
    hace_30_dias = ahora - timedelta(days=30)
    
    pedidos = Pedido.objects.filter(fecha_creacion__gte=hace_30_dias)
    
    return {
        'total_pedidos': pedidos.count(),
        'total_ventas': float(pedidos.aggregate(Sum('total'))['total__sum'] or 0),
        'promedio_venta': float(pedidos.aggregate(Avg('total'))['total__avg'] or 0),
        'productos_mas_vendidos': list(
            DetallePedido.objects.filter(pedido__in=pedidos)
            .values('producto__nombre')
            .annotate(total=Sum('cantidad'))
            .order_by('-total')[:5]
        )
    }

def generar_informe_inventario():
    return {
        'total_productos': Producto.objects.count(),
        'valor_total_inventario': float(Producto.objects.aggregate(
            total=Sum(F('precio') * F('stock')))['total'] or 0),
        'productos_sin_stock': list(
            Producto.objects.filter(stock=0)
            .values('nombre', 'precio')
        ),
        'productos_stock_bajo': list(
            Producto.objects.filter(stock__lt=10)
            .values('nombre', 'stock')
            .order_by('stock')
        )
    }

def generar_informe_clientes():
    return {
        'total_clientes': Cliente.objects.count(),
        'clientes_activos': Cliente.objects.filter(activo=True).count(),
        'clientes_inactivos': Cliente.objects.filter(activo=False).count(),
        'mejores_clientes': list(
            Pedido.objects.values('cliente__nombre')
            .annotate(total_pedidos=Count('id'), total_gastado=Sum('total'))
            .order_by('-total_gastado')[:5]
        )
    }

def generar_informe_proveedores():
    return {
        'total_proveedores': Proveedor.objects.count(),
        'proveedores_activos': Proveedor.objects.filter(activo=True).count(),
        'proveedores_inactivos': Proveedor.objects.filter(activo=False).count()
    }
