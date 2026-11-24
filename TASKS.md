# TASKS.md - Tasks_app

## Increment 1: MVP - Creació i Llistat de Tasques
Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.

### Tasques d'Execució:
- [x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial. (Requisits RF-01 i RF-02)
- [x] Tasca 1.2: Implementar model de dades `Task` a `src/models.py` amb mètodes de serialització JSON. (RNF-01)
- [ ] Tasca 1.3: Desenvolupar Tasks_app a `src/tasks_app.py` amb opcions `add` i `list`. (Requisits RF-03 i RF-04)
- [ ] Tasca 1.4: Crear test d'integració a `test/test_tasks_app.py` segons els escenaris GS-01, GS-02 i GS-03.
- [ ] Tasca 1.5: Validar execució amb OpenCode i verificar que tots els tests passen (`python3 -m pytest test`).

### Tasques de millora de cobertura (v1.1):
- [ ] Tasca 1.6: Garantir la creació automàtica de `data/tasks.json` i l'assignació d'ID incremental a `src/tasks_app.py`. (RF-02, RF-05)
- [ ] Tasca 1.7: Validar les opcions obligatòries de `add` (error i codi de sortida ≠ 0). (RF-06)
- [ ] Tasca 1.8: Afegir a `test/test_tasks_app.py` els tests dels escenaris GS-04, GS-05 i GS-06.
- [ ] Tasca 1.9: Executar `python3 -m pytest test` i verificar que tots els tests (GS-01..GS-06) passen.
