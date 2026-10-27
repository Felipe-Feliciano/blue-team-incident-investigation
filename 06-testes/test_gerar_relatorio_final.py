import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "05-scripts"),
)

import gerar_relatorio_final as gerador


def test_relatorio_inclui_indicador_e_login(tmp_path, monkeypatch):
    arquivo = tmp_path / "relatorio.md"
    monkeypatch.setattr(gerador, "RELATORIO", arquivo)

    eventos = [
        {
            "data": datetime(2026, 10, 27, 9, 14, 2),
            "origem": "auth.log",
            "descricao": "Falha SSH de teste",
        }
    ]

    achados = [
        {
            "ip": "192.168.115.30",
            "quantidade_falhas": 4,
            "inicio": datetime(2026, 10, 27, 9, 14, 2),
            "fim": datetime(2026, 10, 27, 9, 15, 1),
            "logins": [
                {
                    "usuario": "felipe",
                    "data": datetime(2026, 10, 27, 9, 16, 22),
                }
            ],
        }
    ]

    comandos = [
        {
            "data": datetime(2026, 10, 27, 9, 17, 3),
            "usuario": "felipe",
            "comando": "whoami",
        }
    ]

    gerador.gerar_relatorio(eventos, achados, comandos)
    conteudo = arquivo.read_text(encoding="utf-8")

    assert "192.168.115.30" in conteudo
    assert "Falhas SSH: 4" in conteudo
    assert "felipe" in conteudo
    assert "Linha do tempo" in conteudo
    assert "whoami" in conteudo
    assert "não comprovam" in conteudo


def test_relatorio_sem_indicadores(tmp_path, monkeypatch):
    arquivo = tmp_path / "relatorio.md"
    monkeypatch.setattr(gerador, "RELATORIO", arquivo)

    gerador.gerar_relatorio([], [], [])
    conteudo = arquivo.read_text(encoding="utf-8")

    assert "Eventos analisados: 0" in conteudo
    assert "Nenhum indicador atingiu os critérios configurados." in conteudo
    assert "Limitações da análise" in conteudo
