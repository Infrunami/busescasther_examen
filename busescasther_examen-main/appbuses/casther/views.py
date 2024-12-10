from sqlite3 import IntegrityError
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from casther.models import Empleado, Producto, Vehiculo, Informe
from casther.forms import EmpleadoForm, ProductoForm, VehiculoForm, InformeForm, LoginForm
import logging
from django.db.models import Q

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Credenciales inválidas')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def empleados(request):
    empleados_list = Empleado.objects.all()
    return render(request, 'empleados.html', {'empleados': empleados_list})

@login_required
def agregar_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados/agregar_empleado.html', {'form': form})

@login_required
def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'empleados/editar_empleado.html', {'form': form, 'empleado': empleado})

@login_required
def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('empleados')
    return render(request, 'empleados/eliminar_empleado.html', {'empleado': empleado})

@login_required
def inventario(request):
    productos_list = Producto.objects.all()
    return render(request, 'inventario.html', {'productos': productos_list})

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario/inventario')
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/editar_producto.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('inventario')
    return render(request, 'inventario/eliminar_producto.html', {'producto': producto})

@login_required
def trabajos(request):
    vehiculos_list = Vehiculo.objects.filter(informe__isnull=True)
    return render(request, 'trabajos.html', {'vehiculos': vehiculos_list})

@login_required
@transaction.atomic
def generar_informe(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    
    if request.method == 'POST':
        form = InformeForm(request.POST)
        if form.is_valid():
            try:
                # Crear y guardar el informe
                informe = form.save(commit=False)
                informe.vehiculo = vehiculo
                informe.save()
                
                # Obtener el ID antes de eliminar
                vehiculo_id = vehiculo.id
                vehiculo_id.delete()
                
                return redirect('informes')
            except Exception as e:
                # Loguear el error para debugging
                print(f"Error al eliminar vehículo: {e}")
                return redirect('informes')
    else:
        form = InformeForm()
    
    return render(request, 'informes/generar_informe.html', {'form': form, 'vehiculo': vehiculo})

@login_required
def informes(request):
    query = request.GET.get('q', '')
    if query:
        # Búsqueda por patente o modelo
        informes = Informe.objects.filter(
            Q(vehiculo__patente__icontains=query) |  # búsqueda en patente
            Q(vehiculo__modelo__icontains=query)     # búsqueda en modelo
        ).select_related('vehiculo').order_by('-fecha')
    else:
        # Si no hay búsqueda, mostrar todos los informes
        informes = Informe.objects.all().select_related('vehiculo').order_by('-fecha')
    
    context = {
        'informes': informes,
        'query': query,
    }
    return render(request, 'informes.html', context)

@login_required
def visualizar_informe(request, informe_id):
    informe = get_object_or_404(Informe, id=informe_id)
    return render(request, 'informes/visualizar_informe.html', {'informe': informe})

def index(request):
    return render(request, 'index.html')

def empleados(request):
    empleados_list = Empleado.objects.all().order_by('apellido', 'nombre')
    paginator = Paginator(empleados_list, 10)  # 10 empleados por página
    page_number = request.GET.get('page')
    empleados = paginator.get_page(page_number)
    return render(request, 'empleados.html', {'empleados': empleados})

def inventario(request):
    productos_list = Producto.objects.all().order_by('nombre')
    paginator = Paginator(productos_list, 10)  # 10 productos por página
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    return render(request, 'inventario.html', {'productos': productos})

def trabajos(request):
    vehiculos_list = Vehiculo.objects.all().order_by('-id')  # Ordenados por el más reciente
    paginator = Paginator(vehiculos_list, 10)  # 10 vehículos por página
    page_number = request.GET.get('page')
    vehiculos = paginator.get_page(page_number)
    return render(request, 'trabajos.html', {'vehiculos': vehiculos})

def informes(request):
    informes_list = Informe.objects.all().order_by('-fecha_creacion')
    paginator = Paginator(informes_list, 10)  # 10 informes por página
    page_number = request.GET.get('page')
    informes = paginator.get_page(page_number)
    return render(request, 'informes.html', {'informes': informes})

@transaction.atomic
def agregar_empleado(request):
    if request.method == 'POST':
        try:
            Empleado.objects.create(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                area=request.POST['area'],
                cargo=request.POST['cargo'],
                fecha_nacimiento=request.POST['fecha_nacimiento']
            )
            messages.success(request, 'Empleado agregado exitosamente.')
            return redirect('empleados')
        except IntegrityError:
            messages.error(request, 'Error al agregar el empleado. Por favor, intente de nuevo.')
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    return render(request, 'empleados/agregar_empleado.html')

@transaction.atomic
def agregar_producto(request):
    if request.method == 'POST':
        try:
            Producto.objects.create(
                nombre=request.POST['nombre'],
                categoria=request.POST['categoria'],
                precio=request.POST['precio'],
                cantidad=request.POST['cantidad']
            )
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect('inventario')
        except IntegrityError:
            messages.error(request, 'Error al agregar el producto. Por favor, intente de nuevo.')
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    return render(request, 'inventario/agregar_producto.html')

@transaction.atomic
def agregar_vehiculo(request):
    if request.method == 'POST':
        try:
            Vehiculo.objects.create(
                modelo=request.POST['modelo'],
                año=request.POST['año'],
                patente=request.POST['patente'],
                problema=request.POST['problema']
            )
            messages.success(request, 'Vehículo agregado exitosamente.')
            return redirect('trabajos')
        except IntegrityError:
            messages.error(request, 'Error al agregar el vehículo. Por favor, intente de nuevo.')
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    return render(request, 'trabajos/agregar_vehiculo.html')

@transaction.atomic
def generar_informe(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    if request.method == 'POST':
        try:
            Informe.objects.create(
                vehiculo=vehiculo,
                diagnostico=request.POST['diagnostico'],
                reparacion=request.POST['reparacion'],
                comentarios=request.POST['comentarios']
            )
            messages.success(request, 'Informe generado exitosamente.')
            return redirect('informes')
        except IntegrityError:
            messages.error(request, 'Error al generar el informe. Por favor, intente de nuevo.')
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    return render(request, 'trabajos/generar_informe.html', {'vehiculo': vehiculo})

def visualizar_informe(request, informe_id):
    informe = get_object_or_404(Informe.objects.select_related('vehiculo'), id=informe_id)
    return render(request, 'informes/visualizar_informe.html', {'informe': informe})