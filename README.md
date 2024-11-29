# Sistema de Agendamentos para Barbearia

## 📝 Descrição
Este sistema foi desenvolvido para gerenciar de forma eficiente os agendamentos de serviços da Barbershop, proporcionando uma experiência prática e intuitiva tanto para os clientes quanto para os administradores e funcionários.

O sistema automatiza o processo de agendamento, garantindo que horários sejam controlados com base na duração de cada serviço, além de oferecer flexibilidade para que os clientes selecionem suas preferências de atendimento.

## 🚀 Ferramentas Utilizadas
- **Python**: Linguagem principal usada no desenvolvimento.
- **Django**: Framework web para o backend.
- **HTML/CSS**: Criação e estilização do frontend.
- **SQLite**: Banco de dados utilizado para armazenamento e consulta de dados.

## 🎯 Funcionalidade Ideal do Sistema
O fluxo do sistema segue os seguintes passos:

1. **Tela Inicial**
   - O cliente insere o número de telefone.
   - O sistema exibe os agendamentos já realizados pelo cliente.
   - Caso não haja agendamentos, aparece uma opção para criar um novo agendamento.

2. **Novo Agendamento**
   - O cliente seleciona o serviço desejado.
   - O sistema verifica a duração do serviço para calcular os horários disponíveis.

3. **Escolha de Preferências**
   - **Preferência por Funcionário:**
     - O cliente seleciona o funcionário desejado.
     - O sistema exibe os horários disponíveis para o funcionário escolhido.
   - **Sem Preferência por Funcionário:**
     - O cliente seleciona um horário disponível.
     - O sistema exibe os funcionários disponíveis naquele horário.

4. **Confirmação**
   - Após selecionar o serviço, funcionário e horário, o agendamento é confirmado.
   - O cliente recebe uma mensagem de sucesso com os detalhes do agendamento.

5. **Gerenciamento de Agendamentos**
   - Funcionários podem visualizar suas agendas.
   - Administradores podem gerenciar serviços, horários e funcionários.

## 📋 Regras de Negócio

1. **Cadastro de Clientes**
   - Caso o cliente não esteja cadastrado no sistema, será solicitado o registro inicial (nome e número de telefone).

2. **Serviços**
   - Cada serviço possui uma descrição, duração e preço.
   - A duração do serviço determina os horários disponíveis.

3. **Funcionários**
   - Cada funcionário possui:
     - Um horário de trabalho predefinido.
     - Serviços que pode realizar.
   - Preferências do cliente podem direcionar a seleção de funcionários.

4. **Horários Disponíveis**
   - Baseados na duração do serviço e na disponibilidade do funcionário.
   - Conflitos de agenda são automaticamente evitados.

5. **Confirmação de Agendamentos**
   - Após a seleção do serviço, funcionário e horário, o agendamento é confirmado.
   - O horário é bloqueado para novos agendamentos.

## 📌 Funcionalidades
- Tela Inicial: Exibição de agendamentos existentes e opção de criar novos.
- Novo Agendamento: Seleção de serviço, preferências (funcionário/horário) e confirmação.
- Gerenciamento de Agendamentos: Controle total para administradores e funcionários.
- Duração Personalizada: Horários calculados com base no tempo de cada serviço.
- Conflito de Horários: Gerenciamento automatizado para evitar sobreposição.

## 👥 Contribuições
Sugestões e melhorias são bem-vindas!
Abra issues ou envie pull requests para colaborar.