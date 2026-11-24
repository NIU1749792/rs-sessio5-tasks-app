import json
import os
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


def executa(directori, *arguments, entorn=None):
    return subprocess.run(
        [sys.executable, str(RUTA_SCRIPT), *arguments],
        cwd=directori,
        capture_output=True,
        text=True,
        env=entorn,
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
            'data_limit': None,
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


def test_gs06b_creacio_titol_buit(directori_temporal):
    resultat = executa(
        directori_temporal,
        'add', '--title', '', '--subject', 'RS',
    )

    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    assert resultat.returncode != 0
    assert resultat.stdout.strip() == (
        "Error: el títol i l'assignatura no poden ser buits."
    )
    assert json.loads(ruta_tasques.read_text(encoding='utf-8')) == []


def test_gs07_creacio_amb_data_limit(directori_temporal):
    resultat = executa(
        directori_temporal,
        'add', '--title', 'Pràctica 2', '--subject', 'RS',
        '--due', '2026-12-15',
    )

    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    assert resultat.returncode == 0
    assert resultat.stdout.strip() == 'Tasca [ID: 1] creada amb èxit'
    assert json.loads(ruta_tasques.read_text(encoding='utf-8')) == [
        {
            'id': 1,
            'titol': 'Pràctica 2',
            'assignatura': 'RS',
            'estat': 'pendent',
            'data_limit': '2026-12-15',
        }
    ]


def test_gs08_creacio_sense_data_limit(directori_temporal):
    resultat = executa(
        directori_temporal,
        'add', '--title', 'Lectura', '--subject', 'IA',
    )

    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    assert resultat.returncode == 0
    assert json.loads(ruta_tasques.read_text(encoding='utf-8')) == [
        {
            'id': 1,
            'titol': 'Lectura',
            'assignatura': 'IA',
            'estat': 'pendent',
            'data_limit': None,
        }
    ]


def test_gs09_data_limit_format_incorrecte(directori_temporal):
    resultat = executa(
        directori_temporal,
        'add', '--title', 'Pràctica 2', '--subject', 'RS',
        '--due', '15/12/2026',
    )

    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    assert resultat.returncode != 0
    assert resultat.stdout.strip() == (
        'Error: la data límit ha de tenir el format YYYY-MM-DD.'
    )
    assert json.loads(ruta_tasques.read_text(encoding='utf-8')) == []


def test_gs10_lectura_registre_v1x(directori_temporal):
    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    ruta_tasques.write_text(
        json.dumps(
            [
                {
                    'id': 1,
                    'titol': 'Pràctica 1',
                    'assignatura': 'RS',
                    'estat': 'pendent',
                }
            ],
            ensure_ascii=False,
        ),
        encoding='utf-8',
    )

    resultat = executa(directori_temporal, 'list')

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == '[1] Pràctica 1 (RS) - estat: pendent'
    assert resultat.stderr == ''


def test_gs11_modificacio_dun_atribut(directori_temporal):
    tasques = [
        {
            'id': 1,
            'titol': 'Practica 1',
            'assignatura': 'RS',
            'estat': 'pendent',
            'data_limit': '2026-12-01',
        }
    ]
    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    ruta_tasques.write_text(
        json.dumps(tasques, ensure_ascii=False), encoding='utf-8'
    )

    resultat = executa(
        directori_temporal, 'edit', '--id', '1', '--title', 'Pràctica 1'
    )

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == 'Tasca [ID: 1] modificada amb èxit'
    assert json.loads(ruta_tasques.read_text(encoding='utf-8')) == [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'RS',
            'estat': 'pendent',
            'data_limit': '2026-12-01',
        }
    ]


def test_gs12_modificacio_de_diversos_atributs(directori_temporal):
    tasques = [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'SO',
            'estat': 'pendent',
            'data_limit': '2026-12-01',
        }
    ]
    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    ruta_tasques.write_text(
        json.dumps(tasques, ensure_ascii=False), encoding='utf-8'
    )

    resultat = executa(
        directori_temporal,
        'edit', '--id', '1', '--subject', 'RS', '--due', '2026-12-10',
    )

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == 'Tasca [ID: 1] modificada amb èxit'
    assert json.loads(ruta_tasques.read_text(encoding='utf-8')) == [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'RS',
            'estat': 'pendent',
            'data_limit': '2026-12-10',
        }
    ]


def test_gs13_modificacio_tasca_inexistent(directori_temporal):
    tasques = [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'RS',
            'estat': 'pendent',
            'data_limit': None,
        }
    ]
    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    contingut_inicial = json.dumps(tasques, ensure_ascii=False)
    ruta_tasques.write_text(contingut_inicial, encoding='utf-8')

    resultat = executa(
        directori_temporal,
        'edit', '--id', '99', '--title', 'Nou títol',
    )

    assert resultat.returncode != 0
    assert resultat.stdout.strip() == (
        'Error: no existeix cap tasca amb ID 99.'
    )
    assert ruta_tasques.read_text(encoding='utf-8') == contingut_inicial


