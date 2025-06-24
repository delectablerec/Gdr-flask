import random
#from utils.log import Log
# 
from gioco.personaggio import Personaggio
from gioco.classi import Mago, Guerriero, Ladro
from gioco.ambiente import Ambiente, Vulcano, Foresta, Palude
from gioco.oggetto import Oggetto, PozioneCura, BombaAcida, Medaglione
from gioco.inventario import Inventario
# , Json
from utils.messaggi import Messaggi

#  
class Missione():
    """
    Si occupa di aggregare istanze di ambiente , nemici e ricompense
    Rappresenta una missione, composta da un ambiente, nemici e premi.
    """
    def __init__(self, nome:str, ambiente : Ambiente, nemici : list[Personaggio], premi: list[Oggetto])->None :
        """
    Si occupa di aggregare istanze di ambiente , nemici e ricompense
    Rappresenta una missione, composta da un ambiente, nemici e premi.

    Args:
        nome (str): Il nome della missione
        ambiente (Ambiente) : L'istanza di ambiente necessaria per applicare gli effetti ambientali durante la missione.
        nemici (list[Personaggio]): Lista di nemici della missione
        premi (list[Oggetto]): Lista delle ricompense

    Returns:
        None
    """
        # inizializzazione attributi
        self.nome = nome
        self.ambiente = ambiente  # ereditato dal torneo corrente
        self.nemici = nemici  # lista dei nemici di tutti i tornei
        self.premi = premi  # supporta premio singolo o multiplo
        self.completata = False  # flag per premio in inventario
        self.attiva = False

    def get_nemici(self)->list[Personaggio]:
        """
        Metodo get per ottenere la lista di nemici dentro missione

        Args:
            None

        Returns:
            list[Personaggio] : Ritorna la lista di nemici della Missione

        """
        return self.nemici

    def rimuovi_nemico(self, nemico : Personaggio)->None:
        """
        Rimuove un nemico dalla lista nemici della Missione
        Args:
        nemico (Personaggio): Nemico da rimuovere dalla lista

        Returns:
            None
        """
        self.nemici.remove(nemico)
        msg = f"{nemico} rimosso dalla lista nemici della missione"
        Messaggi.add_to_messaggi(msg)
        #Log.scrivi_log(msg)
        #Json.scrivi_dati("data/salvataggio.json",Json.applica_patch(self.to_dict()))

    def rimuovi_nemici_sconfitti(self)->None:
        """
        Rimuove i nemici sconfitti dalla proprietà lista nemici

        Args:
            None

        Returns:
            None
        """
        #Metto in una lista i nemici sconfitti che devo rinuovere
        lista_to_remove = []
        for nemico in self.nemici:
            if nemico.sconfitto():
                lista_to_remove.append(nemico)
        #Rimuovo i nemici sconfitti dalla proprietà nemici
        for nemico in lista_to_remove:
            self.rimuovi_nemico(nemico)

    # controlla se la lista self.nemici è vuota e nel caso restituisce True
    def verifica_completamento(self)-> bool :
        """
        Controllo che la lista di nemici sia vuota e in tal caso ritorna True,
        altrimenti False

        Args:
            None

        Returns:
            bool: True se la missione è completata, altrimenti False
        """
        if len(self.nemici) == 0:
            self.completata = True
            msg = f"Missione '{self.nome}' completata"
            Messaggi.add_to_messaggi(msg)
           # Log.scrivi_log(msg)
            return True
        return False

    # aggiunge premio all'inventario del giocatore se la missione è completata
    def assegna_premio(self, inventari_giocatori : list[Inventario] )->None:
        """
        Mette nell'inventario dei giocatori gli oggetti contenuti nella lista
        dei Premi (Proprietà di Missione) distribuendoli casualmente

        Args:
            inventari_giocatori (list[Inventario]): Inventari a cui assegnare il premio

        Returns:
            None

        """
        for premio in self.premi:
            inventario = random.choice(inventari_giocatori)
            if inventario.proprietario == None :
                msg="Non è possibile assegnare un premio ad un inventario senza un personaggio"
                Messaggi.add_to_messaggi(msg)
                raise ValueError(msg)
            inventario.aggiungi(premio)
            msg = f"Premio {premio.nome} aggiunto all'inventario di {inventario.proprietario.nome} "
            Messaggi.add_to_messaggi(msg)
           # Log.scrivi_log(msg)
            dati_da_salvare = [self.to_dict(), inventario.to_dict()]
            # for dati in dati_da_salvare:
            #     Json.scrivi_dati("data/salvataggio.json",Json.applica_patch(dati))

    #QUESTO METODO E' PROVVISORIO
    def check_missione(self, inventari_vincitori : list[Inventario] )->None:
        """
        Questo metodo mette insieme gli altri nella giusta sequenza:
        Idealmente andrebbe chiamato dopo ogni attacco del giocatore
        Rimuovi i nemici sconfitti. 
        Verifica completamento (dovrebbe funzionare anche con la lista dei nemici vuota)
        assegna il premio al giocatore_vincitore se la missione è completata

        Args:
            giocatore_vincitore (Personaggio): Usato per assegnargli il premio

        Returns:
            None
        """
        self.rimuovi_nemici_sconfitti()
        if self.verifica_completamento():
            self.assegna_premio(inventari_vincitori)

    def to_dict(self) -> dict:
        """
        Restituisce uno stato serializzabile per session o JSON.

        Returns:
            dict: Dizionario del materiale serializzato
        """
        return {
            "classe": self.__class__.__name__,
            "nome": self.nome,
            "ambiente": self.ambiente.to_dict(),
            "nemici": [nemico.to_dict() for nemico in self.nemici],
            "premi": [premio.to_dict() for premio in self.premi],
            "completata": self.completata,
            "attiva": self.attiva
        }
    @classmethod
    def from_dict(cls, data: dict) -> "Missione":
        """Ricostruisce l’istanza a partire da un dict serializzato.

        Args:
            data (dict): Dati serializzati

        Returns:
            Ambiente: Dati deserializzati
        """
        ambiente_cls = Ambiente.from_dict(data["ambiente"])
        nemici = [Personaggio.from_dict(nemico) for nemico in data.get("nemici", [])]
        premi = [Oggetto.from_dict(premio) for premio in data.get("premi", [])]
        missione = cls(
            nome=data["nome"],
            ambiente=ambiente_cls,
            nemici=nemici,
            premi=premi
        )
        missione.completata = data.get("completata", False)
        missione.attiva = data.get("attiva", False)
        return missione


