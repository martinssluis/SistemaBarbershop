from django.urls import path
from . import views

urlpatterns = [
    path('', views.entrada_cliente, name='entrada_cliente'),
    path('novo_agendamento/<int:cliente_id>/', views.novo_agendamento, name='novo_agendamento'),
    path('selecionar_funcionario/<int:cliente_id>/<int:servico_id>/', views.selecionar_funcionario, name='selecionar_funcionario'),
    path('selecionar_horario/<int:cliente_id>/<int:servico_id>/', views.selecionar_horario, name='selecionar_horario'),
    path('confirmar_agendamento/<int:cliente_id>/<int:servico_id>/<int:horario_id>/', views.confirmar_agendamento, name='confirmar_agendamento'),
    path('cadastro_cliente/<str:telefone>/', views.cadastro_cliente, name='cadastro_cliente'),
]
