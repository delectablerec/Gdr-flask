from utils.log import Log
# serve per random.randint nei metodi attacca
import random
from utils.salvataggio import SerializableMixin
@SerializableMixin.register_class
class Personaggio(SerializableMixin):
    """
    Classe Padre per tutte classi
    Contiene le proprietà comuni a ogni classe (Mago, Ladro, Guerriero)
    """
    def __init__(self, nome: str) -> None:
        self.nome = nome
        self.salute = 100
        self.salute_max = 200
        self.attacco_min = 5
        self.attacco_max = 80
        self.storico_danni_subiti = []
        self.livello = 1

    def attacca(self, bersaglio: 'Personaggio', mod_ambiente: int = 0) -> None:
        danno = random.randint(self.attacco_min, (self.attacco_max + mod_ambiente)) 
        testo = f"{self.nome} attacca {bersaglio.nome} per {danno} punti!"
        Log.scrivi_log(testo)
        bersaglio.subisci_danno(danno)

    def subisci_danno(self, danno: int) -> None:
        self.salute = max(0, self.salute - danno)
        self.storico_danni_subiti.append(danno)
        testo = f"Salute di {self.nome}: {self.salute}\n"
        Log.scrivi_log(testo)

    def sconfitto(self) -> bool:
        return self.salute <= 0

    def recupera_salute(self, mod_ambiente: int = 0) -> None:
        if self.salute == 100:
            testo = f"{self.nome} ha già la salute piena."
            Log.scrivi_log(testo)
            return
        recupero = int(self.salute * 0.3) + mod_ambiente
        nuova_salute = min(self.salute + recupero, 100)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        testo = f"\n{self.nome} recupera {effettivo} HP. Salute attuale: {self.salute}"
        Log.scrivi_log(testo)

    def migliora_statistiche(self) -> None:
        self.livello += 1
        self.attacco_max += 0.02 * self.attacco_max
        self.salute_max += 0.01 * self.salute_max
        testo = f"{self.nome} è salito al livello {self.livello}!"
        Log.scrivi_log(testo)

    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON."""
        return {
            "classe": self.__class__.__name__,
            "nome": self.nome,
            "salute": self.salute,
            "salute_max": self.salute_max,
            "attacco_min": self.attacco_min,
            "attacco_max": self.attacco_max,
            "storico_danni_subiti": self.storico_danni_subiti,
            "livello": self.livello
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Personaggio":
        """Ricostruisce l’istanza a partire da un dict serializzato."""
        obj = cls(data["nome"])
        obj.salute = data.get("salute", 100)
        obj.salute_max = data.get("salute_max", 200)
        obj.attacco_min = data.get("attacco_min", 5)
        obj.attacco_max = data.get("attacco_max", 80)
        obj.storico_danni_subiti = data.get("storico_danni_subiti", [])
        obj.livello = data.get("livello", 1)
        return obj
