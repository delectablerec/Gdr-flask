from oggetti.oggetto import Oggetto
from personaggi.personaggio import Personaggio
from ambienti.ambiente import Ambiente
from utils.log import Log
from utils.interfaccia import InterfacciaUtente as IU
from utils.salvataggio import SerializableMixin, Json
@SerializableMixin.register_class

class Inventario(SerializableMixin):
    """
    Gestisce la lista di oggetti posseduto da ogni personaggio
    Sarà la classe inventario a gestire le istanze di classe Oggetto
    """
    def __init__(self, proprietario : Personaggio = None )->None:
        self.oggetti = []
        self.proprietario = proprietario

    def aggiungi(self, oggetto: Oggetto)->None:
        """
        Aggiungi un oggetto all'inventario.

        Args:
            oggetto (Oggetto): L'oggetto da aggiungere all'inventario.

        Return:
            None

        """
        self.oggetti.append(oggetto)
        #Log.scrivi_log(f"Aggiunto l'oggetto '{oggetto.nome}' all inventario. ")

    def usa_oggetto(self, oggetto : Oggetto, bersaglio= None, ambiente: Ambiente = None)->None:
        """
        Utilizza un oggetto presente nell'inventario.

        Args:
            oggetto (Oggetto): oggetto da usare.
            utilizzatore (Personaggio): Il Personaggio che usa l'oggetto.
            bersaglio(Any): None di Default è un parametro opzionale che
            permette di usare un oggetto su un altro Personaggio che non sia l'utilizzatore.

        Return:
            None

        """
        if self.proprietario :
            utilizzatore = self.proprietario
            for obj in self.oggetti :
                if obj is oggetto :
                    if ambiente is None:
                        mod_ambiente = 0
                    else:
                         mod_ambiente = ambiente.modifica_effetto_oggetto(oggetto)
                    oggetto.usa(utilizzatore, bersaglio, mod_ambiente=mod_ambiente)
                    self.oggetti.remove(oggetto)
                    return
            testo = f"{utilizzatore.nome} non ha {oggetto.nome}."
            print(testo)
            Log.scrivi_log(testo)
        else:
            print("Per usare un oggetto, l'inventario deve avere un proprietario")

    def cerca_e_usa(self, bersaglio=None, ambiente : Ambiente = None )-> None:
        """
        Mostra gli oggetti contenuti nell'inventario e permette di scegliere
        l'oggetto da usare attraverso l'indice.
        Chiama il metodo usa_oggetto

        Args:
            bersaglio(Any): Parametro opzionale , bersaglio su cui utilizzare
            l'oggetto se offensivo.
            ambient(Ambiente): L'ambiente può alterare il funzionamento degli
            oggetti.

        Return:
            None
        """
        if len(self.oggetti)!= 0:
            print("Inventario :")
            for indx, obj in enumerate(self.oggetti, start=1):
                print(f"{indx}- {obj.nome}")
            idx_obj_scelto = IU.chiedi_numero("Quale oggetto vuoi usare ? ",minimo= 1,massimo= len(self.oggetti))
            self.usa_oggetto(self.oggetti[idx_obj_scelto], bersaglio=bersaglio, ambiente=ambiente )
        else:
            testo= "L'inventario è vuoto"
            print(testo)
            Log.scrivi_log(testo)

    def cerca_e_usa_multi(
            self,
            bersagli: list[Personaggio] = None,
            ambiente: Ambiente = None
    ) -> None:

        """
        Mostra gli oggetti contenuti nell'inventario e permette di scegliere
        l'oggetto da usare attraverso l'indice.
        Chiama il metodo usa_oggetto

        Args:
            bersagli (list(Any)): Parametro opzionale , bersaglio su cui
            utilizzare l'oggetto
            ambiente (Ambiente): L'ambiente può alterare il funzionamento degli
            oggetti

        Return:
            None
        """
        if len(self.oggetti) != 0:
            print("Inventario :")
            for indx, obj in enumerate(self.oggetti, start=1):
                print(f"{indx}- {obj.nome}")
            print(f"{len(self.oggetti) + 1}- esci dall'inventario")
            n_scelte_obj = len(self.oggetti)+1
            idx_obj_scelto = -1 + IU.chiedi_numero(
                "Quale oggetto vuoi usare ? ",
                minimo=1,
                massimo= n_scelte_obj
            )
            if idx_obj_scelto+1 == n_scelte_obj :  # se scelgo nessuno
                print("Nessun oggetto scelto. si esce dall'inventario")
                return

            # situazioni particolari
            if bersagli is None:
                bersagli = []

            # se anziché una lista di bersagli è un Personaggio singolo
            if isinstance(bersagli, Personaggio):
                bersagli = [bersagli]
            if self.proprietario not in bersagli:
                # Aggiungo il proprietario come bersaglio disponibile
                # se non è già presente nella lista dei bersagli
                bersagli.append(self.proprietario)

            # stampo i possibili bersagli dell'effetto
            for indx, bers in enumerate(bersagli, start=1):
                print(f"{indx}- {bers.nome} ({bers.salute}/{bers.salute_max})")
            n_scelte_bersagli = len(bersagli)+1
            print(f"{n_scelte_bersagli}- nessuno")
            indx_bers_scelto =-1 + IU.chiedi_numero(
                "Su chi lo vuoi usare ? ",
                minimo=1,
                massimo= n_scelte_bersagli
            )
            if indx_bers_scelto +1 == n_scelte_bersagli :  # se scelgo nessuno
                bersaglio_scelto = None
            else:
                bersaglio_scelto = bersagli[indx_bers_scelto]

            self.usa_oggetto(
                self.oggetti[idx_obj_scelto],
                bersaglio=bersaglio_scelto,
                ambiente=ambiente
            )
        else:
            testo = "L'inventario è vuoto"
            print(testo)
            Log.scrivi_log(testo)
        dati_salvataggio = [self.to_dict(), bersaglio_scelto.to_dict()]
        for dati in dati_salvataggio:
            Json.scrivi_dati("data/salvataggio.json", Json.applica_patch(dati))

    def mostra(self)->None:
        """
        Stampa il contenuto dell'inventario.

        Args:
            None

        Return:
            None

        """
        print("Inventario :")
        for oggetto in self.oggetti :
            print(f"-{oggetto.nome}")

    def riversa(self, da_inventario : 'Inventario')->None:
        """
        Permette ad un inventario di prendere tutti gli oggetti di un altro inventario(da_inventario)

        Args:
            da_inventario(Inventario): L'inventario da cui vengono prelevati tutti gli oggetti.

        Return:
            None

        """
        if len(da_inventario.oggetti) != 0 :
            if self.proprietario == None:
                print("Inseriti nell'inventario : ")
                Log.scrivi_log("Oggetti trasferiti da un inventario a un altro. ")
            else:
                print(f"{self.proprietario.nome} raccoglie :")
                Log.scrivi_log(f"{self.proprietario.nome} ha raccolto oggetti dall'inventario di un altro personaggio. ")
            for oggetto in da_inventario.oggetti :
                print(f" - {oggetto.nome}")
                Log.scrivi_log(f"{oggetto.nome} trasferito nell'inventario. ")
                self.aggiungi(oggetto)
            da_inventario.oggetti.clear()
        else:
            if da_inventario.proprietario == None:
                testo = "l'inventario è vuoto."
            else:
                testo = f"L'inventario di {da_inventario.proprietario.nome} è vuoto"
            print(testo)
            Log.scrivi_log(testo)