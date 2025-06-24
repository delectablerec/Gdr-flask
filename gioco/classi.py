import random
from utils.log import Log
 
from utils.messaggi import Messaggi
from gioco.personaggio import Personaggio

 
class Mago(Personaggio):
    """
    Classe che rappresenta un personaggio mago.
    Estende la classe personaggio con attacco diminuito e recupero
    di salute personalizzato
    """
    def __init__(self, nome: str) -> None:
        """
        Inizializza il personaggio Mago con salute 80

        Args:
            nome (str): nome del personaggio

        Returns:
            None
        """
        super().__init__(nome)
        self.salute = 80

    def attacca(self, bersaglio: Personaggio, mod_ambiente: int = 0) -> None:
        """
        Il Mago ha attacco minimo diminuito di 5 e attacco massimo
        aumentato di 10

        Args:
            bersaglio (Personaggio): personaggio che subisce l'attacco
            mod_ambiente (int): modificatore ambientale di attacco (default: 0)

        Returns:
            None
        """
        danno = random.randint(self.attacco_min - 5, self.attacco_max + 10) + mod_ambiente
        msg = f"{self.nome} lancia un incantesimo su {bersaglio.nome} per {danno} danni!"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        bersaglio.subisci_danno(danno)

    def recupera_salute(self, mod_ambiente: int = 0) -> None:
        """
        Recupera la salute del Mago alla fine di ogni duello del 20%

        Args:
            mod_ambiente (int): modificatore ambientale di recupero (default: 0)

        Returns:
            None
        """
        recupero = int((self.salute + mod_ambiente) * 0.2)
        nuova_salute = min(self.salute + recupero, 80)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        msg = f"{self.nome} medita e recupera {effettivo} HP. Salute attuale: {self.salute}"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)


 
class Guerriero(Personaggio):
    """
    Classe che rappresenta un personaggio guerriero.
    Estende la classe Personaggio, con salute_max di 120, attacco piu potente e
    guarigione post duello fissa di 30 salute
    """
    def __init__(self, nome: str) -> None:
        """
        Inizializza il personaggio Guerriero con salute 120

        Args:
            nome (str): nome del personaggio

        Returns:
            None
        """
        super().__init__(nome)
        self.salute = 120

    def attacca(self, bersaglio: Personaggio, mod_ambiente: int = 0) -> None:
        """
        Il Guerriero ha un attacco minimo aumentato di 15 e un attacco
        massimo aumentato di 20 + il modificatore dell'ambiente corrente

        Args:
            bersaglio (Personaggio): personaggio che subisce l'attacco
            mod_ambiente (int): modificatore ambientale di attacco (default: 0)

        Returns:
            None
        """
        danno = random.randint(self.attacco_min + 15, self.attacco_max + mod_ambiente + 20)
        msg = f"{self.nome} colpisce con la spada {bersaglio.nome} per {danno} danni!"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        bersaglio.subisci_danno(danno)

    def recupera_salute(self, mod_ambiente: int = 0) -> None:
        """
        Il guerriero al termine di ogni duello recupera salute pari 30

        Args:
            mod_ambiente (int): modificatore ambientale di recupero (default: 0)

        Returns:
            None
        """
        recupero = 30 + mod_ambiente
        nuova_salute = min(self.salute + recupero, 120)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        msg = f"{self.nome} si fascia le ferite e recupera {effettivo} HP. Salute attuale: {self.salute}"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)


 
class Ladro(Personaggio):
    """
    Estende la classe Personaggio, ha salute elevata a 140, +5 attacco_max e
    attacco_min, recupera punti salute al termine del duello
    casualmente in un range 10-40
    """
    def __init__(self, nome: str) -> None:
        """
        Inizializza il personaggio Ladro con salute 140

        Args:
            nome (str): nome del personaggio

        Returns:
            None
        """
        super().__init__(nome)
        self.salute = 140

    def attacca(self, bersaglio: Personaggio, mod_ambiente: int = 0) -> None:
        """
        Il Ladro ha un attacco minimo aumentato di 5 e un attacco
        massimo aumentato di 5

        Args:
            bersaglio (Personaggio): personaggio che subisce l'attacco
            mod_ambiente (int): modificatore ambientale di attacco (default: 0)

        Returns:
            None
        """
        danno = random.randint(self.attacco_min + 5, self.attacco_max + 5) + mod_ambiente
        msg = f"{self.nome} colpisce furtivamente {bersaglio.nome} per {danno} danni!"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        bersaglio.subisci_danno(danno)

    def recupera_salute(self, mod_ambiente: int = 0) -> None:
        """
        Permette al ladro di recuperare un numero casuale
        di punti salute in un range 10-40, modificato dall'ambiente

        Args:
            mod_ambiente (int): modificatore ambientale di recupero (default: 0)

        Returns:
            None
        """
        recupero = random.randint(10, 40) + mod_ambiente
        nuova_salute = min(self.salute + recupero, 140)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        msg = f"{self.nome} si cura rapidamente e recupera {effettivo} HP. Salute attuale: {self.salute}"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)