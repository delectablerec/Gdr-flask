import uuid
from gioco.basic import Basic
from gioco.oggetto import Oggetto
from gioco.personaggio import Personaggio
from gioco.ambiente import Ambiente
from utils.messaggi import Messaggi
# from utils.log import Log
#  , Json
#  

class Inventario(Basic):
    """
    Gestisce la lista di oggetti posseduto da ogni personaggio
    Sarà la classe inventario a gestire le istanze di classe Oggetto
    """
    def __init__(self, proprietario : Personaggio = None )->None:
        self.id = str(uuid.uuid4())
        self.oggetti = []
        self.proprietario = proprietario

    def aggiungi_oggetto(self, oggetto: Oggetto)->None:
        """
        Aggiungi un oggetto all'inventario.
        la stringa di testo viene aggiunta alla stringa di messaggi

        Args:
            oggetto (Oggetto): L'oggetto da aggiungere all'inventario.

        Return:
            None

        """
        self._aggiungi(oggetto)
        msg = f"Aggiunto l'oggetto '{oggetto.nome}' all inventario. "
        Messaggi.add_to_messaggi(msg)

    def _aggiungi(self, oggetto: Oggetto)-> None:
        """
        Aggiunge un oggetto all'inventario il metodo al momento è previsto come
        interno alla classe, ma può essere usato anche fuori.
        Serve sia allo scopo di  aggiungere un oggetto all'inventario senza
        un messaggio di ritorno (opzionale) sia per non mostrare direttamente
        con un append la lista oggetti qualora servisse anche esternamente.

        Args:
            oggetto (Oggetto): L'oggetto da aggiungere all'inventario.

        Return:
            None
        """
        self.oggetti.append(oggetto)

    def cerca_oggetto(self, oggetto: Oggetto)-> bool | None:
        """
        cerca un oggetto specifico nell'inventario
        ritorna true se è presente o false se non c'è
        se avviene un errore ritorna None e aggiunge un messaggio di errore
        alla stringa di messaggi.

        Args:
            oggetto (Oggetto): l'elemento da cercare all'interno della lista interna oggetti

        Returns:
            found (bool): risultato previsto della funzione per cercare un oggetto specifico
                ritorna true se viene trovato
                ritorna false se non è presente

            None.
        """
        msg =""
        try:
            found = False
            for obj in self.oggetti:
                if obj is oggetto:
                    found = True
                    break
            return found
        except Exception as e:
            msg = f"Errore generico: {e}"
            Messaggi.add_to_messaggi(msg)

    def mostra_inventario(self)->None:
        """
        invia una stringa con la lista dei nomi degli oggetti presenti
        alla classe Messaggi.

        Args:
            None

        Return:
            None.

        """
        msg = ""
        if len(self.oggetti) == 0:
            msg = "L'inventario è vuoto."
        else:
            msg = "Inventario :\n"
            for oggetto in self.oggetti :
                msg +=f"-{oggetto.nome}\n"
        Messaggi.add_to_messaggi(msg)

    def mostra_lista_inventario(self)-> list[Oggetto] | str:
        """
        metodo che ritorna la lista degli oggetti presenti nell'inventario
        o invia una stringa a Messaggi per avvisare che l'inventario è vuoto:

        Args:
            None

        Return:
            list[Oggetto]: lista degli oggetti nell'inventario
            None: in questo caso viene utilizzarto il metodo statico add_to_messaggi
            della classe Messaggi per inviare l'invformazione che l'inventario è vuoto.

        """
        if len(self.oggetti) == 0:
            msg = "L'inventario è vuoto."
            Messaggi.add_to_messaggi(msg)
        else:
            return self.oggetti

    def usa_oggetto(
        self,
        oggetto : Oggetto,
        utilizzatore: Personaggio = None,
        bersaglio: Personaggio = None,
        ambiente: Ambiente = None)->None:
        """
        Utilizza un oggetto presente nell'inventario.

        Args:
            oggetto (Oggetto): oggetto da usare.
            utilizzatore (Personaggio): Il Personaggio che usa l'oggetto se non passato
            si proverà ad utilizzare quello presente in self.Proprietario se presente.
            bersaglio(Any): None di Default è un parametro opzionale che
            permette di usare un oggetto su un altro Personaggio che non sia l'utilizzatore.
            ambiente (Ambiente): L'ambiente può alterare il funzionamento degli
            oggetti

        Return:
            None

        """
        msg = ""
        if not utilizzatore and self.proprietario:
            utilizzatore=self.proprietario
        elif not utilizzatore and not self.proprietario:
            msg = "manca l'utilizzatore"
        elif self.cerca_oggetto(oggetto):
            msg = "l'oggetto non è stato trovato nell'inventario"
        else:
            if not bersaglio:
                bersaglio = utilizzatore
            if ambiente is None:
                mod_ambiente = 0
            else:
                mod_ambiente, msg = ambiente.modifica_effetto_oggetto(oggetto)
                msg += "\n"
            msg += oggetto.usa(
                utilizzatore,
                bersaglio,
                mod_ambiente=mod_ambiente
            )
            self.oggetti.remove(oggetto)
        #
        # dati_salvataggio = [self.to_dict(), bersaglio.to_dict()]
        # for dati in dati_salvataggio:
        #     Json.scrivi_dati("data/salvataggio.json", Json.applica_patch(dati))
        Messaggi.add_to_messaggi(msg)

    def riversa_inventario(self, da_inventario : 'Inventario')-> None:
        """
        Permette ad un inventario di prendere tutti gli oggetti di un altro inventario(da_inventario)

        Args:
            da_inventario(Inventario): L'inventario da cui vengono prelevati tutti gli oggetti.

        Return:
            None

        """
        msg = ""
        if len(da_inventario.oggetti) != 0 :
            if self.proprietario == None:
                msg = "Inseriti nell'inventario : "
                # Log.scrivi_log("Oggetti trasferiti da un inventario a un altro. ")
            else:
                msg = f"{self.proprietario.nome} raccoglie :"
                # Log.scrivi_log(f"{self.proprietario.nome} ha raccolto oggetti dall'inventario di un altro personaggio. ")
            for oggetto in da_inventario.oggetti :
                msg= f"\n - {oggetto.nome}"
                # Log.scrivi_log(f"{oggetto.nome} trasferito nell'inventario. ")
                self._aggiungi(oggetto)
            da_inventario.oggetti.clear()
        else:
            if da_inventario.proprietario == None:
                msg = "l'inventario è vuoto."
            else:
                msg = f"L'inventario di {da_inventario.proprietario.nome} è vuoto"
            # Log.scrivi_log(msg)
        Messaggi.add_to_messaggi(msg)

    def to_dict(self) -> dict:
        """
        Serializza l'inventario in un dizionario.

        Returns:
            dict: Rappresentazione dell'inventario come dizionario.
        """
        return {
            'classe': self.__class__.__name__,
            'id': str(self.id),
            'oggetti': [oggetto.to_dict() for oggetto in self.oggetti],
            'proprietario': self.proprietario if self.proprietario else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Inventario':
        """
        Deserializza un dizionario in un oggetto Inventario.

        Args:
            data (dict): Il dizionario da deserializzare.

        Returns:
            Inventario: L'oggetto Inventario deserializzato.
        """
        inventario = cls()
        inventario.id = data.get('id', str(uuid.uuid4()))
        inventario.oggetti = [
            Oggetto.from_dict(oggetto) for oggetto in data.get('oggetti', [])
        ]

        inventario.proprietario = data['proprietario'] if data.get('proprietario') else None

        return inventario
