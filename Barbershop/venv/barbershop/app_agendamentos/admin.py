from django.contrib import admin
from .models import *

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'telefone', 'cortes_feitos')  
admin.site.register(Servico)
admin.site.register(Cliente)
admin.site.register(Funcionario, FuncionarioAdmin)  
admin.site.register(Disponibilidade)
admin.site.register(Agendamento)
