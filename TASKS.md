# TASKS.md - Tasks_app

## Increment 1: MVP - Creació i Llistat de Tasques
Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.

### Tasques d'Execució:
- [x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial. (Requisits RF-01 i RF-02)
- [x] Tasca 1.2: Implementar model de dades `Task` a `src/models.py` amb mètodes de serialització JSON. (RNF-01)
- [x] Tasca 1.3: Desenvolupar Tasks_app a `src/tasks_app.py` amb opcions `add` i `list`. (Requisits RF-03 i RF-04)
- [x] Tasca 1.4: Crear test d'integració a `test/test_tasks_app.py` segons els escenaris GS-01, GS-02 i GS-03.
- [x] Tasca 1.5: Validar execució amb OpenCode i verificar que tots els tests passen (`python3 -m pytest test`).

### Tasques de millora de cobertura (v1.1):
- [x] Tasca 1.6: Garantir la creació automàtica de `data/tasks.json` i l'assignació d'ID incremental a `src/tasks_app.py`. (RF-02, RF-05)
- [x] Tasca 1.7: Validar les opcions obligatòries de `add` (error i codi de sortida ≠ 0). (RF-06)
- [x] Tasca 1.8: Afegir a `test/test_tasks_app.py` els tests dels escenaris GS-04, GS-05 i GS-06.
- [x] Tasca 1.9: Executar `python3 -m pytest test` i verificar que tots els tests (GS-01..GS-06) passen.

## Increment 2: Data límit, modificació, completar i avisos (v2.0)
Objectiu: Gestionar el cicle de vida complet d'una tasca i avisar de les tasques caducades o urgents.
Dependències: les tasques s'han d'executar en l'ordre indicat (2.1 → 2.13).

### 2.A Data límit
- [x] Tasca 2.1: Afegir l'atribut opcional `data_limit` al model `Task` de `src/models.py`, amb serialització `YYYY-MM-DD`/`null` i lectura de registres v1.x sense aquesta clau. (RNF-01, RNF-04)
- [x] Tasca 2.2: Afegir l'opció `--due` al comandament `add` amb validació del format de data. (RF-07, RF-08, RF-09)
- [x] Tasca 2.3: Afegir els tests GS-07, GS-08, GS-09 i GS-10 a `test/test_tasks_app.py` i verificar que passen.

### 2.B Modificació de tasques
- [x] Tasca 2.4: Implementar el comandament `edit --id <ID>` amb les opcions `--title`, `--subject`, `--due` i `--status`, actualitzant només els atributs indicats. (RF-10, RF-11, RF-15)
- [x] Tasca 2.5: Implementar els errors d'`edit`: ID inexistent, cap atribut indicat i estat no vàlid. (RF-12, RF-13, RF-14)
- [x] Tasca 2.6: Afegir els tests GS-11, GS-12, GS-13, GS-14 i GS-15 i verificar que passen.

### 2.C Completar tasques
- [x] Tasca 2.7: Implementar el comandament `complete --id <ID>`, incloent el cas de tasca ja completada i d'ID inexistent. (RF-16, RF-17, RF-12)
- [x] Tasca 2.8: Afegir els tests GS-16, GS-17 i GS-18 i verificar que passen.

### 2.D Avisos al llistat
- [x] Tasca 2.9: Implementar l'obtenció de la data actual amb suport per a la variable d'entorn `TASKS_APP_AVUI`. (RNF-05)
- [ ] Tasca 2.10: Ampliar `list` per mostrar la data límit i els indicadors `[CADUCADA]` i `[URGENT]`. (RF-04, RF-18, RF-19, RF-20)
- [ ] Tasca 2.11: Afegir el test GS-19 i verificar que passa.

### 2.E Valors buits i validació de l'increment
- [ ] Tasca 2.12: Rebutjar títol o assignatura buits als comandaments `add` i `edit`, i afegir el test GS-06b. (RF-06 [v2.0])
- [ ] Tasca 2.13: Executar `python3 -m pytest test` i verificar que passen tots els tests (GS-01..GS-19 i GS-06b).
