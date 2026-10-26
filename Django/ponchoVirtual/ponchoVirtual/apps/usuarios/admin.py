from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ponchoVirtual.apps.usuarios.forms import UsuarioForm
from ponchoVirtual.apps.usuarios.models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    add_form = UsuarioForm

    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('documento_identidad',)}),)

    add_fieldsets = (None, {'fields': ('username', 'documento_identidad', 'password1', 'password2')})

    search_fields = ('email', 'documento_identidad', 'username',)


