from datetime import datetime
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parents[1]
EVIDENCIAS_DIR = BASE_DIR / "02-evidencias"

PADRAO_DATA = re.compile(
    r"^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})"
)


def ler_eventos(arquivo):
    eventos = []

    with arquivo.open("r", encoding="utf-8") as f:
        for linha in f:
            resultado = PADRAO_DATA.search(linha)

            if not resultado:
                continue

            data_texto = resultado.group(1)

            try:
                data = datetime.strptime(
                    f"2026 {data_texto}",
                    "%Y %b %d %H:%M:%S"
                )
            except ValueError:
                continue

            eventos.append({
                "data": data,
                "origem": arquivo.name,
                "descricao": linha.strip(),
            })

    return eventos


def main():
    arquivos = [
        EVIDENCIAS_DIR / "auth.log",
        EVIDENCIAS_DIR / "atividade-sistema.log",
    ]

    eventos = []

    for arquivo in arquivos:
        if not arquivo.exists():
            print(f"Arquivo nao encontrado: {arquivo}")
            return

        eventos.extend(ler_eventos(arquivo))

    eventos.sort(key=lambda evento: evento["data"])

    saida = BASE_DIR / "03-analise" / "linha-do-tempo.txt"

    with saida.open("w", encoding="utf-8") as f:
        f.write("LINHA DO TEMPO DA INVESTIGACAO\n")
        f.write("=" * 80 + "\n\n")

        for evento in eventos:
            horario = evento["data"].strftime("%Y-%m-%d %H:%M:%S")
            linha = (
                f"[{horario}] [{evento['origem']}] "
                f"{evento['descricao']}\n"
            )
            f.write(linha)
            print(linha, end="")

    print(f"\nLinha do tempo salva em: {saida}")


if __name__ == "__main__":
    main()
