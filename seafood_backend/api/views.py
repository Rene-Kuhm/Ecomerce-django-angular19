from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, "api/index.html")

def get_inventario(request):
    # Add your inventory logic here
    data = {"message": "Inventario endpoint"}
    return JsonResponse(data)

def get_pedidos(request):
    # Add your orders logic here
    data = {"message": "Pedidos endpoint"}
    return JsonResponse(data)

def get_clientes(request):
    # Add your clients logic here
    data = {"message": "Clientes endpoint"}
    return JsonResponse(data)

def get_proveedores(request):
    # Add your suppliers logic here
    data = {"message": "Proveedores endpoint"}
    return JsonResponse(data)

def get_informes(request):
    # Add your reports logic here
    data = {"message": "Informes endpoint"}
    return JsonResponse(data)