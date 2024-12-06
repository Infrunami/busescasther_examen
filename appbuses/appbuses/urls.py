from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from casther import views

urlpatterns = [
    #vistas base
    path('', views.login_view),
    path('index/', views.index_view),
    path('password/', views.password_view),
    path('admin/', admin.site.urls),

    #vistas funcionales
    path('employees/', views.employees_view),
    path('inventory/', views.inventory_view),
    path('works/', views.works_view),
    path('reports/', views.reports_view),
]