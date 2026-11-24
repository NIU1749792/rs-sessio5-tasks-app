import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

from models import Task

RUTA_TASQUES = Path('data') / 'tasks.json'


def data_limit_valida(valor):
    if valor is None:
        return True
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', valor) is None:
        return False
    try:
        date.fromisoformat(valor)
    except ValueError:
        return False
    return True


def data_actual():
    valor = os.environ.get('TASKS_APP_AVUI')
    if valor is not None and data_limit_valida(valor):
        return date.fromisoformat(valor)
    return date.today()


def assegura_fitxer():
    RUTA_TASQUES.parent.mkdir(parents=True, exist_ok=True)
    if not RUTA_TASQUES.exists():
        RUTA_TASQUES.write_text('[]', encoding='utf-8')


def llegeix_tasques():
    assegura_fitxer()
    with RUTA_TASQUES.open(encoding='utf-8') as fitxer:
        registres = json.load(fitxer)
    return [Task.des_de_diccionari(registre) for registre in registres]


def desa_tasques(tasques):
    registres = [tasca.a_diccionari() for tasca in tasques]
    with RUTA_TASQUES.open('w', encoding='utf-8') as fitxer:
        json.dump(registres, fitxer, ensure_ascii=False, indent=4)


def afegeix_tasca(titol, assignatura, data_limit=None):
    tasques = llegeix_tasques()
    seguent_id = max((tasca.id for tasca in tasques), default=0) + 1
    tasca = Task(seguent_id, titol, assignatura, data_limit=data_limit)
    tasques.append(tasca)
    desa_tasques(tasques)
    print(f'Tasca [ID: {tasca.id}] creada amb èxit')


def error_id_inexistent(id_tasca):
    print(f'Error: no existeix cap tasca amb ID {id_tasca}.')
    sys.exit(1)


def edita_tasca(
    id_tasca, titol=None, assignatura=None, data_limit=None, estat=None
):
    if not RUTA_TASQUES.exists():
        error_id_inexistent(id_tasca)
    tasques = llegeix_tasques()
    for tasca in tasques:
        if tasca.id == id_tasca:
            if titol is not None:
                tasca.titol = titol
            if assignatura is not None:
                tasca.assignatura = assignatura
            if data_limit is not None:
                tasca.data_limit = data_limit
            if estat is not None:
                tasca.estat = estat
            desa_tasques(tasques)
            print(f'Tasca [ID: {id_tasca}] modificada amb èxit')
            return
    error_id_inexistent(id_tasca)


def completa_tasca(id_tasca):
    if not RUTA_TASQUES.exists():
        error_id_inexistent(id_tasca)
    tasques = llegeix_tasques()
    for tasca in tasques:
        if tasca.id == id_tasca:
            if tasca.estat == 'completada':
                print(f'La tasca [ID: {id_tasca}] ja estava completada.')
                return
            tasca.estat = 'completada'
            desa_tasques(tasques)
            print(f'Tasca [ID: {id_tasca}] marcada com a completada')
            return
    error_id_inexistent(id_tasca)


def indicador_tasca(tasca, avui):
    if tasca.estat != 'pendent' or tasca.data_limit is None:
        return ''
    dies = (date.fromisoformat(tasca.data_limit) - avui).days
    if dies < 0:
        return ' [CADUCADA]'
    if dies < 7:
        return ' [URGENT]'
    return ''


def mostra_tasques():
    tasques = llegeix_tasques()
    if not tasques:
        print('Registre de tasques buit.')
        return
    avui = data_actual()
    for tasca in tasques:
        linia = (
            f'[{tasca.id}] {tasca.titol} ({tasca.assignatura})'
            f' - estat: {tasca.estat}'
        )
        if tasca.data_limit is not None:
            linia += f' - data límit: {tasca.data_limit}'
        print(linia + indicador_tasca(tasca, avui))


def main():
    parser = argparse.ArgumentParser(
        description='Eina CLI per gestionar tasques acadèmiques.'
    )
    subcomandaments = parser.add_subparsers(
        dest='comandament', required=True
    )

    parser_afegeix = subcomandaments.add_parser(
        'add', help='Afegeix una nova tasca.'
    )
    parser_afegeix.add_argument(
        '--title', dest='titol', required=True, help='Títol de la tasca.'
    )
    parser_afegeix.add_argument(
        '--subject', dest='assignatura', required=True,
        help='Assignatura de la tasca.'
    )
    parser_afegeix.add_argument(
        '--due', dest='data_limit', help='Data límit (YYYY-MM-DD).'
    )

    subcomandaments.add_parser('list', help='Mostra totes les tasques.')

    parser_edita = subcomandaments.add_parser(
        'edit', help='Modifica una tasca existent.'
    )
    parser_edita.add_argument(
        '--id', dest='id_tasca', type=int, required=True,
        help='Identificador de la tasca.'
    )
    parser_edita.add_argument(
        '--title', dest='titol', help='Nou títol de la tasca.'
    )
    parser_edita.add_argument(
        '--subject', dest='assignatura', help='Nova assignatura de la tasca.'
    )
    parser_edita.add_argument(
        '--due', dest='data_limit', help='Nova data límit (YYYY-MM-DD).'
    )
    parser_edita.add_argument(
        '--status', dest='estat', help='Nou estat de la tasca.'
    )

    parser_completa = subcomandaments.add_parser(
        'complete', help='Marca una tasca com a completada.'
    )
    parser_completa.add_argument(
        '--id', dest='id_tasca', type=int, required=True,
        help='Identificador de la tasca.'
    )

    arguments = parser.parse_args()
    if arguments.comandament == 'add':
        if not data_limit_valida(arguments.data_limit):
            print('Error: la data límit ha de tenir el format YYYY-MM-DD.')
            sys.exit(1)
        afegeix_tasca(
            arguments.titol, arguments.assignatura, arguments.data_limit
        )
    elif arguments.comandament == 'edit':
        if not data_limit_valida(arguments.data_limit):
            print('Error: la data límit ha de tenir el format YYYY-MM-DD.')
            sys.exit(1)
        if arguments.estat is not None and arguments.estat not in (
            'pendent', 'completada'
        ):
            print("Error: l'estat ha de ser 'pendent' o 'completada'.")
            sys.exit(1)
        if (
            arguments.titol is None
            and arguments.assignatura is None
            and arguments.data_limit is None
            and arguments.estat is None
        ):
            print('Error: cal indicar almenys un atribut a modificar.')
            sys.exit(1)
        edita_tasca(
            arguments.id_tasca,
            arguments.titol,
            arguments.assignatura,
            arguments.data_limit,
            arguments.estat,
        )
    elif arguments.comandament == 'complete':
        completa_tasca(arguments.id_tasca)
    else:
        mostra_tasques()


if __name__ == '__main__':
    main()
