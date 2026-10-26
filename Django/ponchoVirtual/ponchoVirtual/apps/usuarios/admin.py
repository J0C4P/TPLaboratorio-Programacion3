from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


#configuracion con filtros para que el admin pueda aprobar rapido
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Columnas que se ven en la tabla principal
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    # Filtro lateral para ver rapido los "Inactivos" (solicitudes pendientes)
    list_filter = ('is_active', 'is_staff', 'groups')
    # Buscador por nombre o dni
    search_fields = ('username', 'email', 'first_name', 'last_name', 'documento_identidad')
    ordering = ('username',)

