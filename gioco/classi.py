import random
from utils.log import Log
from utils.salvataggio import SerializableMixin
from utils.messaggi import Messaggi
from gioco.personaggio import Personaggio

@SerializableMixin.register_class
class Mago(Personaggio):
    def __init__(self, nome: str) -> None:
        super().__init__(nome)
        self.salute = 80

    def attacca(self, bersaglio: Personaggio, mod_ambiente: int = 0) -> None:
        danno = random.randint(self.attacco_min - 5, self.attacco_max + 10) + mod_ambiente
        msg = f"{self.nome} lancia un incantesimo su {bersaglio.nome} per {danno} danni!"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        bersaglio.subisci_danno(danno)

    def recupera_salute(self, mod_ambiente: int = 0) -> None:
        recupero = int((self.salute + mod_ambiente) * 0.2)
        nuova_salute = min(self.salute + recupero, 80)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        msg = f"{self.nome} medita e recupera {effettivo} HP. Salute attuale: {self.salute}"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)


@SerializableMixin.register_class
class Guerriero(Personaggio):
    def __init__(self, nome: str) -> None:
        super().__init__(nome)
        self.salute = 120

    def attacca(self, bersaglio: Personaggio, mod_ambiente: int = 0) -> None:
        danno = random.randint(self.attacco_min + 15, self.attacco_max + mod_ambiente + 20)
        msg = f"{self.nome} colpisce con la spada {bersaglio.nome} per {danno} danni!"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        bersaglio.subisci_danno(danno)

    def recupera_salute(self, mod_ambiente: int = 0) -> None:
        recupero = 30 + mod_ambiente
        nuova_salute = min(self.salute + recupero, 120)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        msg = f"{self.nome} si fascia le ferite e recupera {effettivo} HP. Salute attuale: {self.salute}"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)


@SerializableMixin.register_class
class Ladro(Personaggio):
    def __init__(self, nome: str) -> None:
        super().__init__(nome)
        self.salute = 140

    def attacca(self, bersaglio: Personaggio, mod_ambiente: int = 0) -> None:
        danno = random.randint(self.attacco_min + 5, self.attacco_max + 5) + mod_ambiente
        msg = f"{self.nome} colpisce furtivamente {bersaglio.nome} per {danno} danni!"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        bersaglio.subisci_danno(danno)

    def recupera_salute(self, mod_ambiente: int = 0) -> None:
        recupero = random.randint(10, 40) + mod_ambiente
        nuova_salute = min(self.salute + recupero, 140)
        effettivo = nuova_salute - self.salute
        self.salute = nuova_salute
        msg = f"{self.nome} si cura rapidamente e recupera {effettivo} HP. Salute attuale: {self.salute}"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)