def test_gs14_modificacio_sense_atributs(directori_temporal):
    tasques = [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'RS',
            'estat': 'pendent',
            'data_limit': None,
        }
    ]
    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    contingut_inicial = json.dumps(tasques, ensure_ascii=False)
    ruta_tasques.write_text(contingut_inicial, encoding='utf-8')

    resultat = executa(directori_temporal, 'edit', '--id', '1')

    assert resultat.returncode != 0
    assert resultat.stdout.strip() == (
        'Error: cal indicar almenys un atribut a modificar.'
    )
    assert ruta_tasques.read_text(encoding='utf-8') == contingut_inicial


def test_gs15_modificacio_estat_no_valid(directori_temporal):
    tasques = [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'RS',
            'estat': 'pendent',
            'data_limit': None,
        }
    ]
    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    contingut_inicial = json.dumps(tasques, ensure_ascii=False)
    ruta_tasques.write_text(contingut_inicial, encoding='utf-8')

    resultat = executa(
        directori_temporal, 'edit', '--id', '1', '--status', 'acabada'
    )

    assert resultat.returncode != 0
    assert resultat.stdout.strip() == (
        "Error: l'estat ha de ser 'pendent' o 'completada'."
    )
    assert ruta_tasques.read_text(encoding='utf-8') == contingut_inicial


def test_gs16_marca_tasca_completada(directori_temporal):
    tasques = [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'RS',
            'estat': 'pendent',
            'data_limit': None,
        }
    ]
    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    ruta_tasques.write_text(
        json.dumps(tasques, ensure_ascii=False), encoding='utf-8'
    )

    resultat = executa(directori_temporal, 'complete', '--id', '1')

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == (
        'Tasca [ID: 1] marcada com a completada'
    )
    assert json.loads(ruta_tasques.read_text(encoding='utf-8')) == [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'RS',
            'estat': 'completada',
            'data_limit': None,
        }
    ]


def test_gs17_tasca_ja_completada(directori_temporal):
    tasques = [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'RS',
            'estat': 'completada',
            'data_limit': None,
        }
    ]
    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    contingut_inicial = json.dumps(tasques, ensure_ascii=False)
    ruta_tasques.write_text(contingut_inicial, encoding='utf-8')

    resultat = executa(directori_temporal, 'complete', '--id', '1')

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == (
        'La tasca [ID: 1] ja estava completada.'
    )
    assert ruta_tasques.read_text(encoding='utf-8') == contingut_inicial


def test_gs18_completar_tasca_inexistent(directori_temporal):
    tasques = [
        {
            'id': 1,
            'titol': 'Pràctica 1',
            'assignatura': 'RS',
            'estat': 'pendent',
            'data_limit': None,
        }
    ]
    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    contingut_inicial = json.dumps(tasques, ensure_ascii=False)
    ruta_tasques.write_text(contingut_inicial, encoding='utf-8')

    resultat = executa(directori_temporal, 'complete', '--id', '7')

    assert resultat.returncode != 0
    assert resultat.stdout.strip() == (
        'Error: no existeix cap tasca amb ID 7.'
    )
    assert ruta_tasques.read_text(encoding='utf-8') == contingut_inicial


def test_gs19_llistat_caducades_urgents_i_sense_avis(directori_temporal):
    tasques = [
        {
            'id': 1,
            'titol': 'Lliurament P4',
            'assignatura': 'RS',
            'estat': 'pendent',
            'data_limit': '2026-11-20',
        },
        {
            'id': 2,
            'titol': 'Examen parcial',
            'assignatura': 'SO',
            'estat': 'pendent',
            'data_limit': '2026-11-24',
        },
        {
            'id': 3,
            'titol': 'Pràctica 2',
            'assignatura': 'GABD',
            'estat': 'pendent',
            'data_limit': '2026-11-30',
        },
        {
            'id': 4,
            'titol': 'Pràctica 3',
            'assignatura': 'TDIW',
            'estat': 'pendent',
            'data_limit': '2026-12-01',
        },
        {
            'id': 5,
            'titol': 'Informe',
            'assignatura': 'RS',
            'estat': 'completada',
            'data_limit': '2026-11-20',
        },
        {
            'id': 6,
            'titol': 'Lectura',
            'assignatura': 'IA',
            'estat': 'pendent',
            'data_limit': None,
        },
    ]
    ruta_tasques = directori_temporal / 'data' / 'tasks.json'
    ruta_tasques.write_text(
        json.dumps(tasques, ensure_ascii=False), encoding='utf-8'
    )
    entorn = os.environ.copy()
    entorn['TASKS_APP_AVUI'] = '2026-11-24'

    resultat = executa(directori_temporal, 'list', entorn=entorn)

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        (
            '[1] Lliurament P4 (RS) - estat: pendent'
            ' - data límit: 2026-11-20 [CADUCADA]'
        ),
        (
            '[2] Examen parcial (SO) - estat: pendent'
            ' - data límit: 2026-11-24 [URGENT]'
        ),
        (
            '[3] Pràctica 2 (GABD) - estat: pendent'
            ' - data límit: 2026-11-30 [URGENT]'
        ),
        '[4] Pràctica 3 (TDIW) - estat: pendent - data límit: 2026-12-01',
        (
            '[5] Informe (RS) - estat: completada'
            ' - data límit: 2026-11-20'
        ),
        '[6] Lectura (IA) - estat: pendent',
    ]
    assert resultat.stderr == ''
