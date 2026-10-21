from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Usuario


class UsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('documento_identidad', )
