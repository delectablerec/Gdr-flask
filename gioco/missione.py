import random
from  utils.log import Log
from utils.salvataggio import SerializableMixin

from personaggi.personaggio import Personaggio
from personaggi.classi import Mago, Guerriero, Ladro
from ambienti.ambiente import Ambiente, Vulcano, Foresta, Palude
from oggetti.oggetto import Oggetto, PozioneCura, BombaAcida, Medaglione
from inventario.inventario import Inventario
from utils.salvataggio import SerializableMixin, Json

@SerializableMixin.register_class
class Missione(SerializableMixin):
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
    def __init__(self, nome:str, ambiente : Ambiente, nemici : list[Personaggio], premi: list[Oggetto])->None :

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
        testo = f"{nemico} rimosso dalla lista nemici della missione"
        print(testo)
        Log.scrivi_log(testo)
        Json.scrivi_dati("data/salvataggio.json",Json.applica_patch(self.to_dict()))

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
            testo = f"Missione '{self.nome}' completata"
            print(testo)
            Log.scrivi_log(testo)
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
                raise ValueError("Non è possibile assegnare un premio ad un inventario senza un personaggio")
            inventario.aggiungi(premio)
            testo = f"Premio {premio.nome} aggiunto all'inventario di {inventario.proprietario.nome} "
            print(testo)
            Log.scrivi_log(testo)
            dati_da_salvare = [self.to_dict(), inventario.to_dict()]
            for dati in dati_da_salvare:
                Json.scrivi_dati("data/salvataggio.json",Json.applica_patch(dati))

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


#Lista delle missioni
@SerializableMixin.register_class
class GestoreMissioni(SerializableMixin):
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
        culto = Missione("Sgomina il culto di Graz'zt sul vulcano Gheemir", Vulcano(),[Mago("Cultista1"), Mago("Cultista2"), Mago("Cultista3")],[PozioneCura(),Medaglione()])
        return [imboscata, salva_principessa, culto]

    def mostra(self)->None:
        """
        Mostra le missioni disponibili

        Args:
            None

        Returns:
            None
        """
        print("Missioni disponibili:")
        for missione in self.lista_missioni:
            print(f"-{missione.nome}")
        #print(f"-{indx}  {missione.nome}" for indx, missione in enumerate(self.lista_missioni, start=1) if not missione.completata)

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
                testo = f"Missione : {missione.nome} completata"
                missione.attiva = False
                print(testo)
                Log.scrivi_log(testo)
        Json.scrivi_dati("data/salvataggio.json",Json.applica_patch(self.to_dict()))
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
            raise ValueError("Non ci sono missioni non completate ")
        except ValueError as e :
            print(f"Errore: {e}")
            return None