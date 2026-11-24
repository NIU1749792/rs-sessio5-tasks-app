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


@pytest.fixture
def directori_sense_fitxer(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
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


def test_gs04_creacio_automatica_del_fitxer(directori_sense_fitxer):
    resultat = executa(directori_sense_fitxer, 'list')

    ruta_tasques = directori_sense_fitxer / 'data' / 'tasks.json'
    assert resultat.returncode == 0
    assert resultat.stdout.strip() == 'Registre de tasques buit.'
    assert ruta_tasques.read_text(encoding='utf-8').strip() == '[]'


def test_gs05_assignacio_id_incremental(directori_temporal):
    tasques = [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'RS',
            'estat': 'pendent',
        }
    ]
    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    ruta_tasques.write_text(
        json.dumps(tasques, ensure_ascii=False), encoding='utf-8'
    )

    resultat = executa(
        directori_temporal,
        'add', '--title', 'Examen parcial', '--subject', 'SO',
    )

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == 'Tasca [ID: 2] creada amb èxit'
    assert len(json.loads(ruta_tasques.read_text(encoding='utf-8'))) == 2


def test_gs06_creacio_sense_assignatura(directori_temporal):
    resultat = executa(
        directori_temporal,
        'add', '--title', 'Pràctica 1',
    )

    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    assert resultat.returncode != 0
    assert 'error:' in resultat.stderr
    assert 'creada amb èxit' not in resultat.stdout
    assert json.loads(ruta_tasques.read_text(encoding='utf-8')) == []
