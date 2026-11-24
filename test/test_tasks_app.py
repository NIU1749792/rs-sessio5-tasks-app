import json
import subprocess
import sys
from pathlib import Path

import pytest

RUTA_SCRIPT = Path(__file__).resolve().parents[1] / 'src' / 'tasks_app.py'


@pytest.fixture
def directori_temporal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'data').mkdir()
    (tmp_path / 'data' / 'tasks.json').write_text('[]', encoding='utf-8')
    return tmp_path


def executa(directori, *arguments):
    return subprocess.run(
        [sys.executable, str(RUTA_SCRIPT), *arguments],
        cwd=directori,
        capture_output=True,
        text=True,
    )


def test_gs01_creacio_tasca(directori_temporal):
    resultat = executa(
        directori_temporal,
        'add', '--title', 'Pràctica 1', '--subject', 'RS',
    )

    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    assert resultat.returncode == 0
    assert resultat.stdout.strip() == 'Tasca [ID: 1] creada amb èxit'
    assert json.loads(ruta_tasques.read_text(encoding='utf-8')) == [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'RS',
            'estat': 'pendent',
        }
    ]


def test_gs02_llistat_buit(directori_temporal):
    resultat = executa(directori_temporal, 'list')

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == 'Registre de tasques buit.'


def test_gs03_llistat_amb_registres(directori_temporal):
    tasques = [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'RS',
            'estat': 'pendent',
        },
        {
            'id': 2,
            'titol': 'Examen parcial',
            'assignatura': 'SO',
            'estat': 'pendent',
        },
    ]
    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    ruta_tasques.write_text(
        json.dumps(tasques, ensure_ascii=False), encoding='utf-8'
    )

    resultat = executa(directori_temporal, 'list')

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        '[1] Pràctica 1 (RS) - estat: pendent',
        '[2] Examen parcial (SO) - estat: pendent',
    ]
