import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "05-scripts"))
import exportar_relatorio_csv as exportador

def test_exporta_indicador_com_login_aceito(tmp_path, monkeypatch):
    arquivo_csv = tmp_path / "indicadores-correlacao.csv"
    monkeypatch.setattr(exportador, "ARQUIVO_SAIDA", arquivo_csv)

    from datetime import datetime

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

    exportador.exportar_csv(achados)

    with arquivo_csv.open(
        "r", encoding="utf-8-sig", newline=""
    ) as arquivo:
        linhas = list(csv.DictReader(arquivo))

    assert len(linhas) == 1
    assert linhas[0]["ip"] == "192.168.115.30"
    assert linhas[0]["quantidade_falhas"] == "4"
    assert linhas[0]["login_aceito"] == "Sim"
    assert linhas[0]["usuario"] == "felipe"
    assert linhas[0]["classificacao"] == "Requer investigacao"


def test_csv_sem_indicadores_contem_apenas_cabecalho(
    tmp_path, monkeypatch
):
    arquivo_csv = tmp_path / "indicadores-correlacao.csv"
    monkeypatch.setattr(exportador, "ARQUIVO_SAIDA", arquivo_csv)

    exportador.exportar_csv([])

    with arquivo_csv.open(
        "r", encoding="utf-8-sig", newline=""
    ) as arquivo:
        leitor = csv.DictReader(arquivo)
        linhas = list(leitor)

    assert linhas == []
    assert leitor.fieldnames is not None
    assert "ip" in leitor.fieldnames
    assert "classificacao" in leitor.fieldnames
