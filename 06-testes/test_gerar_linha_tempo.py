import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "05-scripts")
)

from gerar_linha_tempo import ler_eventos


def test_le_evento_com_data_valida(tmp_path):
    arquivo = tmp_path / "auth.log"
    arquivo.write_text(
        "Oct 27 09:14:02 ubuntu-server sshd[2101]: "
        "Failed password for admin from 192.168.115.30 port 51001 ssh2\n",
        encoding="utf-8",
    )

    eventos = ler_eventos(arquivo)

    assert len(eventos) == 1
    assert eventos[0]["data"].strftime("%Y-%m-%d %H:%M:%S") == (
        "2026-10-27 09:14:02"
    )
    assert "Failed password" in eventos[0]["descricao"]


def test_ignora_linha_sem_data_valida(tmp_path):
    arquivo = tmp_path / "auth.log"
    arquivo.write_text(
        "Esta linha nao contem um evento de autenticacao\n",
        encoding="utf-8",
    )

    eventos = ler_eventos(arquivo)

    assert eventos == []


def test_le_multiplos_eventos_em_ordem_de_arquivo(tmp_path):
    arquivo = tmp_path / "auth.log"
    arquivo.write_text(
        "Oct 27 09:16:22 ubuntu-server sshd[2105]: "
        "Accepted password for felipe from 192.168.115.30 port 51005 ssh2\n"
        "Oct 27 09:14:02 ubuntu-server sshd[2101]: "
        "Failed password for admin from 192.168.115.30 port 51001 ssh2\n",
        encoding="utf-8",
    )

    eventos = ler_eventos(arquivo)

    assert len(eventos) == 2
    assert eventos[0]["data"] > eventos[1]["data"]
