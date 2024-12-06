from django import forms # type: ignore
from .models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'cargo']