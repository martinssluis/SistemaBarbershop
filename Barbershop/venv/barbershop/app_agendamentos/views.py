from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, date
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *

def entrada_cliente(request):
    """
    Exibe a página inicial onde o cliente pode inserir seu telefone para buscar agendamentos existentes.
    """
    if request.method == 'POST':
        telefone = request.POST.get('telefone')
        try:
            cliente = Cliente.objects.get(telefone=telefone)
            agendamentos = Agendamento.objects.filter(cliente=cliente)
            return render(request, 'agendamento_cliente.html', {'cliente': cliente, 'agendamentos': agendamentos})
        except Cliente.DoesNotExist:
            # Se o cliente não for encontrado, redireciona para a página de cadastro
            return redirect('cadastro_cliente', telefone=telefone)
    return render(request, 'entrada_cliente.html')

def cadastro_cliente(request, telefone):
    """
    Página para cadastro de cliente, com base no telefone.
    """
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cliente = Cliente.objects.create(nome=nome, telefone=telefone)
        return redirect('entrada_cliente')
    return render(request, 'cadastro_cliente.html', {'telefone': telefone})

def novo_agendamento(request, cliente_id):
    """
    Página para o cliente escolher o serviço desejado para agendamento.
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)
    servicos = Servico.objects.all()

    if request.method == 'POST':
        servico_id = request.POST.get('servico')
        servico = get_object_or_404(Servico, id=servico_id)
        preferencia = request.POST.get('preferencia_funcionario')

        if preferencia == 'sim':
            return redirect('selecionar_funcionario', cliente_id=cliente.id, servico_id=servico.id)
        else:
            return redirect('selecionar_horario', cliente_id=cliente.id, servico_id=servico.id)

    return render(request, 'novo_agendamento.html', {'cliente': cliente, 'servicos': servicos})

def selecionar_funcionario(request, cliente_id, servico_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    servico = get_object_or_404(Servico, id=servico_id)
    funcionarios = Funcionario.objects.all()

    if request.method == 'POST':
        funcionario_id = request.POST.get('funcionario_id')
        if not funcionario_id:
            return render(request, 'selecionar_funcionario.html', {
                'cliente': cliente,
                'servico': servico,
                'funcionarios': funcionarios,
                'error': 'Por favor, selecione um funcionário.'
            })

        funcionario = get_object_or_404(Funcionario, id=funcionario_id)
        Disponibilidade.gerar_horarios(funcionario, datetime.now().date())
        
        return redirect(f'/selecionar_horario/{cliente_id}/{servico_id}/?funcionario_id={funcionario_id}')

    return render(request, 'selecionar_funcionario.html', {'cliente': cliente, 'servico': servico, 'funcionarios': funcionarios})



def selecionar_horario(request, cliente_id, servico_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    servico = get_object_or_404(Servico, id=servico_id)
    funcionario_id = request.GET.get('funcionario_id') or request.POST.get('funcionario_id')
    funcionario = get_object_or_404(Funcionario, id=funcionario_id)

    horarios = []

    if request.method == 'POST':
        if 'data' in request.POST:
            data = request.POST.get('data')
            if not data:
                return render(request, 'selecionar_horario.html', {
                    'cliente': cliente,
                    'servico': servico,
                    'error': 'Por favor, selecione uma data.',
                    'funcionario_id': funcionario_id
                })
            
            formatos_de_data = ['%Y-%m-%d', '%b. %d, %Y']
            data_selecionada = None

            for formato in formatos_de_data:
                try:
                    print(f"Tentando converter a data: {data} com o formato: {formato}")
                    data_selecionada = datetime.strptime(data, formato).date()
                    break
                except ValueError:
                    continue
            
            if data_selecionada is None:
                return render(request, 'selecionar_horario.html', {
                    'cliente': cliente,
                    'servico': servico,
                    'error': 'Formato de data inválido.',
                    'funcionario_id': funcionario_id
                })
                
            horarios = Disponibilidade.objects.filter(data=data_selecionada, funcionario=funcionario, disponivel=True)
            return render(request, 'selecionar_horario.html', {
                'cliente': cliente,
                'servico': servico,
                'horarios': horarios,
                'data_selecionada': data_selecionada,
                'funcionario_id': funcionario_id
            })

        if 'horario_id' in request.POST:
            horario_id = request.POST.get('horario_id')
            horario = get_object_or_404(Disponibilidade, id=horario_id)
            return redirect('confirmar_agendamento', cliente_id=cliente.id, servico_id=servico.id, horario_id=horario.id)

    return render(request, 'selecionar_horario.html', {
        'cliente': cliente,
        'servico': servico,
        'funcionario_id': funcionario_id,
        'horarios': horarios
    })


def confirmar_agendamento(request, cliente_id, servico_id, horario_id):
    """
    Página para confirmar o agendamento, onde o cliente vê os detalhes e confirma.
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)
    servico = get_object_or_404(Servico, id=servico_id)
    horario = get_object_or_404(Disponibilidade, id=horario_id)

    if request.method == 'POST':
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            servico=servico,
            funcionario=horario.funcionario,
            disponibilidade=horario,
            status='confirmado',
        )
        horario.disponivel = False
        horario.save()

        # Após a confirmação, redireciona para a página de agendamentos do cliente com uma mensagem de sucesso
        agendamentos = Agendamento.objects.filter(cliente=cliente)
        return render(request, 'agendamento_cliente.html', {
            'cliente': cliente,
            'agendamentos': agendamentos,
            'mensagem': 'Agendamento confirmado com sucesso!',
        })

    return render(request, 'confirmar_agendamento.html', {
        'cliente': cliente,
        'servico': servico,
        'horario': horario,
    })
