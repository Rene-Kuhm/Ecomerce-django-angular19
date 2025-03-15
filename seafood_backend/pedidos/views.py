from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Pedido, DetallePedido
from inventario.models import Producto
from clientes.models import Cliente
from django.db.models import Q

@login_required
def index(request):
    search_query = request.GET.get('search', '')
    estado_filter = request.GET.get('estado', '')
    
    pedidos = Pedido.objects.all()
    
    if search_query:
        pedidos = pedidos.filter(
            Q(cliente__nombre__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    
    if estado_filter:
        pedidos = pedidos.filter(estado=estado_filter)
    
    context = {
        'pedidos': pedidos,
        'search_query': search_query,
        'estado_filter': estado_filter,
        'estados': Pedido.ESTADO_CHOICES,
    }
    return render(request, 'pedidos/index.html', context)

@login_required
def pedido_crear(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        notas = request.POST.get('notas', '')
        
        if not cliente_id or not productos:
            messages.error(request, 'Por favor complete todos los campos requeridos.')
            return redirect('pedido_crear')
        
        try:
            with transaction.atomic():
                # Crear el pedido
                cliente = Cliente.objects.get(id=cliente_id)
                pedido = Pedido.objects.create(
                    cliente=cliente,
                    notas=notas
                )
                
                # Agregar los productos al pedido
                for producto_id, cantidad in zip(productos, cantidades):
                    if cantidad and int(cantidad) > 0:
                        producto = Producto.objects.get(id=producto_id)
                        if producto.cantidad_stock < int(cantidad):
                            raise ValueError(f'Stock insuficiente para {producto.nombre}')
                        
                        # Crear detalle del pedido
                        DetallePedido.objects.create(
                            pedido=pedido,
                            producto=producto,
                            cantidad=int(cantidad),
                            precio_unitario=producto.precio
                        )
                        
                        # Actualizar stock
                        producto.cantidad_stock -= int(cantidad)
                        producto.save()
                
                pedido.actualizar_total()
                messages.success(request, 'Pedido creado exitosamente.')
                return redirect('pedido_detalle', pk=pedido.pk)
                
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('pedido_crear')
        except Exception as e:
            messages.error(request, 'Error al crear el pedido.')
            return redirect('pedido_crear')
    
    context = {
        'clientes': Cliente.objects.filter(activo=True),
        'productos': Producto.objects.filter(activo=True, cantidad_stock__gt=0)
    }
    return render(request, 'pedidos/pedido_form.html', context)

@login_required
def pedido_detalle(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'pedidos/pedido_detalle.html', {'pedido': pedido})

@login_required
def pedido_estado(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Pedido.ESTADO_CHOICES):
            pedido.estado = nuevo_estado
            pedido.save()
            messages.success(request, 'Estado del pedido actualizado exitosamente.')
        
    return redirect('pedido_detalle', pk=pedido.pk)

@login_required
def pedido_cancelar(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        if pedido.estado != 'cancelado':
            try:
                with transaction.atomic():
                    # Devolver productos al inventario
                    for detalle in pedido.detalles.all():
                        producto = detalle.producto
                        producto.cantidad_stock += detalle.cantidad
                        producto.save()
                    
                    pedido.estado = 'cancelado'
                    pedido.save()
                    messages.success(request, 'Pedido cancelado exitosamente.')
            except Exception as e:
                messages.error(request, 'Error al cancelar el pedido.')
        
    return redirect('pedido_detalle', pk=pedido.pk)
