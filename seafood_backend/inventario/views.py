from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto
from django.db.models import Q

@login_required
def index(request):
    search_query = request.GET.get('search', '')
    productos = Producto.objects.all()
    
    if search_query:
        productos = productos.filter(
            Q(nombre__icontains=search_query) |
            Q(descripcion__icontains=search_query)
        )
    
    context = {
        'productos': productos,
        'search_query': search_query,
    }
    return render(request, 'inventario/index.html', context)

@login_required
def producto_crear(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        imagen = request.FILES.get('imagen')
        
        producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            cantidad_stock=stock,
            imagen=imagen
        )
        messages.success(request, 'Producto creado exitosamente.')
        return redirect('inventario')
        
    return render(request, 'inventario/producto_form.html', {'action': 'Crear'})

@login_required
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        producto.cantidad_stock = request.POST.get('stock')
        
        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']
            
        producto.save()
        messages.success(request, 'Producto actualizado exitosamente.')
        return redirect('inventario')
        
    return render(request, 'inventario/producto_form.html', {
        'producto': producto,
        'action': 'Editar'
    })

@login_required
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('inventario')
    
    return render(request, 'inventario/producto_confirmar_eliminar.html', {
        'producto': producto
    })

@login_required
def ajustar_stock(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 0))
        operacion = request.POST.get('operacion')
        
        if operacion == 'sumar':
            producto.cantidad_stock += cantidad
        elif operacion == 'restar':
            if producto.cantidad_stock >= cantidad:
                producto.cantidad_stock -= cantidad
            else:
                messages.error(request, 'No hay suficiente stock para realizar esta operación.')
                return redirect('inventario')
                
        producto.save()
        messages.success(request, f'Stock actualizado exitosamente. Nuevo stock: {producto.cantidad_stock}')
        return redirect('inventario')
        
    return render(request, 'inventario/ajustar_stock.html', {'producto': producto})
