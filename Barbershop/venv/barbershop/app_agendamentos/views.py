from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Servico, Funcionario, Horario, Agendamento

def entrada_cliente(request):
    if request.method == 'POST':
        telefone = request.POST.get('telefone')
        try:
            cliente = Cliente.objects.get(telefone=telefone)
            agendamentos = Agendamento.objects.filter(cliente=cliente)
            return render(request, 'agendamento_cliente.html', {'cliente': cliente, 'agendamentos': agendamentos})
        except Cliente.DoesNotExist:
            return redirect('cadastro_cliente', telefone=telefone)
    return render(request, 'entrada_cliente.html')

def cadastro_cliente(request, telefone):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cliente = Cliente.objects.create(nome=nome, telefone=telefone)
        return redirect('entrada_cliente')
    return render(request, 'cadastro_cliente.html', {'telefone': telefone})

def novo_agendamento(request, cliente_id):
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
        funcionario_id = request.POST.get('funcionario')
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)
        horarios = Horario.objects.filter(funcionario=funcionario, disponivel=True)
        return render(request, 'selecionar_horario.html', {'cliente': cliente, 'servico': servico, 'funcionario': funcionario, 'horarios': horarios})
    return render(request, 'selecionar_funcionario.html', {'cliente': cliente, 'servico': servico, 'funcionarios': funcionarios})

def selecionar_horario(request, cliente_id, servico_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    servico = get_object_or_404(Servico, id=servico_id)
    horarios = Horario.objects.filter(disponivel=True)
    if request.method == 'POST':
        horario_id = request.POST.get('horario')
        horario = get_object_or_404(Horario, id=horario_id)
        return render(request, 'confirmar_agendamento.html', {'cliente': cliente, 'servico': servico, 'horario': horario})
    return render(request, 'selecionar_horario.html', {'cliente': cliente, 'servico': servico, 'horarios': horarios})

def confirmar_agendamento(request, cliente_id, servico_id, horario_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    servico = get_object_or_404(Servico, id=servico_id)
    horario = get_object_or_404(Horario, id=horario_id)
    if request.method == 'POST':
        funcionario_id = request.POST.get('funcionario')
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            servico=servico,
            funcionario=funcionario,
            horario=horario,
            status='confirmado'
        )
        agendamento.save()
        return render(request, 'agendamento_confirmado.html', {'cliente': cliente, 'servico': servico, 'funcionario': funcionario, 'horario': horario})
    return render(request, 'confirmar_agendamento.html', {'cliente': cliente, 'servico': servico, 'horario': horario})
