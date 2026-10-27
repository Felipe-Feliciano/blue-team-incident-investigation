# Relatório Final de Investigação Blue Team

**Gerado em:** 27/10/2026 14:17:53

> **Aviso:** os registros utilizados neste projeto são simulados para fins educacionais.

## 1. Resumo executivo

- Eventos analisados: 13
- Indicadores de correlação encontrados: 1
- Comandos registrados identificados: 5

A análise correlaciona registros de autenticação SSH e atividade de sistema. Os indicadores identificados devem ser investigados e não constituem, isoladamente, prova de comprometimento.

## 2. Indicadores identificados

### Indicador 1

- IP de origem: `192.168.115.30`
- Falhas SSH: 4
- Início da sequência: 2026-10-27 09:14:02
- Fim da sequência: 2026-10-27 09:15:01
- Logins aceitos correlacionados:
  - Usuário `felipe`, em 2026-10-27 09:16:22

**Classificação:** requer investigação.

## 3. Linha do tempo

| Data e hora | Fonte | Evento registrado |
|---|---|---|
| 2026-10-27 09:14:02 | auth.log | Oct 27 09:14:02 ubuntu-server sshd[2101]: Failed password for invalid user admin from 192.168.115.30 port 51001 ssh2 |
| 2026-10-27 09:14:18 | auth.log | Oct 27 09:14:18 ubuntu-server sshd[2102]: Failed password for invalid user admin from 192.168.115.30 port 51002 ssh2 |
| 2026-10-27 09:14:35 | auth.log | Oct 27 09:14:35 ubuntu-server sshd[2103]: Failed password for invalid user admin from 192.168.115.30 port 51003 ssh2 |
| 2026-10-27 09:15:01 | auth.log | Oct 27 09:15:01 ubuntu-server sshd[2104]: Failed password for felipe from 192.168.115.30 port 51004 ssh2 |
| 2026-10-27 09:16:22 | auth.log | Oct 27 09:16:22 ubuntu-server sshd[2105]: Accepted password for felipe from 192.168.115.30 port 51005 ssh2 |
| 2026-10-27 09:17:03 | atividade-sistema.log | Oct 27 09:17:03 ubuntu-server audit[2201]: USER_CMD user=felipe command="whoami" |
| 2026-10-27 09:17:18 | atividade-sistema.log | Oct 27 09:17:18 ubuntu-server audit[2202]: USER_CMD user=felipe command="id" |
| 2026-10-27 09:17:42 | atividade-sistema.log | Oct 27 09:17:42 ubuntu-server audit[2203]: USER_CMD user=felipe command="sudo cat /etc/shadow" |
| 2026-10-27 09:18:05 | atividade-sistema.log | Oct 27 09:18:05 ubuntu-server audit[2204]: USER_CMD user=felipe command="crontab -l" |
| 2026-10-27 09:18:40 | auth.log | Oct 27 09:18:40 ubuntu-server sshd[2106]: Failed password for invalid user backup from 192.168.115.45 port 52001 ssh2 |
| 2026-10-27 09:19:03 | auth.log | Oct 27 09:19:03 ubuntu-server sshd[2107]: Failed password for invalid user backup from 192.168.115.45 port 52002 ssh2 |
| 2026-10-27 09:22:11 | auth.log | Oct 27 09:22:11 ubuntu-server sshd[2108]: Accepted publickey for analyst from 192.168.115.20 port 53001 ssh2 |
| 2026-10-27 09:23:10 | atividade-sistema.log | Oct 27 09:23:10 ubuntu-server audit[2205]: USER_CMD user=analyst command="whoami" |

## 4. Atividade de sistema registrada

- **2026-10-27 09:17:03** — usuário `felipe`: `whoami`
- **2026-10-27 09:17:18** — usuário `felipe`: `id`
- **2026-10-27 09:17:42** — usuário `felipe`: `sudo cat /etc/shadow`
- **2026-10-27 09:18:05** — usuário `felipe`: `crontab -l`
- **2026-10-27 09:23:10** — usuário `analyst`: `whoami`

Os registros de comandos indicam atividade registrada, mas não comprovam, por si só, que os comandos foram executados com sucesso.

## 5. Recomendações

1. Validar se as autenticações identificadas eram autorizadas.
2. Consultar logs adicionais para confirmar o contexto dos eventos.
3. Verificar os resultados dos comandos e eventuais registros de uso de privilégios.
4. Preservar as evidências originais e registrar a conclusão da investigação.

## 6. Limitações da análise

- Os registros são fictícios e não representam um incidente real.
- A correlação temporal não comprova causalidade nem identidade do responsável.
- Um login aceito não demonstra, isoladamente, acesso indevido.
- Os comandos registrados não comprovam sucesso, elevação de privilégios ou persistência.
- A análise depende dos padrões de log reconhecidos pelo script.

## 7. Conclusão

O script identificou eventos que merecem validação e organizou as evidências para apoiar uma investigação. Não é possível confirmar comprometimento com os registros simulados disponíveis.
