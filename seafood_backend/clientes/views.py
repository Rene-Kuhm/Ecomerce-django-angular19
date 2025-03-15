from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Cliente

@login_required
def index(request):
    search_query = request.GET.get('search', '')
    estado_filter = request.GET.get('estado')
    
    clientes = Cliente.objects.all()
    
    if search_query:
        clientes = clientes.filter(
            Q(nombre__icontains=search_query) |
            Q(rut__icontains=search_query) |
            Q(email__icontains=search_query)
        )
        
    if estado_filter:
        clientes = clientes.filter(activo=(estado_filter == 'activo'))
    
    context = {
        'clientes': clientes,
        'search_query': search_query,
        'estado_filter': estado_filter
    }
    return render(request, 'clientes/index.html', context)

@login_required
def cliente_crear(request):
    if request.method == 'POST':
        try:
            cliente = Cliente.objects.create(
                nombre=request.POST.get('nombre'),
                rut=request.POST.get('rut'),
                email=request.POST.get('email'),
                telefono=request.POST.get('telefono'),
                direccion=request.POST.get('direccion'),
                activo=True
            )
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('clientes')
        except Exception as e:
            messages.error(request, 'Error al crear el cliente. Verifique que el RUT y email no estén duplicados.')
            return render(request, 'clientes/cliente_form.html', {
                'action': 'Crear',
                'cliente': request.POST
            })
    
    return render(request, 'clientes/cliente_form.html', {'action': 'Crear'})

@login_required
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        try:
            cliente.nombre = request.POST.get('nombre')
            cliente.rut = request.POST.get('rut')
            cliente.email = request.POST.get('email')
            cliente.telefono = request.POST.get('telefono')
            cliente.direccion = request.POST.get('direccion')
            cliente.save()
            
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('clientes')
        except Exception as e:
            messages.error(request, 'Error al actualizar el cliente. Verifique que el RUT y email no estén duplicados.')
    
    return render(request, 'clientes/cliente_form.html', {
        'cliente': cliente,
        'action': 'Editar'
    })

@login_required
def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        cliente.activo = False
        cliente.save()
        messages.success(request, 'Cliente desactivado exitosamente.')
        return redirect('clientes')
    
    return render(request, 'clientes/cliente_confirmar_eliminar.html', {
        'cliente': cliente
    })

@login_required
def cliente_activar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        cliente.activo = True
        cliente.save()
        messages.success(request, 'Cliente activado exitosamente.')
    
    return redirect('clientes')
