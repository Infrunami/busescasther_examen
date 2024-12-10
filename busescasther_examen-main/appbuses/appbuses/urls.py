from django.contrib import admin # type: ignore
from django.urls import path
from casther import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index, name='index'),
    path('empleados/', views.empleados, name='empleados'),
    path('empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleados/editar/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/agregar/', views.agregar_producto, name='agregar_producto'),
    path('inventario/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('inventario/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('trabajos/', views.trabajos, name='trabajos'),
    path('trabajos/agregar/', views.agregar_vehiculo, name='agregar_vehiculo'),
    path('trabajos/generar_informe/<int:vehiculo_id>/', views.generar_informe, name='generar_informe'),
    path('informes/', views.informes, name='informes'),
    path('informes/visualizar/<int:informe_id>/', views.visualizar_informe, name='visualizar_informe'),
]
