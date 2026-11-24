import json


class Task:
    def __init__(self, id, titol, assignatura, estat='pendent'):
        self.id = id
        self.titol = titol
        self.assignatura = assignatura
        self.estat = estat

    def a_diccionari(self):
        return {
            'id': self.id,
            'titol': self.titol,
            'assignatura': self.assignatura,
            'estat': self.estat,
        }

    @classmethod
    def des_de_diccionari(cls, dades):
        return cls(
            dades['id'],
            dades['titol'],
            dades['assignatura'],
            dades['estat'],
        )

    def a_json(self):
        return json.dumps(self.a_diccionari(), ensure_ascii=False)

    @classmethod
    def des_de_json(cls, text):
        return cls.des_de_diccionari(json.loads(text))
