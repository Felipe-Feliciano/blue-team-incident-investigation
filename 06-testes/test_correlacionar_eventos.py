import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "05-scripts")
)

from correlacionar_eventos import analisar


def criar_evento(minuto, segundo, descricao):
    return {
        "data": datetime(2026, 10, 27, 9, minuto, segundo),
        "origem": "auth.log",
        "descricao": descricao,
    }


def test_detecta_tres_falhas_e_login_aceito():
    eventos = [
        criar_evento(
            14, 2,
            "Failed password for admin from 192.168.115.30"
        ),
        criar_evento(
            14, 18,
            "Failed password for admin from 192.168.115.30"
        ),
        criar_evento(
            14, 35,
            "Failed password for admin from 192.168.115.30"
        ),
        criar_evento(
            15, 30,
            "Accepted password for felipe from 192.168.115.30"
        ),
    ]

    achados, comandos = analisar(eventos)

    assert len(achados) == 1
    assert achados[0]["ip"] == "192.168.115.30"
    assert achados[0]["quantidade_falhas"] == 3
    assert len(achados[0]["logins"]) == 1
    assert comandos == []


def test_nao_alerta_com_duas_falhas():
    eventos = [
        criar_evento(
            14, 2,
            "Failed password for admin from 192.168.115.30"
        ),
        criar_evento(
            14, 18,
            "Failed password for admin from 192.168.115.30"
        ),
    ]

    achados, comandos = analisar(eventos)

    assert achados == []
    assert comandos == []


def test_nao_correlaciona_login_de_outro_ip():
    eventos = [
        criar_evento(
            14, 2,
            "Failed password for admin from 192.168.115.30"
        ),
        criar_evento(
            14, 18,
            "Failed password for admin from 192.168.115.30"
        ),
        criar_evento(
            14, 35,
            "Failed password for admin from 192.168.115.30"
        ),
        criar_evento(
            15, 0,
            "Accepted password for felipe from 192.168.115.20"
        ),
    ]

    achados, _ = analisar(eventos)

    assert len(achados) == 1
    assert achados[0]["logins"] == []


def test_identifica_comandos_registrados():
    eventos = [
        criar_evento(
            17, 42,
            'USER_CMD user=felipe command="sudo cat /etc/shadow"'
        ),
    ]

    achados, comandos = analisar(eventos)

    assert achados == []
    assert len(comandos) == 1
    assert comandos[0]["usuario"] == "felipe"
    assert comandos[0]["comando"] == "sudo cat /etc/shadow"
