from django.db import models
from datetime import datetime, date, time, timedelta

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, unique=True)
    cortes_feitos = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Disponibilidade(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()
    disponivel = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('funcionario', 'data', 'horario')
    
    def __str__(self):
        return f'{self.data} {self.horario} - {self.funcionario.nome}'

    @staticmethod
    def gerar_horarios(funcionario, data):
        """
        Gera os horários de disponibilidade para o funcionário em um dia específico.
        A barbearia funciona das 08:00 às 20:00 com intervalos de 15 minutos.
        """
        horario_inicio = time(8, 0)  # 08:00
        horario_fim = time(20, 0)  # 20:00
        delta = timedelta(minutes=15)  # Intervalo de 15 minutos
        horario_atual = datetime.combine(data, horario_inicio)
        horario_limite = datetime.combine(data, horario_fim)

        while horario_atual < horario_limite:
            # Criar disponibilidade no banco de dados se não existir
            Disponibilidade.objects.get_or_create(
                funcionario=funcionario,
                data=data,
                horario=horario_atual.time(),
                disponivel=True,
            )
            horario_atual += delta  # Avançar para o próximo horário

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_em_pontos = models.IntegerField(default=0)
    pontos_gerados = models.IntegerField(default=0)
    duracao = models.DurationField(help_text="Duração do serviço (ex: 00:30:00) para 30 minutos")
    
    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, unique=True)
    pontos = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado')
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    disponibilidade = models.ForeignKey(Disponibilidade, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    finalizado = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('disponibilidade', 'funcionario')
        
    def __str__(self):
        return f'{self.cliente.nome} - {self.servico.nome} em {self.disponibilidade.data} às {self.disponibilidade.horario} com {self.funcionario.nome if self.funcionario else "funcionário não atribuído"}'
    
    def save(self, *args, **kwargs):
        """
        Ao salvar o agendamento, se o status for confirmado, marca a disponibilidade como indisponível.
        """
        if self.disponibilidade and self.status == 'confirmado':
            # Tornar o horário indisponível após o agendamento
            self.disponibilidade.disponivel = False
            self.disponibilidade.save()
        super().save(*args, **kwargs)
