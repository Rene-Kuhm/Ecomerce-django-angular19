from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Proveedor

@login_required
def index(request):
    search_query = request.GET.get('search', '')
    estado_filter = request.GET.get('estado')
    
    proveedores = Proveedor.objects.all()
    
    if search_query:
        proveedores = proveedores.filter(
            Q(nombre__icontains=search_query) |
            Q(rut__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(contacto__icontains=search_query)
        )
        
    if estado_filter:
        proveedores = proveedores.filter(activo=(estado_filter == 'activo'))
    
    context = {
        'proveedores': proveedores,
        'search_query': search_query,
        'estado_filter': estado_filter
    }
    return render(request, 'proveedores/index.html', context)

@login_required
def proveedor_crear(request):
    if request.method == 'POST':
        try:
            proveedor = Proveedor.objects.create(
                nombre=request.POST.get('nombre'),
                rut=request.POST.get('rut'),
                contacto=request.POST.get('contacto'),
                email=request.POST.get('email'),
                telefono=request.POST.get('telefono'),
                direccion=request.POST.get('direccion'),
                notas=request.POST.get('notas'),
                activo=True
            )
            messages.success(request, 'Proveedor creado exitosamente.')
            return redirect('proveedores')
        except Exception as e:
            messages.error(request, 'Error al crear el proveedor. Verifique que el RUT y email no estén duplicados.')
            return render(request, 'proveedores/proveedor_form.html', {
                'action': 'Crear',
                'proveedor': request.POST
            })
    
    return render(request, 'proveedores/proveedor_form.html', {'action': 'Crear'})

@login_required
def proveedor_editar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        try:
            proveedor.nombre = request.POST.get('nombre')
            proveedor.rut = request.POST.get('rut')
            proveedor.contacto = request.POST.get('contacto')
            proveedor.email = request.POST.get('email')
            proveedor.telefono = request.POST.get('telefono')
            proveedor.direccion = request.POST.get('direccion')
            proveedor.notas = request.POST.get('notas')
            proveedor.save()
            
            messages.success(request, 'Proveedor actualizado exitosamente.')
            return redirect('proveedores')
        except Exception as e:
            messages.error(request, 'Error al actualizar el proveedor. Verifique que el RUT y email no estén duplicados.')
    
    return render(request, 'proveedores/proveedor_form.html', {
        'proveedor': proveedor,
        'action': 'Editar'
    })

@login_required
def proveedor_eliminar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        proveedor.activo = False
        proveedor.save()
        messages.success(request, 'Proveedor desactivado exitosamente.')
        return redirect('proveedores')
    
    return render(request, 'proveedores/proveedor_confirmar_eliminar.html', {
        'proveedor': proveedor
    })

@login_required
def proveedor_activar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        proveedor.activo = True
        proveedor.save()
        messages.success(request, 'Proveedor activado exitosamente.')
    
    return redirect('proveedores')
