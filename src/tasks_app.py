import argparse
import json
from pathlib import Path

from models import Task

RUTA_TASQUES = Path('data') / 'tasks.json'


def llegeix_tasques():
    with RUTA_TASQUES.open(encoding='utf-8') as fitxer:
        registres = json.load(fitxer)
    return [Task.des_de_diccionari(registre) for registre in registres]


def desa_tasques(tasques):
    registres = [tasca.a_diccionari() for tasca in tasques]
    with RUTA_TASQUES.open('w', encoding='utf-8') as fitxer:
        json.dump(registres, fitxer, ensure_ascii=False, indent=4)


def afegeix_tasca(titol, assignatura):
    tasques = llegeix_tasques()
    tasca = Task(len(tasques) + 1, titol, assignatura)
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

    subcomandaments.add_parser('list', help='Mostra totes les tasques.')

    arguments = parser.parse_args()
    if arguments.comandament == 'add':
        afegeix_tasca(arguments.titol, arguments.assignatura)
    else:
        mostra_tasques()


if __name__ == '__main__':
    main()
