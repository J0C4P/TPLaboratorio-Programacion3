from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    categorias_predefinidas = [
        ('', '-- Seleccione la indicada --'),
        ('Textil', 'Textil'),
        ('Ceramica', 'Ceramica'),
        ('Orfebreria y joyeria', 'Orfebreria y joyeria'),
        ('Gastronomia regional', 'Gastronomia regional'),
    ]

    categoria = forms.ChoiceField(choices=categorias_predefinidas)

    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'imagen', 'descripcion', 'precio', 'stock']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '"Dulce de Cayote"'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '$12.500'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dulce en hebras cocinado en paila de cobre sin conservantes'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '"5 Unidades"'}),
        }


class ProductoModificarForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'imagen', 'precio', 'stock', 'activo']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }
