from django.db import models
from datetime import datetime, date

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
    
class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, unique=True)
    cortes_feitos = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nome
    
class Horario(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    disponivel = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('funcionario', 'data', 'horario_inicio')
        
    def __str__(self):
        return f'{self.data} {self.horario_inicio}-{self.horario_fim} - {self.funcionario}'
    
    def verificar_conflito(self, duracao):
        horario_final = (datetime.combine(date.min, self.horario_inicio) + duracao).time()
        return horario_final <= self.horario_fim
    
class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado')
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    horario = models.ForeignKey(Horario, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    finalizado = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('horario', 'funcionario')
        
    def __str__(self):
        return f'{self.cliente.nome} - {self.servico.nome} em {self.horario.data} às {self.horario_inicio} com {self.funcionario.nome if self.funcionario else "funcionário não atribuído"}'
    
    def save(self, *args, **kwargs):
        if self.horario and self.status == 'confirmado':
            self.horario.disponivel = False
            self.horario.save()
            super().save(*args, **kwargs)
