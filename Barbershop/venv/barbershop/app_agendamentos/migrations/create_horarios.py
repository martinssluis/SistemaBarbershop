import datetime
from django.core.management.base import BaseCommand
from app_agendamentos.models import Funcionario, Horario

class Command(BaseCommand):
    help = 'Cria horários para todos os funcionários de segunda a sábado, das 8h às 20h'

    def handle(self, *args, **kwargs):
        start_time = datetime.time(8, 0)
        end_time = datetime.time(20, 0)
        delta = datetime.timedelta(minutes=30)  # Intervalo de 30 minutos entre horários

        dias_da_semana = [0, 1, 2, 3, 4, 5]  # Segunda a Sábado
        funcionarios = Funcionario.objects.all()

        for funcionario in funcionarios:
            for dia in dias_da_semana:
                current_time = datetime.datetime.combine(datetime.date.today(), start_time)
                while current_time.time() < end_time:
                    horario_fim = (datetime.datetime.combine(datetime.date.today(), current_time.time()) + delta).time()
                    Horario.objects.get_or_create(
                        data=current_time.date() + datetime.timedelta(days=(dia - current_time.weekday() % 7)),
                        horario_inicio=current_time.time(),
                        horario_fim=horario_fim,
                        funcionario=funcionario,
                        defaults={'disponivel': True}
                    )
                    current_time += delta

        self.stdout.write(self.style.SUCCESS('Horários criados com sucesso!'))
