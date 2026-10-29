from django.contrib.auth.forms import UserCreationForm
from django import forms
from ponchoVirtual.apps.artesanos.models import Stand
from .models import Usuario


class UsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('documento_identidad', )


class StandForm(forms.ModelForm):
    class Meta:
        model = Stand
        fields = ('numero', 'zona')
