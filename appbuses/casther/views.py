from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from .models import Empleado
from .forms import EmpleadoForm


def index_view(request):
    return render (request, 'index.html', {})
def login_view(request):
    return render (request, 'login.html', {})
def password_view(request):
    return render (request, 'password.html', {})
def inventory_view(request):
    return render(request, 'inventory.html', {})
def works_view(request):
    return render(request, 'works.html', {})
def reports_view(request):
    return render(request, 'reports.html', {})
def employees_view(request):
    return render(request,'employees.html', {})