#Lista delle missioni
# 
class GestoreMissioni():
#class GestoreMissioni ():
    """
    È un gestore di istanze della classe Missione, e le gestisce con diversi metodi
    """

    def __init__(self)->None:
        #La proprietà principale di Missioni sarà una lista di oggetti Missione
        self.lista_missioni = self.setup()

    def setup(self)->list[Missione]:
        """
        Istanzio le Missioni da fornire al GestoreMissioni,
        viene chiamato nel costruttore di GestoreMissioni

        Args:
            None

        Returns:
            list[Missione]: Ritorna una lista di istanze di classe Missione
        """
         #Istanzio le missioni
        imboscata = Missione("Imboscata", Foresta(), [Guerriero("Robin Hood"), Guerriero("Little Jhon")], [PozioneCura(),PozioneCura(),BombaAcida()])
        salva_principessa = Missione("Salva la principessa", Palude(),[Ladro("Megera furfante")],[Medaglione()])
        culto = Missione("Sgomina il culto di Graz'zt sul vulcano Gheemir", Vulcano(),[Mago("Cubista1"), Mago("Cultista2"), Mago("Cultista3")],[PozioneCura(),Medaglione()])
        return [imboscata, salva_principessa, culto]

    def mostra(self)->None:
        """
        Mostra le missioni disponibili

        Args:
            None

        Returns:
            None
        """
        msg = ("Missioni disponibili:")
        Messaggi.add_to_messaggi(msg)
        #Log.scrivi_log(msg)
        for missione in self.lista_missioni:
            msg = f"-{missione.nome}"
            # self.messaggi.add_to_messaggi(msg)
            #Log.scrivi_log(msg)

    def finita(self)->bool:
        """
        Controlla se in Missioni ci sono ancora missioni non completate in
        tal caso ritorna False, se tutte le missioni sono state completate
        ritorna True

        Args:
            None

        Returns:
            bool: Ritorna True se tutte le missioni sono state completate,
            altrimenti False
        """
        esito = True
        for missione in self.lista_missioni :
            if missione.completata == False :
                esito = False
            if esito == True:
                missione.attiva = False
                msg = f"Missione : {missione.nome} completata"
                Messaggi.add_to_messaggi(msg)
                #Log.scrivi_log(msg)
        #Json.scrivi_dati("data/salvataggio.json",Json.applica_patch(self.to_dict()))
        return esito

    def sorteggia(self)-> Missione | None:
        """
        Sorteggia una missione a caso tra quelle non completate in missioni e
        la ritorna , se non ci sono missioni non copletate ritorna False.

        Args:
            None

        Returns:
            Missione | None: Ritorna un'istanza di Missione non completata
            o None se il GestoreMissioni ha solo missioni completate
        """
        for missione in self.lista_missioni :
            if missione.attiva:
                return missione
        try:
            random.shuffle(self.lista_missioni)
            for missione in self.lista_missioni :
                if not missione.completata :
                    missione.attiva = True
                    return missione
            #Se non ci sono missioni che non siano state completate
            msg = "Non ci sono missioni non completate"
            raise ValueError(msg)
        except ValueError as e :
            msg = f"Errore: {e}"
            Messaggi.add_to_messaggi(msg)
            #Log.scrivi_log(msg)
            return None

    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON.

        Returns:
            dict: Dizionario del materiale serializzato
        """
        return {
            "classe": self.__class__.__name__,
            "lista_missioni": [missione.to_dict() for missione in self.lista_missioni]
        }
    @classmethod
    def from_dict(cls, data: dict) -> "GestoreMissioni":
        """Ricostruisce l’istanza a partire da un dict serializzato.

        Args:
            data (dict): Dati serializzati

        Returns:
            Ambiente: Dati deserializzati
        """
        gestore = cls()
        gestore.lista_missioni = [Missione.from_dict(missione) for missione in data.get("lista_missioni", [])]
        return gestore