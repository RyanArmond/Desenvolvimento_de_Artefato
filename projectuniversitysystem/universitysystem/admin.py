from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Aluno

# Register your admins here.
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['username', 'email', 'cpf', 'funcao']

    # Campos que aparecem ao editar um usuário
    fieldsets = UserAdmin.fieldsets + (
        ('Campos adicionais', {'fields': ('cpf', 'funcao')}),
    )

    # Campos que aparecem ao criar um usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos adicionais', {'fields': ('first_name', 'last_name', 'email', 'cpf', 'funcao')}),
    )

admin.site.register(Usuario, UsuarioAdmin)



