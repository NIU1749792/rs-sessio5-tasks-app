# AGENTS.md — Directives per a OpenCode

## Entorn i Stack Tècnic
- Llenguatge: Python 3.11+ (només biblioteca estàndard).
- Interfície: Línia de comandes (CLI) amb el mòdul `argparse`.
- Manteniment de Dades: Fitxer JSON local (`data/tasks.json`), relatiu al directori de treball actual.

## Estructura del Repositori
- `src/` → codi font (`tasks_app.py`, `models.py`).
- `test/` → proves amb pytest (`test_tasks_app.py`).
- `data/` → fitxer de persistència `tasks.json`.

## Comandes de Desenvolupament
- Executar aplicació: `python3 src/tasks_app.py <comandament> [opcions]`
  - Comandaments disponibles: `add`, `list`, `edit`, `complete`.
- Executar amb una data fixada: `TASKS_APP_AVUI=2026-11-24 python3 src/tasks_app.py list`
- Executar tots els tests: `python3 -m pytest test`
- Executar test únic: `python3 -m pytest test/test_tasks_app.py`

## Convencions de Codi
- Estil: PEP8.
- Idioma del codi i comentaris: Català (mantenir consistència en noms de variables). No afegeixis àlies ni noms en anglès (excepte la classe `Task`).
- Els missatges per pantalla han de coincidir literalment amb els de `SPECIFICATIONS.md`.

## Convencions de Test
- Cada escenari Gherkin (GS-xx) de `SPECIFICATIONS.md` ha de tenir com a mínim un test amb el seu identificador al nom (ex. `test_gs01_creacio_tasca`).
- Els tests s'executen en un directori temporal (fixture `tmp_path` de pytest, amb `cwd=tmp_path`). Mai modifiquen el `data/tasks.json` del repositori.
- Els tests que depenen de la data actual han de fixar-la amb la variable d'entorn `TASKS_APP_AVUI=YYYY-MM-DD` (RNF-05). Mai depenen del dia real d'execució.
- Les dates es tracten amb el mòdul estàndard `datetime` (`date.fromisoformat`).

## Regles de Gestió de Tasques (`TASKS.md`)
1. Llegeix `TASKS.md` i identifica la següent tasca amb estat `[ ]`.
2. Canvia l'estat de la tasca actual a `[/]` abans d'iniciar la codificació.
3. Executa ÚNICAMENT una sola tasca per torn (encara que la següent sigui només de validació).
4. Verifica que el codi compleixi els requisits i escenaris Gherkin de `SPECIFICATIONS.md`.
5. Quan estigui completada i verificada, canvia l'estat a `[x]`.
6. Atura't i demana confirmació a l'usuari abans de passar a la següent tasca.

## Restriccions de Desenvolupament (Límits)
- No instal·lis llibreries externes no autoritzades (només `pytest`, ja instal·lat).
- Només pots crear o modificar fitxers a `src/`, `test/` i `data/`, i l'estat de les tasques a `TASKS.md`.
- Mai modifiquis `AGENTS.md`, `SPECIFICATIONS.md`, `.devcontainer/` ni `requirements.txt`.
- Mai executis comandes `git` (els commits els fa el desenvolupador).
- Mai llegeixis ni modifiquis la carpeta `_esborranys/`.
- No trenquis la compatibilitat amb els escenaris GS de versions anteriors: tots els tests existents han de continuar passant.
- Si una especificació és ambigua, pregunta abans d'implementar.
