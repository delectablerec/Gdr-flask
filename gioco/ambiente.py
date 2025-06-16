import random
from gioco.oggetto import BombaAcida, Oggetto, PozioneCura
from gioco.classi import Guerriero, Ladro, Mago
from gioco.personaggio import Personaggio
from utils.log import Log
from utils.salvataggio import SerializableMixin

@SerializableMixin.register_class
class Ambiente(SerializableMixin):
    """
    Classe base per gli ambienti, con serializzazione e metodi stub.
    """
    def __init__(self, nome: str, modifica_attacco: int = 0, modifica_cura: float = 0):
        self.nome = nome
        self.modifica_attacco = modifica_attacco
        self.modifica_cura = modifica_cura

    def modifica_attacco_max(self, attaccante: Personaggio) -> int:
        raise NotImplementedError

    def modifica_effetto_oggetto(self, oggetto: Oggetto) -> int:
        raise NotImplementedError

    def mod_cura(self, soggetto: Personaggio) -> int:
        raise NotImplementedError

    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON."""
        return {
            "classe": self.__class__.__name__,
            "nome": self.nome,
            "modifica_attacco": self.modifica_attacco,
            "modifica_cura": self.modifica_cura
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Ambiente":
        """Ricostruisce l’istanza a partire da un dict serializzato."""
        mapping = {
            "Foresta": Foresta,
            "Vulcano": Vulcano,
            "Palude": Palude
        }
        ambiente_cls = mapping.get(data.get("classe"), Foresta)
        return ambiente_cls()

@SerializableMixin.register_class
class Foresta(Ambiente):
    def __init__(self):
        super().__init__(nome="Foresta", modifica_attacco=5, modifica_cura=5)

    def modifica_attacco_max(self, attaccante: Personaggio) -> int:
        if isinstance(attaccante, Guerriero):
            msg = f"{attaccante.nome} guadagna {self.modifica_attacco} attacco nella Foresta!"
            Log.scrivi_log(msg)
            return self.modifica_attacco
        return 0

    def modifica_effetto_oggetto(self, oggetto: Oggetto) -> int:
        return 0

    def mod_cura(self, soggetto: Personaggio) -> int:
        if isinstance(soggetto, Ladro):
            return self.modifica_cura
        return 0

@SerializableMixin.register_class
class Vulcano(Ambiente):
    def __init__(self):
        super().__init__(nome="Vulcano", modifica_attacco=10, modifica_cura=-5)

    def modifica_attacco_max(self, attaccante: Personaggio) -> int:
        if isinstance(attaccante, Mago):
            msg = f"{attaccante.nome} guadagna {self.modifica_attacco} attacco nel Vulcano!"
            Log.scrivi_log(msg)
            return self.modifica_attacco
        elif isinstance(attaccante, Ladro):
            msg = f"{attaccante.nome} perde {self.modifica_attacco} attacco nel Vulcano!"
            Log.scrivi_log(msg)
            return -self.modifica_attacco
        return 0

    def modifica_effetto_oggetto(self, oggetto: Oggetto) -> int:
        if isinstance(oggetto, BombaAcida):
            variazione = random.randint(0, 15)
            msg = f"Nella {self.nome}, la Bomba Acida guadagna {variazione} danni!"
            Log.scrivi_log(msg)
            return variazione
        return 0

    def mod_cura(self, soggetto: Personaggio) -> int:
        return self.modifica_cura

@SerializableMixin.register_class
class Palude(Ambiente):
    def __init__(self):
        super().__init__(nome="Palude", modifica_attacco=-5, modifica_cura=0.3)

    def modifica_attacco_max(self, attaccante: Personaggio) -> int:
        if isinstance(attaccante, (Guerriero, Ladro)):
            msg = f"{attaccante.nome} perde {-self.modifica_attacco} attacco nella Palude!"
            Log.scrivi_log(msg)
            return self.modifica_attacco
        return 0

    def modifica_effetto_oggetto(self, oggetto: Oggetto) -> int:
        if isinstance(oggetto, PozioneCura):
            riduzione = int(oggetto.valore * self.modifica_cura)
            msg = f"Nella {self.nome}, la Pozione Cura ha effetto ridotto di {riduzione} punti!"
            Log.scrivi_log(msg)
            return -riduzione
        return 0

    def mod_cura(self, soggetto: Personaggio) -> int:
        return 0

class AmbienteFactory:
    """
    Factory per ottenere ambienti via form (get_opzioni, seleziona_da_id)
    o in modo casuale (sorteggia_ambiente).
    """
    @staticmethod
    def get_opzioni() -> dict[str, Ambiente]:
        return {
            "1": Foresta(),
            "2": Vulcano(),
            "3": Palude()
        }

    @staticmethod
    def seleziona_da_id(scelta: str) -> Ambiente:
        return AmbienteFactory.get_opzioni().get(scelta, Foresta())

    @staticmethod
    def sorteggia_ambiente() -> Ambiente:
        ambienti = list(AmbienteFactory.get_opzioni().values())
        ambiente = random.choice(ambienti)
        msg = f"Ambiente Casuale Selezionato: {ambiente.nome}"
        Log.scrivi_log(msg)
        return ambiente