from gioco.personaggio import Personaggio
from utils.log import Log
 
from utils.messaggi import Messaggi

# Modulo oggetti
# Contiene la classe base Oggetto e le classi derivate
 
class Oggetto ():
    """
    Classe padre di tutti gli oggetti contenibili nell'inventario
    """
    def __init__(self, nome: str, offensivo: bool = False) -> None:
        """
        Inizializza un oggetto con nome e tipo

        Args:
            nome (str): Nome dell'oggetto
            tipo (str): Tipo dell'oggetto
            offensivo (bool): Se l'oggetto è offensivo o meno (default: False)

        Returns:
            None

        """
        self.nome = nome
        self.usato = False
        self.offensivo = offensivo
        self.messaggi = ""
    

    def usa(
            self,
            utilizzatore: Personaggio,
            bersaglio: bool = None,
            mod_ambiente: int = 0
            ) -> None:
        """
        Metodo da implementare in ogni oggetto

        Args:
            utilizzatore (Personaggio): Personaggio che usa l'oggetto
            bersaglio (Personaggio): Personaggio bersaglio dell'oggetto
            mod_ambiente (int): variabile dell'Ambiente in cui si trova l'oggetto

        Returns:
            None
        """
        raise NotImplementedError("Questo oggetto non ha effetto definito.")
    
    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON.

        Returns:
            dict: Dizionario del materiale serializzato
        """
        return {
            "classe": self.__class__.__name__,
            "nome": self.nome,
            "usato": self.usato,
            "offensivo": self.offensivo,
            "messaggi": self.messaggi
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Oggetto":
        """Ricostruisce l’istanza a partire da un dict serializzato.

        Args:
            data (dict): Dati serializzati

        Returns:
            Ambiente: Dati deserializzati
        """
        oggetto = cls(nome=data["nome"])
        oggetto.usato = data.get("usato", False)
        oggetto.messaggi = data.get("messaggi", "")
        return oggetto

 
class PozioneCura(Oggetto):
    """
    Cura il personaggio che la usa di un certo valore
    """
    def __init__(
            self,
            nome: str = "Pozione Rossa",
            valore: int = 30
            ) -> None:
        """
        Inizializza una pozione di cura

        Args:
            nome (str): Nome della pozione
            valore (int): Valore di cura della pozione

        Returns:
            None
        """
        super().__init__(nome)
        self.valore = valore

    def usa(self,
            utilizzatore: Personaggio,
            bersaglio: Personaggio = None,
            mod_ambiente: int = 0
            ) -> None:
        """
        Cura il personaggio che la usa di un certo valore

        Args:
            utilizzatore (Personaggio): Personaggio che usa la pozione
            bersaglio (Personaggio): Personaggio bersaglio della pozione
            mod_ambiente (int): variabile dell'Ambiente in cui si trova l'oggetto

        Returns:
            None
        """
        if bersaglio is None:
            target = utilizzatore
            msg = "su se stesso"
        else:
            target = bersaglio
            msg = f"su {bersaglio.nome}"
        target.salute = min(target.salute + self.valore + mod_ambiente, target.salute_max)
        text = f"{utilizzatore.nome} usa {self.nome} {msg} e ripristinando {self.valore + mod_ambiente} salute!"
        Messaggi.add_to_messaggi(text)
        Log.scrivi_log(text)
        self.usato = True
        
    def to_dict(self) -> dict:
        return {
            "classe": self.__class__.__name__,
            "nome": self.nome,
            "usato": self.usato,
            "offensivo": self.offensivo,
            "messaggi": self.messaggi
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PozioneCura":
        """Ricostruisce l’istanza a partire da un dict serializzato.

        Args:
            data (dict): Dati serializzati

        Returns:
            Ambiente: Dati deserializzati
        """
        oggetto = cls(nome=data["nome"], valore=data["valore"])
        oggetto.usato = data.get("usato", False)
        return oggetto

 
class BombaAcida(Oggetto):
    """
    Infligge danno pari al valore(Proprietà)
    """
    def __init__(self, nome: str = "Bomba Acida", danno: int = 30) -> None:
        """
        Inizializza una bomba acida

        Args:
            nome (str): Nome della bomba
            danno (int): Danno inflitto dalla bomba (dafault: 30)

        Returns:
            None
        """
        super().__init__(nome, offensivo=True)
        self.danno = danno

    def usa(self, utilizzatore: Personaggio, bersaglio: Personaggio = None, mod_ambiente: int = 0) -> None:
        """
        Infligge danno al bersaglio

        Args:
            utilizzatore (Personaggio): Personaggio che usa la bomba
            bersaglio (Personaggio): Personaggio bersaglio della bomba
            mod_ambiente (int): variabile dell'Ambiente in cui si trova l'oggetto

        Returns:
            None
        """
        if bersaglio is None:
            msg= f"{utilizzatore.nome} cerca di usare {self.nome}, ma non ha un bersaglio!"
            Messaggi.add_to_messaggi(msg)
            Log.scrivi_log(msg)
            return
        bersaglio.subisci_danno(self.danno + mod_ambiente)
        msg = f"{utilizzatore.nome} lancia {self.nome} su {bersaglio.nome}, infliggendo {self.danno + mod_ambiente} danni!"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        msg = f"A {bersaglio.nome} resta {bersaglio.salute} salute"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        self.usato = True
        
    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON.

        Returns:
            dict: Dizionario del materiale serializzato
        """
        data = super().to_dict()
        data.update({
            "danno": self.danno
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "BombaAcida":
        """Ricostruisce l’istanza a partire da un dict serializzato.

        Args:
            data (dict): Dati serializzati

        Returns:
            Ambiente: Dati deserializzati
        """
        oggetto = cls(nome=data["nome"], danno=data["danno"])
        oggetto.usato = data.get("usato", False)
        return oggetto

 
class Medaglione(Oggetto):
    """
    Incrementa l'attacco_max del personaggio che lo usa
    """
    def __init__(self) -> None:
        """
        Inizializza un medaglione

        Args:
            None

        Returns:
            None
        """
        super().__init__("Medaglione")

    def usa(self, utilizzatore: 'Personaggio', bersaglio: 'Personaggio' = None, mod_ambiente: int = 0) -> None:
        """
        Incrementa l'attacco_max del personaggio che lo usa

        Args:
            utilizzatore (Personaggio): Personaggio che usa il medaglione
            bersaglio (Personaggio): Personaggio bersaglio del medaglione
            mod_ambiente (int): variabile dell'Ambiente in cui si trova l'oggetto

        Returns:
            None
        """
        target = bersaglio if bersaglio else utilizzatore
        target.attacco_max += 10 + mod_ambiente
        msg = f"{target.nome} indossa {self.nome}, aumentando il suo attacco massimo!"
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        self.usato = True
        
    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON.

        Returns:
            dict: Dizionario del materiale serializzato
        """
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict) -> "Medaglione":
        """Ricostruisce l’istanza a partire da un dict serializzato.

        Args:
            data (dict): Dati serializzati

        Returns:
            Ambiente: Dati deserializzati
        """
        oggetto = cls()
        oggetto.usato = data.get("usato", False)
        return oggetto
