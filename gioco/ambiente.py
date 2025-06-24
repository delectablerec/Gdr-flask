import random
from gioco.oggetto import BombaAcida, Oggetto, PozioneCura
from gioco.classi import Guerriero, Ladro, Mago
from gioco.personaggio import Personaggio
from utils.log import Log
from utils.messaggi import Messaggi


 
class Ambiente():
    """
    E responsabile alla gestione di variabili  globali dovuti all'ambiente
    interagisce con le classi Personaggio e Oggetto
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
        """Restituisce uno stato serializzabile per session o JSON.

        Returns:
            dict: Dizionario del materiale serializzato
        """
        return {
            "classe": self.__class__.__name__,
            "nome": self.nome,
            "modifica_attacco": self.modifica_attacco,
            "modifica_cura": self.modifica_cura
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Ambiente":
        """
        Ricostruisce un'istanza di Ambiente o di una sua sottoclasse a partire da un dizionario serializzato.

        Utilizza il valore associato alla chiave "classe" per determinare quale sottoclasse
        di Ambiente istanziare. Se la classe non è riconosciuta, restituisce un'istanza di Foresta come default.

        Args:
            data (dict): Dizionario contenente i dati serializzati dell'ambiente.
                Deve contenere almeno la chiave "classe" con il nome della sottoclasse.

        Returns:
            Ambiente: Un'istanza della sottoclasse di Ambiente indicata nel dizionario.
        """
        classe_nome = data.get("classe", "Foresta")
        ambiente_cls = globals().get(classe_nome, Foresta)
        return ambiente_cls()

class Foresta(Ambiente):
    """
    La classe Foresta eredita da Ambiente e rappresenta un ambiente specifico
    con modifiche agli attacchi dei guerrieri e alla cura a fine turno per i ladri.
    """
    def __init__(self):
        super().__init__(nome="Foresta", modifica_attacco=5, modifica_cura=5)

    def modifica_attacco_max(self, attaccante: Personaggio) -> int:
        """
        Il metodo controlla se l'attaccante è un Guerriero e, in caso affermativo,
        aumenta il suo attacco massimo di un valore definito modifica_attacco=5.

        Args:
            attaccante (Personaggio): Attaccante

        Returns:
            int: Il valore intero che andrà a modificare l'attacco o 0 se l'attaccante non è un guerriero
        """
        if isinstance(attaccante, Guerriero):
            msg = f"{attaccante.nome} guadagna {self.modifica_attacco} attacco nella Foresta!"
            Messaggi.add_to_messaggi(msg)
            Log.scrivi_log(msg)
            return self.modifica_attacco
        return 0

    def modifica_effetto_oggetto(self, oggetto: Oggetto) -> int:
        """
        Questo metodo non modifica l'effetto dell'oggetto.

        Args:
            oggetto (Oggetto): Oggetto da modificare

        returns:
            int: 0
        """
        return 0

    def mod_cura(self, soggetto: Personaggio) -> int:
        """
        Questa funzione aumenta la cura del ladro di un valore definito nell'ambiente Foresta.

        Args:
            soggetto (Personaggio): Il personaggio che riceve la cura se è un ladro

        returns:
            int: L'aumento della cura se il soggetto è un ladro, altrimenti 0
        """
        if isinstance(soggetto, Ladro):
            return self.modifica_cura
        return 0


 
class Vulcano(Ambiente):
    """
    La classe Vulcano eredita da Ambiente e rappresenta un ambiente specifico
    con modifiche agli attacchi dei maghi e dei ladri, un incremento random dei
    danni delle bombe acide e alla cura a fine turno per tutti.
    """
    def __init__(self):
        super().__init__(nome="Vulcano", modifica_attacco=10, modifica_cura=-5)

    def modifica_attacco_max(self, attaccante: Personaggio) -> int:
        """
        Il metodo controlla se l'attaccante è un Mago e, in caso affermativo,
        aumenta il suo attacco massimo di un valore definito modifica_attacco=10.
        Se l'attaccante è un Ladro, diminuisce il suo attacco massimo di un valore
        definito modifica_attacco=10.

        Args:
            attaccante (Personaggio): Il personaggio che attacca

        returns:
            int: L'aumento o la diminuzione dell'attacco massimo
        """

        if isinstance(attaccante, Mago):
            msg = f"{attaccante.nome} guadagna {self.modifica_attacco} attacco nel Vulcano!"
            Messaggi.add_to_messaggi(msg)
            Log.scrivi_log(msg)
            return self.modifica_attacco
        elif isinstance(attaccante, Ladro):
            msg = f"{attaccante.nome} perde {self.modifica_attacco} attacco nel Vulcano!"
            Messaggi.add_to_messaggi(msg)
            Log.scrivi_log(msg)
            return -self.modifica_attacco
        return 0

    def modifica_effetto_oggetto(self, oggetto: Oggetto) -> int:
        """
        Il metodo aumenta il danno della bomba acida di un valore casuale da 0 a 15

        Args:
            oggetto (Oggetto): Oggetto da modificare

        returns:
            int: Aumento del danno della bomba acida
        """
        if isinstance(oggetto, BombaAcida):
            variazione = random.randint(0, 15)
            msg = f"Nella {self.nome}, la Bomba Acida guadagna {variazione} danni!"
            Messaggi.add_to_messaggi(msg)
            Log.scrivi_log(msg)
            return variazione
        return 0

    def mod_cura(self, soggetto: Personaggio) -> int:
        """
        Questo metodo aumenta la cura di tutti i personaggi di un valore definito
        nell'ambiente Vulcano.

        Args:
            soggetto (Personaggio): Il personaggio che riceve la cura

        returns:
            int: L'aumento della cura se il soggetto è un ladro, altrimenti 0

        """
        return self.modifica_cura


 
class Palude(Ambiente):
    """
    La classe Palude eredita da Ambiente e rappresenta un ambiente specifico
    con un decremento agli attacchi dei ladri e dei guerrieri, e alle cure delle
    pozioni
    """
    def __init__(self):
        super().__init__(nome="Palude", modifica_attacco=-5, modifica_cura=0.3)
    
    def modifica_attacco_max(self, attaccante: Personaggio) -> int:
        """
        Il metodo controlla se l'attaccante è un Guerriero o un Ladro e, in caso affermativo,
        diminuisce il suo attacco massimo di un valore definito modifica_attacco=-5 nell'ambiente Palude.

        Args:
            attaccante (Personaggio): Il personaggio che attacca

        returns:
            int: La diminuzione dell'attacco massimo
        """
        if isinstance(attaccante, (Guerriero, Ladro)):
            msg = f"{attaccante.nome} perde {-self.modifica_attacco} attacco nella Palude!"
            Messaggi.add_to_messaggi(msg)
            Log.scrivi_log(msg)
            return self.modifica_attacco
        return 0

    def modifica_effetto_oggetto(self, oggetto: Oggetto) -> int:
        """
        Il metodo riduce l'effetto della Pozione Cura del %30
        Args:
            oggetto (Oggetto): Oggetto da modificare

        returns:
            int: Riduzione dell'effetto della Pozione Cura
        """
        if isinstance(oggetto, PozioneCura):
            riduzione = int(oggetto.valore * self.modifica_cura)
            msg = f"Nella {self.nome}, la Pozione Cura ha effetto ridotto di {riduzione} punti!"
            Messaggi.add_to_messaggi(msg)
            Log.scrivi_log(msg)
            return -riduzione
        return 0

    def mod_cura(self, soggetto: Personaggio) -> int:
        return 0


class AmbienteFactory:
    """
    Factory per la generazione di ambienti nel sistema di combattimento.
    Fornisce metodi per creare un ambiente casuale oppure selezionarlo manualmente.
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
        """
        Permette all'utente di selezionare un ambiente tra quelli disponibili.

        Se l'input è valido, viene restituito l'ambiente predefinito (Foresta).

        Args:
            None

        Returns:
            ambiente: Un'istanza della sottoclasse selezionata di Ambiente, o Foresta come default.
        """
        return AmbienteFactory.get_opzioni().get(scelta, Foresta())

    @staticmethod
    def sorteggia_ambiente() -> Ambiente:
        """
        Sorteggia un ambiente casuale tra quelli disponibili.

        Args:
            None

        Returns:
           ambiente: Un'istanza di una sottoclasse di Ambiente scelta casualmente (Foresta, Vulcano o Palude).
        """
        ambienti = list(AmbienteFactory.get_opzioni().values())
        ambiente = random.choice(ambienti)
        msg = f"Ambiente Casuale Selezionato: {ambiente.nome}"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        return ambiente