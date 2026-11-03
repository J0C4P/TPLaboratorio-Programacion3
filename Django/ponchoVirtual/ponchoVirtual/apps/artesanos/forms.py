from django import forms
from .models import Artesano, Emprendimiento, Stand


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
        fields = ['nombre_artesano', 'apellido', 'dni', 'correo', 'telefono', 'localidad', 'provincia']

        widgets = {
            'nombre_artesano': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-control'}),
            }


class EmprendimientoForm(forms.ModelForm):
    class Meta:
        model = Emprendimiento
        fields = ['nombre_emprendimiento', 'descripcion', 'trayectoria', 'observaciones', 'cantidad_productos']

        widgets = {
            'nombre_emprendimiento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Manos Catamarqueñas'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'rows': 3, 'placeholder':'Breve descripción del emprendimiento'}),
            'trayectoria': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder':'Años de experiencia o historia...'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder':'Observaciones adicionales (opcional)'}),
            'cantidad_productos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 10'})
        }


class ArtesanoModificarForm(forms.ModelForm):
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
        fields = ['correo', 'telefono', 'localidad', 'provincia']

        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-control'}),
        }


class EmprendimientoModificarForm(forms.ModelForm):
    class Meta:
        model = Emprendimiento
        fields = ['descripcion', 'trayectoria', 'observaciones', 'cantidad_productos']

        widgets = {
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'rows': 3}),
            'trayectoria': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'cantidad_productos': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class StandForm(forms.ModelForm):
    zonas = [('', '-- Seleccione una Zona --'), ("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]

    zona = forms.ChoiceField(choices=zonas)

    class Meta:
        model = Stand
        fields = ('numero', 'zona')

        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'zona': forms.Select(attrs={'class': 'form-control'})
        }
