import csv
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ARQUIVO_SAIDA = BASE_DIR / "04-relatorios" / "indicadores-correlacao.csv"

sys.path.insert(0, str(Path(__file__).resolve().parent))

from correlacionar_eventos import ler_logs, analisar


def exportar_csv(achados):
    ARQUIVO_SAIDA.parent.mkdir(parents=True, exist_ok=True)

    campos = [
        "ip",
        "quantidade_falhas",
        "inicio_falhas",
        "fim_falhas",
        "login_aceito",
        "usuario",
        "horario_login",
        "classificacao",
        "justificativa",
    ]

    with ARQUIVO_SAIDA.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()

        for achado in achados:
            logins = achado["logins"]

            if logins:
                for login in logins:
                    escritor.writerow({
                        "ip": achado["ip"],
                        "quantidade_falhas": achado["quantidade_falhas"],
                        "inicio_falhas": achado["inicio"].isoformat(
                            sep=" "
                        ),
                        "fim_falhas": achado["fim"].isoformat(
                            sep=" "
                        ),
                        "login_aceito": "Sim",
                        "usuario": login["usuario"],
                        "horario_login": login["data"].isoformat(
                            sep=" "
                        ),
                        "classificacao": "Requer investigacao",
                        "justificativa": (
                            "Falhas SSH seguidas por login aceito "
                            "do mesmo IP na janela analisada."
                        ),
                    })
            else:
                escritor.writerow({
                    "ip": achado["ip"],
                    "quantidade_falhas": achado["quantidade_falhas"],
                    "inicio_falhas": achado["inicio"].isoformat(
                        sep=" "
                    ),
                    "fim_falhas": achado["fim"].isoformat(
                        sep=" "
                    ),
                    "login_aceito": "Nao",
                    "usuario": "",
                    "horario_login": "",
                    "classificacao": "Requer investigacao",
                    "justificativa": (
                        "Multiplas falhas SSH na janela analisada, "
                        "sem login aceito correlacionado."
                    ),
                })

    print(f"Relatorio CSV salvo em: {ARQUIVO_SAIDA}")
    print(f"Indicadores exportados: {len(achados)}")


def main():
    eventos = ler_logs()
    achados, _ = analisar(eventos)
    exportar_csv(achados)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as erro:
        print(f"ERRO: {erro}")
