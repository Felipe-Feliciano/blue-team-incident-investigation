
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RELATORIO = BASE_DIR / "04-relatorios" / "relatorio-final-automatico.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))

from correlacionar_eventos import ler_logs, analisar


def gerar_relatorio(eventos, achados, comandos):
    RELATORIO.parent.mkdir(parents=True, exist_ok=True)

    linhas = [
        "# Relatório Final de Investigação Blue Team",
        "",
        f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        "",
        "> **Aviso:** os registros utilizados neste projeto são simulados "
        "para fins educacionais.",
        "",
        "## 1. Resumo executivo",
        "",
        f"- Eventos analisados: {len(eventos)}",
        f"- Indicadores de correlação encontrados: {len(achados)}",
        f"- Comandos registrados identificados: {len(comandos)}",
        "",
        "A análise correlaciona registros de autenticação SSH e atividade "
        "de sistema. Os indicadores identificados devem ser investigados "
        "e não constituem, isoladamente, prova de comprometimento.",
        "",
        "## 2. Indicadores identificados",
        "",
    ]

    if achados:
        for numero, achado in enumerate(achados, start=1):
            linhas.extend([
                f"### Indicador {numero}",
                "",
                f"- IP de origem: `{achado['ip']}`",
                f"- Falhas SSH: {achado['quantidade_falhas']}",
                f"- Início da sequência: {achado['inicio']}",
                f"- Fim da sequência: {achado['fim']}",
            ])

            if achado["logins"]:
                linhas.append("- Logins aceitos correlacionados:")
                for login in achado["logins"]:
                    linhas.append(
                        f"  - Usuário `{login['usuario']}`, "
                        f"em {login['data']}"
                    )
            else:
                linhas.append("- Login aceito correlacionado: não identificado")

            linhas.extend([
                "",
                "**Classificação:** requer investigação.",
                "",
            ])
    else:
        linhas.extend([
            "Nenhum indicador atingiu os critérios configurados.",
            "",
        ])

    linhas.extend([
        "## 3. Linha do tempo",
        "",
        "| Data e hora | Fonte | Evento registrado |",
        "|---|---|---|",
    ])

    for evento in eventos:
        descricao = evento["descricao"].replace("|", "\\|")
        linhas.append(
            f"| {evento['data']} | {evento['origem']} | {descricao} |"
        )

    linhas.extend([
        "",
        "## 4. Atividade de sistema registrada",
        "",
    ])

    if comandos:
        for evento in comandos:
            linhas.append(
                f"- **{evento['data']}** — usuário `{evento['usuario']}`: "
                f"`{evento['comando']}`"
            )
    else:
        linhas.append("Nenhum comando reconhecido nos registros.")

    linhas.extend([
        "",
        "Os registros de comandos indicam atividade registrada, mas não "
        "comprovam, por si só, que os comandos foram executados com sucesso.",
        "",
        "## 5. Recomendações",
        "",
        "1. Validar se as autenticações identificadas eram autorizadas.",
        "2. Consultar logs adicionais para confirmar o contexto dos eventos.",
        "3. Verificar os resultados dos comandos e eventuais registros de "
        "uso de privilégios.",
        "4. Preservar as evidências originais e registrar a conclusão "
        "da investigação.",
        "",
        "## 6. Limitações da análise",
        "",
        "- Os registros são fictícios e não representam um incidente real.",
        "- A correlação temporal não comprova causalidade nem identidade "
        "do responsável.",
        "- Um login aceito não demonstra, isoladamente, acesso indevido.",
        "- Os comandos registrados não comprovam sucesso, elevação de "
        "privilégios ou persistência.",
        "- A análise depende dos padrões de log reconhecidos pelo script.",
        "",
        "## 7. Conclusão",
        "",
        "O script identificou eventos que merecem validação e organizou "
        "as evidências para apoiar uma investigação. Não é possível "
        "confirmar comprometimento com os registros simulados disponíveis.",
        "",
    ])

    RELATORIO.write_text("\n".join(linhas), encoding="utf-8")

    print(f"Relatório final salvo em: {RELATORIO}")
    print(f"Eventos incluídos: {len(eventos)}")
    print(f"Indicadores incluídos: {len(achados)}")
    print(f"Comandos incluídos: {len(comandos)}")


def main():
    eventos = ler_logs()
    achados, comandos = analisar(eventos)
    gerar_relatorio(eventos, achados, comandos)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as erro:
        print(f"ERRO: {erro}")

