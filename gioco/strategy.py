import random
from gioco.ambiente import Ambiente
from gioco.inventario import Inventario
from gioco.personaggio import Personaggio
from utils.log import Log
from utils.salvataggio import SerializableMixin


@SerializableMixin.register_class
class StrategiaAttacco(SerializableMixin):

    def __init__(self, nome: 'str' = "Strategia di attacco"):
        self.nome = nome

    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON."""
        return {
            "classe": self.__class__.__name__,
            "nome": self.nome
        }
    @classmethod
    def from_dict(cls, data: dict) -> 'StrategiaAttacco':
        """Ricostruisce l’istanza a partire da un dict serializzato."""
        strategia = cls(nome=data.get("nome", "Strategia di attacco"))
        return strategia

    @staticmethod
    def esegui_attacco(
        nemico: 'Personaggio',
        bersaglio: 'Personaggio',
        inventario: 'Inventario',
        ambiente: 'Ambiente' = None
    ) -> None:
        raise NotImplementedError(
            "Devi implementare il metodo esegui nella sottoclasse"
        )


@SerializableMixin.register_class
class Aggressiva(StrategiaAttacco):

    def __init__(self):
        super().__init__(nome="Aggressiva")

    @classmethod
    def from_dict(cls, data: dict) -> 'Aggressiva':
        return cls(nome=data.get("nome", "Aggressiva"))

    @staticmethod
    def esegui_attacco(
        nemico: 'Personaggio',
        bersaglio: 'Personaggio',
        inventario: 'Inventario',
        ambiente: 'Ambiente' = None
    ) -> None:
        testo = f"{nemico} attacca {bersaglio.nome} con un attacco aggressivo!"
        Log.scrivi_log(testo)
        if inventario and inventario.oggetti:
            ogg = next(
                (
                    ogg for ogg in inventario.oggetti
                    if ogg.nome == "Bomba Acida"
                ),
                None
            )
            if ogg and (random.randint(0, 1) == 0):
                inventario.usa_oggetto(
                    oggetto=ogg,
                    bersaglio=bersaglio,
                    ambiente=ambiente
                )
        if bersaglio.sconfitto():
            return
        mod_attacco = ambiente.modifica_attacco_max(nemico) if ambiente else 0
        nemico.attacca(bersaglio, mod_ambiente=mod_attacco)


@SerializableMixin.register_class
class Difensiva(StrategiaAttacco):
    def __init__(self):
        super().__init__(nome="Difensiva")

    @staticmethod
    def esegui_attacco(
        nemico: 'Personaggio',
        bersaglio: 'Personaggio',
        inventario: 'Inventario',
        ambiente: 'Ambiente' = None
    ) -> None:
        testo =  f"{nemico.nome} attacca {bersaglio.nome} con un attacco difensivo!"
        Log.scrivi_log(testo)

        if nemico.salute < 60 and inventario and inventario.oggetti:
            ogg = next(
                (
                    ogg for ogg in inventario.oggetti
                    if ogg.nome == "Pozione Rossa"
                ),
                None
            )
            if ogg and (random.randint(0, 1) == 0):
                inventario.usa_oggetto(
                    oggetto=ogg,
                    bersaglio=nemico,
                    ambiente=ambiente
                )

        mod_attacco = ambiente.modifica_attacco_max(nemico) if ambiente else 0
        nemico.attacca(bersaglio, mod_attacco)


@SerializableMixin.register_class
class Equilibrata(StrategiaAttacco):
    def __init__(self):
        super().__init__(nome="Equilibrata")

    @staticmethod
    def esegui_attacco(
        nemico: 'Personaggio',
        bersaglio: 'Personaggio',
        inventario: 'Inventario',
        ambiente: 'Ambiente' = None
    ) -> None:
        testo = f"{nemico.nome} attacca {bersaglio.nome} " "con un attacco equilibrato!"
        Log.scrivi_log(testo)
        if nemico.salute < 40:
            if inventario and inventario.oggetti:
                ogg = next(
                    (
                        ogg for ogg in inventario.oggetti
                        if ogg.nome == "Pozione Rossa"
                    ),
                    None
                )
                if ogg and (random.randint(0, 2) == 0):
                    inventario.usa_oggetto(
                        oggetto=ogg,
                        bersaglio=nemico,
                        ambiente=ambiente
                    )
        elif inventario and inventario.oggetti:
            ogg = next(
                (
                    ogg for ogg in inventario.oggetti
                    if ogg.nome == "Bomba Acida"
                ),
                None
            )
            if ogg and (random.randint(0, 2) == 0):
                inventario.usa_oggetto(
                    ogg,
                    bersaglio=bersaglio,
                    ambiente=ambiente
                )
                if bersaglio.sconfitto():
                    return

        mod_attacco = ambiente.modifica_attacco_max(nemico) if ambiente else 0
        nemico.attacca(bersaglio, mod_attacco)


class StrategiaAttaccoFactory:

    @staticmethod
    def strategia_random() -> StrategiaAttacco:
        random_choice = random.choice(
            ["aggressiva", "difensiva", "equilibrata"]
        )
        return StrategiaAttaccoFactory.usa_strategia(random_choice)

    @staticmethod
    def usa_strategia(tipo: str) -> StrategiaAttacco:
        tipo = tipo.lower()
        if tipo == "aggressiva":
            return Aggressiva()
        elif tipo == "difensiva":
            return Difensiva()
        elif tipo == "equilibrata":
            return Equilibrata()
        else:
            raise ValueError(f"Tipo di strategia sconosciuto: {tipo}")