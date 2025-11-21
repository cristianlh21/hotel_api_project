# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Campos a mostrar en la lista de usuarios
    list_display = UserAdmin.list_display + ('rol', 'legajo_id',)
    
    # Campos para editar en el formulario
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rol', 'legajo_id')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
