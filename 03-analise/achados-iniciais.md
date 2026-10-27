# Achados Iniciais — Investigação Blue Team

## Achado 1 — Falhas repetidas de autenticação SSH

- IP: 192.168.115.30
- Quantidade: 4 falhas
- Período: 09:14:02 a 09:15:01
- Evidência: `02-evidencias/auth.log`
- Avaliação: atividade que merece investigação adicional.

## Achado 2 — Autenticação bem-sucedida após as falhas

- Usuário: felipe
- IP: 192.168.115.30
- Horário: 09:16:22
- Método: senha
- Evidência: `02-evidencias/auth.log`
- Avaliação: correlação temporal relevante, mas não comprova
  que as falhas e o acesso foram realizados pela mesma pessoa.

## Achado 3 — Comandos potencialmente sensíveis

- Usuário registrado: felipe
- Horário mais relevante: 09:17:42
- Comando registrado: `sudo cat /etc/shadow`
- Evidência: `02-evidencias/atividade-sistema.log`
- Avaliação: é necessário verificar se houve autorização e se
  o comando foi concluído com sucesso.

## Achado 4 — Consulta de tarefas agendadas

- Usuário: felipe
- Horário: 09:18:05
- Comando: `crontab -l`
- Evidência: `02-evidencias/atividade-sistema.log`
- Avaliação: a consulta isolada não comprova persistência.

## Limitações

Os registros são fictícios e foram criados para fins educacionais.
Não existem, até aqui, evidências suficientes para confirmar
comprometimento do servidor.
