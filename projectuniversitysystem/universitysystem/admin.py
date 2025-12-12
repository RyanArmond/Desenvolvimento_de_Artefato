from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Aluno, Instituicao, Curso, Disciplina, Turma,
    Historico, ItemHistorico, RestauranteUniversitario,
    CalendarioAcademico, Compromisso
)

# Register your admins here.
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    list_display = ['username', 'email', 'cpf',  'matricula', 'funcao']

    # Campos que aparecem ao editar um usuário
    fieldsets = UserAdmin.fieldsets + (
        ('Campos adicionais', {'fields': ('cpf', 'matricula', 'funcao', 'foto')}),
    )

    list_filter = ('funcao', 'is_staff', 'is_superuser')

    # Campos que aparecem ao criar um usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos adicionais', {'fields': ('first_name', 'last_name', 'email', 'cpf', 'matricula', 'funcao', 'foto')}),
    )


@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'cnpj')
    search_fields = ('nome', 'sigla', 'cnpj')


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'instituicao', 'horarios')
    list_filter = ('instituicao',)
    search_fields = ('nome', 'sigla')


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'curso')
    list_filter = ('curso',)
    search_fields = ('nome', 'codigo')


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('status', 'curso')
    list_filter = ('status', 'curso')
    search_fields = ('matricula', 'cpf')
    autocomplete_fields = ['user'] 


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numero', 'periodo', 'status')
    list_filter = ('status', 'periodo')
    search_fields = ('nome',)


class ItemHistoricoInline(admin.TabularInline):
    model = ItemHistorico
    extra = 1


@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'data_emissao')
    search_fields = ('aluno__nome_completo', 'aluno__matricula')
    inlines = [ItemHistoricoInline] 


@admin.register(ItemHistorico)
class ItemHistoricoAdmin(admin.ModelAdmin):
    list_display = ('historico', 'disciplina', 'media', 'periodo_cursado')
    list_filter = ('disciplina', 'periodo_cursado')
    search_fields = ('historico__aluno__nome_completo',)


@admin.register(RestauranteUniversitario)
class RestauranteUniversitarioAdmin(admin.ModelAdmin):
    list_display = ('instituicao', 'horario_funcionamento')
    search_fields = ('instituicao__nome',)


class CompromissoInline(admin.TabularInline):
    model = Compromisso
    extra = 1


@admin.register(CalendarioAcademico)
class CalendarioAcademicoAdmin(admin.ModelAdmin):
    list_display = ('instituicao', 'data_referencia', 'descricao')
    list_filter = ('instituicao',)
    inlines = [CompromissoInline]


@admin.register(Compromisso)
class CompromissoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'tipo', 'calendario_academico')
    list_filter = ('tipo', 'data')
    search_fields = ('titulo',)