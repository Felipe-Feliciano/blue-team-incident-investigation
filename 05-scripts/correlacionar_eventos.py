from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parents[1]
EVIDENCIAS_DIR = BASE_DIR / "02-evidencias"

ANO = 2026
JANELA_MINUTOS = 5
LIMITE_FALHAS = 3

PADRAO_DATA = re.compile(
    r"^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})"
)

PADRAO_FALHA = re.compile(
    r"Failed password for (?:invalid user )?(\S+) "
    r"from (\d{1,3}(?:\.\d{1,3}){3})"
)

PADRAO_SUCESSO = re.compile(
    r"Accepted (?:password|publickey) for (\S+) "
    r"from (\d{1,3}(?:\.\d{1,3}){3})"
)

PADRAO_COMANDO = re.compile(
    r"USER_CMD user=(\S+) command=\"([^\"]+)\""
)


def extrair_data(linha):
    resultado = PADRAO_DATA.search(linha)

    if not resultado:
        return None

    try:
        return datetime.strptime(
            f"{ANO} {resultado.group(1)}",
            "%Y %b %d %H:%M:%S",
        )
    except ValueError:
        return None


def ler_logs():
    eventos = []

    arquivos = [
        EVIDENCIAS_DIR / "auth.log",
        EVIDENCIAS_DIR / "atividade-sistema.log",
    ]

    for arquivo in arquivos:
        if not arquivo.exists():
            raise FileNotFoundError(
                f"Arquivo de evidência não encontrado: {arquivo}"
            )

        with arquivo.open("r", encoding="utf-8") as f:
            for linha in f:
                data = extrair_data(linha)

                if data is None:
                    continue

                eventos.append({
                    "data": data,
                    "origem": arquivo.name,
                    "descricao": linha.strip(),
                })

    return sorted(eventos, key=lambda evento: evento["data"])


def analisar(eventos):
    falhas_por_ip = defaultdict(list)
    logins_aceitos = []
    comandos = []

    for evento in eventos:
        linha = evento["descricao"]

        falha = PADRAO_FALHA.search(linha)
        sucesso = PADRAO_SUCESSO.search(linha)
        comando = PADRAO_COMANDO.search(linha)

        if falha:
            falhas_por_ip[falha.group(2)].append({
                "data": evento["data"],
                "usuario": falha.group(1),
            })

        if sucesso:
            logins_aceitos.append({
                "data": evento["data"],
                "usuario": sucesso.group(1),
                "ip": sucesso.group(2),
            })

        if comando:
            comandos.append({
                "data": evento["data"],
                "usuario": comando.group(1),
                "comando": comando.group(2),
            })

    achados = []

    for ip, falhas in falhas_por_ip.items():
        falhas.sort(key=lambda evento: evento["data"])

        for inicio in range(len(falhas)):
            primeira = falhas[inicio]["data"]
            limite = primeira + timedelta(minutes=JANELA_MINUTOS)

            grupo = [
                evento
                for evento in falhas[inicio:]
                if primeira <= evento["data"] <= limite
            ]

            if len(grupo) < LIMITE_FALHAS:
                continue

            fim = grupo[-1]["data"]

            sucessos = [
                login for login in logins_aceitos
                if login["ip"] == ip
                and fim <= login["data"] <= limite
            ]

            achados.append({
                "ip": ip,
                "quantidade_falhas": len(grupo),
                "inicio": primeira,
                "fim": fim,
                "logins": sucessos,
            })
            break

    return achados, comandos


def main():
    eventos = ler_logs()
    achados, comandos = analisar(eventos)

    print("RELATÓRIO DE CORRELAÇÃO DE EVENTOS")
    print("=" * 55)
    print(f"Eventos analisados: {len(eventos)}")
    print(f"Indicadores encontrados: {len(achados)}")
    print()

    for achado in achados:
        print(f"[ALERTA] IP: {achado['ip']}")
        print(
            f"Falhas SSH: {achado['quantidade_falhas']} "
            f"entre {achado['inicio']} e {achado['fim']}"
        )

        if achado["logins"]:
            for login in achado["logins"]:
                print(
                    f"Login aceito após as falhas: "
                    f"usuário={login['usuario']}, "
                    f"horário={login['data']}"
                )
        else:
            print("Nenhum login aceito correlacionado à sequência.")

        print()

    if not achados:
        print("Nenhuma sequência atingiu o limite configurado.")

    print("ATIVIDADE DE SISTEMA REGISTRADA")
    print("-" * 55)

    if comandos:
        for evento in comandos:
            print(
                f"{evento['data']} | usuário={evento['usuario']} "
                f"| comando={evento['comando']}"
            )
    else:
        print("Nenhum comando reconhecido nos registros.")

    print()
    print(
        "Nota: os registros são simulados. "
        "Correlação temporal não comprova comprometimento."
    )


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as erro:
        print(f"ERRO: {erro}")
