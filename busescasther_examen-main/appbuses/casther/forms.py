from django import forms
from .models import Empleado, Producto, Vehiculo, Informe

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'area', 'cargo', 'fecha_nacimiento']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'cantidad']

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['modelo', 'año', 'patente', 'problema']

class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = ['diagnostico', 'reparacion', 'comentarios']