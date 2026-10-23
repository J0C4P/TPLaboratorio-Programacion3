from django import forms
from .models import Artesano, Emprendimiento


class ArtesanoForm(forms.ModelForm):
    provincias_arg = [
        ('', '-- Seleccione su provincia --'),
        ('Buenos Aires', 'Buenos Aires'),
        ('Catamarca', 'Catamarca'),
        ('Córdoba', 'Córdoba'),
        ('Mendoza', 'Mendoza'),
        ('Santa Fe', 'Santa Fe'),
        ('Tucumán', 'Tucumán'),
        ('Entre Ríos', 'Entre Ríos'),
        ('Salta', 'Salta'),
    ]

    provincia = forms.ChoiceField(choices=provincias_arg)

    class Meta:
        model = Artesano
        fields = ['nombre', 'apellido', 'dni', 'correo', 'telefono', 'localidad', 'provincia']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-control'}),
            }


class EmprendimientoForm(forms.ModelForm):
    pabellones = [('Pabellon A', 'Pabellon A'), ('Pabellon B', 'Pabellon B'), ('Pabellon C', 'Pabellon C'), ('Pabellon D', 'Pabellon D'),]

    ubicacion = forms.ChoiceField(choices=pabellones)

    class Meta:
        model = Emprendimiento
        fields = ['nombre', 'descripcion', 'trayectoria', 'observaciones', 'cantidad_productos', 'ubicacion']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Manos Catamarqueñas'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'rows': 3, 'placeholder':'Breve descripción del emprendimiento'}),
            'trayectoria': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder':'Años de experiencia o historia...'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder':'Observaciones adicionales (opcional)'}),
            'cantidad_productos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 10'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
        }
