# Blue Team Incident Investigation

## Sobre o projeto

Projeto educacional de investigação de incidentes de segurança, com foco em análise de logs Linux, correlação de eventos e construção automatizada de uma linha do tempo.

O cenário simula falhas de autenticação SSH, um acesso bem-sucedido e registros posteriores de atividade no sistema. O objetivo é demonstrar técnicas básicas de investigação defensiva utilizando Python.

## Objetivos

- Analisar registros de autenticação SSH.
- Correlacionar eventos de diferentes fontes.
- Identificar sequências de falhas de autenticação seguidas por login aceito.
- Construir uma linha do tempo cronológica.
- Identificar comandos registrados nos logs de atividade.
- Documentar achados, hipóteses, limitações e recomendações.
- Validar os scripts com testes automatizados.

## Tecnologias

- Kali Linux
- Linux e SSH
- Python 3
- pytest
- Logs de sistema
- Git e GitHub
- Markdown

## Estrutura do projeto

- `01-planejamento/` — plano da investigação.
- `02-evidencias/` — logs fictícios usados no cenário.
- `03-analise/` — achados e linha do tempo.
- `04-relatorios/` — relatório técnico.
- `05-scripts/` — scripts Python de análise.
- `06-testes/` — testes automatizados e evidência de execução.

## Funcionalidades

### 1. Geração da linha do tempo

O script `05-scripts/gerar_linha_tempo.py` reúne eventos de diferentes arquivos de log, ordena os registros cronologicamente e gera `03-analise/linha-do-tempo.txt`.

### 2. Correlação de eventos

O script `05-scripts/correlacionar_eventos.py`:

- Identifica três ou mais falhas de autenticação SSH do mesmo IP em uma janela de cinco minutos.
- Verifica se existe um login aceito do mesmo IP após a sequência de falhas, dentro do intervalo configurado.
- Lista comandos registrados para apoiar a investigação.
- Apresenta os indicadores encontrados no terminal.

A correlação é um indicador para investigação adicional. Ela não comprova que o acesso foi indevido nem que os comandos registrados foram executados com sucesso.


## Como executar

### 1. Gerar a linha do tempo

```bash
python3 05-scripts/gerar_linha_tempo.py
```

### 2. Executar a correlação de eventos

```bash
python3 05-scripts/correlacionar_eventos.py
```

### 3. Exportar os indicadores para CSV

```bash
python3 05-scripts/exportar_relatorio_csv.py
```

O relatório será salvo em `04-relatorios/indicadores-correlacao.csv`, podendo ser aberto no Excel ou importado para o Power BI.

### 4. Executar os testes automatizados

```bash
python3 -m pytest -v 06-testes/
```

**Resultado atual:** 9 testes aprovados.

Os testes validam a correlação de eventos, a identificação de comandos registrados, a geração da linha do tempo e a exportação do CSV.

## Testes

O projeto possui sete testes automatizados, cobrindo:

- Leitura de eventos com datas válidas.
- Ignorar linhas sem data válida.
- Leitura de múltiplos eventos.
- Detecção de três falhas e login aceito.
- Ausência de alerta com apenas duas falhas.
- Não correlacionar um login de outro IP.
- Identificação de comandos registrados.

**Resultado validado durante o desenvolvimento: 7 testes aprovados.**

A evidência da execução está disponível em `06-testes/resultado-testes.txt`.

## Limitações

- Os eventos são fictícios e foram criados para treinamento.
- O script utiliza o ano de 2026 para interpretar as datas.
- A análise depende dos padrões de log definidos no código.
- A linha do tempo organiza eventos, mas não comprova causalidade.
- A proximidade entre falhas e login aceito não prova uma invasão.
- Os registros de comandos não comprovam sucesso, elevação de privilégios ou persistência.
- O projeto não é um SIEM e não realiza monitoramento contínuo.

## Aviso

Projeto desenvolvido para fins educacionais, utilizando evidências simuladas em um cenário controlado.
