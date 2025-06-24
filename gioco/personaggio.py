from gioco.basic import Basic
from utils.log import Log
# serve per random.randint nei metodi attacca
import random, uuid
 
from utils.messaggi import Messaggi

 
class Personaggio(Basic):
    """
    Classe Padre per tutte classi
    Contiene le proprietà comuni a ogni classe (Mago, Ladro, Guerriero)
    """
    def __init__(self, nome: str) -> None:
        self.id = str(uuid.uuid4())  
        self.nome = nome
        self.salute = 100
        self.salute_max = 200
        self.attacco_min = 5
        self.attacco_max = 80
        self.storico_danni_subiti = []
        self.livello = 1

    def attacca(self, bersaglio: 'Personaggio', mod_ambiente: int = 0) -> None:
        """
        Metodo di attacco di cui viene fatto l'override in ogni
        classe derivata da personaggio.

        Args:
            bersaglio (Personaggio): bersaglio dell'attacco
            mod_ambiente (int): modificatore di attacco in base all'ambiente

        Returns:
            None
        """
        danno = random.randint(self.attacco_min, (self.attacco_max + mod_ambiente)) 
        msg = f"{self.nome} attacca {bersaglio.nome} per {danno} punti!"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        bersaglio.subisci_danno(danno)

    def subisci_danno(self, danno: int) -> None:
        """
        Sottrae il danno (Input) alla salute del personaggio.

        Args:
            danno (int): danno subito dal personaggio

        Returns:
            None
        """
        self.salute = max(0, self.salute - danno)
        self.storico_danni_subiti.append(danno)
        msg = f"Salute di {self.nome}: {self.salute}\n"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)

    def sconfitto(self) -> bool:
        """
        Verifica se il personaggio è sceso a zero di salute.

        Args:
            None

        Returns:
            bool: True se il personaggio è sconfitto, in caso contrario False
        """
        return self.salute <= 0

    def recupera_salute(self, mod_ambiente: int = 0) -> None:
        """
        Recupera la salute del personaggio del 30% della salute corrente.
        Viene usato da pozioni e dal recupero salute post duello.

        Args:
            mod_ambiente (int): modificatore di recupero in base all'ambiente

        Returns:
            None
        """
        if self.salute == 100:
            msg = f"{self.nome} ha già la salute piena."
            Messaggi.add_to_messaggi(msg)
            Log.scrivi_log(msg)
            return
        recupero = int(self.salute * 0.3) + mod_ambiente
        nuova_salute = min(self.salute + recupero, 100)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        msg = f"\n{self.nome} recupera {effettivo} HP. Salute attuale: {self.salute}"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)

    def migliora_statistiche(self) -> None:
        """
        Metodo per aumentare il livello del personaggio e quindi
        migliorarne le statistiche.
        Aumenta del 2% l'attacco massimo e dell'1% la salute massima.

        Args:
            None

        Returns:
            None
        """
        self.livello += 1
        self.attacco_max += 0.02 * self.attacco_max
        self.salute_max += 0.01 * self.salute_max
        msg = f"{self.nome} è salito al livello {self.livello}!"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)

    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON.

        Returns:
            dict: Dizionario del materiale serializzato
        """
        return {
            "classe": self.__class__.__name__,
            "id": self.id,
            "nome": self.nome,
            "salute": self.salute,
            "salute_max": self.salute_max,
            "attacco_min": self.attacco_min,
            "attacco_max": self.attacco_max,
            "storico_danni_subiti": self.storico_danni_subiti,
            "livello": self.livello,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Personaggio":
        """Ricostruisce l’istanza a partire da un dict serializzato.

        Args:
            data (dict): Dati serializzati

        Returns:
            Ambiente: Dati deserializzati
        """
        oggetto = cls(data["nome"])
        oggetto.salute = data.get("salute", 100)
        oggetto.salute_max = data.get("salute_max", 200)
        oggetto.attacco_min = data.get("attacco_min", 5)
        oggetto.attacco_max = data.get("attacco_max", 80)
        oggetto.storico_danni_subiti = data.get("storico_danni_subiti", [])
        oggetto.livello = data.get("livello", 1)
        return oggetto
