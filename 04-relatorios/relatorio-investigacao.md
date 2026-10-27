# Relatório de Investigação de Incidente — Blue Team

## 1. Resumo executivo

Foi analisado um cenário simulado com registros de autenticação
SSH e atividade de sistema em um servidor Linux.

A análise identificou falhas repetidas de autenticação, seguidas
por um acesso bem-sucedido e registros de comandos que merecem
verificação adicional.

Os dados disponíveis não permitem confirmar um comprometimento.

## 2. Escopo e metodologia

A investigação utilizou dois arquivos fictícios:

- `02-evidencias/auth.log`
- `02-evidencias/atividade-sistema.log`

Foram analisados horários, endereços IP, usuários, métodos de
autenticação e comandos registrados.

## 3. Principais observações

### 3.1 Falhas de autenticação

O endereço 192.168.115.30 apresentou quatro falhas de autenticação
entre 09:14:02 e 09:15:01.

O endereço 192.168.115.45 apresentou duas falhas.

### 3.2 Acesso bem-sucedido

Às 09:16:22, foi registrado um acesso SSH por senha para o usuário
felipe, proveniente de 192.168.115.30.

A proximidade temporal com as falhas anteriores justifica
investigação adicional, mas não prova que os eventos têm a mesma
origem humana ou que o acesso foi indevido.

### 3.3 Atividade após o acesso

Foram registrados comandos de consulta de identidade e grupos,
uma tentativa registrada de consulta ao arquivo /etc/shadow e
uma consulta à tabela de tarefas agendadas do usuário.

Os registros apresentados não confirmam o resultado dos comandos,
a elevação de privilégios ou alterações persistentes.

## 4. Avaliação preliminar de risco

Prioridade de investigação: alta.

Justificativa: combinação de falhas de autenticação, acesso
bem-sucedido e registro de um comando direcionado a informações
sensíveis.

Esta prioridade é uma avaliação do cenário simulado, não uma
confirmação de invasão.

## 5. Recomendações defensivas

- Verificar se o acesso do usuário felipe era autorizado.
- Consultar registros completos de sudo e auditoria do sistema.
- Validar a origem do endereço IP e o contexto da conexão.
- Verificar alterações em contas, permissões e tarefas agendadas.
- Preservar os logs originais e registrar horários de coleta.
- Se houver suspeita real, seguir o procedimento de resposta a
  incidentes da organização antes de realizar alterações no host.

## 6. Limitações

Os eventos analisados são fictícios e foram preparados para
treinamento.

Não foram coletadas evidências de um sistema real, nem confirmados
o sucesso do comando sudo, a elevação de privilégios ou a existência
de persistência.

## 7. Conclusão

O cenário apresenta indicadores que justificam uma investigação
mais profunda, especialmente a sequência de falhas SSH, login
aceito e atividade posterior.

Com as evidências disponíveis, não é possível concluir que houve
comprometimento. A conclusão deverá ser revisada caso novas
evidências confiáveis sejam obtidas.
