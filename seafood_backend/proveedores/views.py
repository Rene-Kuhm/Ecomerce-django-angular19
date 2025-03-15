from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {
        'titulo': '',
    }
    return render(request, 'proveedores/index.html', context)
