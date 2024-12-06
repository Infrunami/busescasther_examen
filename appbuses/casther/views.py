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

##vistas para empleado

# Lista de emplead
def employees_view(request):
    # Obtener todos los empleados
    empleados = Empleado.objects.all()

    # Manejar el formulario de creación
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees_view')
    else:
        form = EmpleadoForm()

    context = {
        'empleados': empleados,
        'form': form,
    }
    return render(request, 'employees.html', context)

def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        print(f"Eliminando empleado: {empleado.nombre} {empleado.apellido}")  # Depuración
        empleado.delete()
        return redirect('employees_view')
    return render(request, 'delete_employee.html', {'empleado': empleado})

