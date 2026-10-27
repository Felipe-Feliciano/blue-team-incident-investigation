# Blue Team Incident Investigation

## Sobre o projeto

Projeto educacional de investigação de incidentes de segurança,
com foco em análise de logs Linux, correlação de eventos e
construção automatizada de uma linha do tempo.

O cenário simula eventos de autenticação SSH e atividades
posteriores que exigem análise defensiva.

## Objetivos

- Analisar registros de autenticação SSH.
- Correlacionar eventos de diferentes fontes.
- Construir uma linha do tempo cronológica.
- Documentar achados, hipóteses e limitações.
- Validar o script com testes automatizados.

## Tecnologias

- Kali Linux
- Linux e SSH
- Python 3
- pytest
- Logs de sistema
- Markdown

## Estrutura

- `01-planejamento/` — plano da investigação.
- `02-evidencias/` — logs fictícios do cenário.
- `03-analise/` — achados e linha do tempo.
- `04-relatorios/` — relatório técnico.
- `05-scripts/` — script Python de análise.
- `06-testes/` — testes automatizados.

## Execução

Gerar a linha do tempo:

```bash
python3 05-scripts/gerar_linha_tempo.py
