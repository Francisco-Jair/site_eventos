from django.contrib import admin
from .models import Palestrantes, Minicursos, Usuarios
from django.http import HttpResponse
import xlwt

admin.site.register(Palestrantes)
admin.site.register(Minicursos)

def exportar_usuarios(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="inscritos.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('inscritos')

    titulos = ['Nome', 'CPF', 'E-mail', 'Instituição', 'Tipo de Usuário']
    
    for index, titulo in enumerate(titulos):
        ws.write(0, index, titulo)  

    for index, usuario in enumerate(queryset):
        i = index + 1
        ws.write(i, 0, usuario.nome)
        ws.write(i, 1, usuario.cpf)
        ws.write(i, 2, usuario.email)
        ws.write(i, 3, usuario.instituicao)
        ws.write(i, 4, usuario.tipo_usuario)

    wb.save(response)

    return response

exportar_usuarios.short_description = 'Exportar Usuários selecionados (planilha)'

class UsuariosAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email', 'instituicao']
    ordering = ['nome']
    actions = [exportar_usuarios]

admin.site.register(Usuarios, UsuariosAdmin)