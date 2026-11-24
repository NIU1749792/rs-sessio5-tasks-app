import argparse
import json
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


def mostra_tasques():
    tasques = llegeix_tasques()
    if not tasques:
        print('Registre de tasques buit.')
        return
    for tasca in tasques:
        print(
            f'[{tasca.id}] {tasca.titol} ({tasca.assignatura})'
            f' - estat: {tasca.estat}'
        )


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

    arguments = parser.parse_args()
    if arguments.comandament == 'add':
        if not data_limit_valida(arguments.data_limit):
            print('Error: la data límit ha de tenir el format YYYY-MM-DD.')
            sys.exit(1)
        afegeix_tasca(
            arguments.titol, arguments.assignatura, arguments.data_limit
        )
    else:
        mostra_tasques()


if __name__ == '__main__':
    main()
