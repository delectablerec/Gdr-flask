import random
from utils.log import Log
from utils.salvataggio import SerializableMixin
from gioco.personaggio import Personaggio
from gioco.classi import Mago, Guerriero, Ladro
from gioco.ambiente import Ambiente, Vulcano, Foresta, Palude
from gioco.oggetto import Oggetto, PozioneCura, BombaAcida, Medaglione
from gioco.inventario import Inventario
from utils.salvataggio import SerializableMixin, Json

@SerializableMixin.register_class
class Missione(SerializableMixin):

    def __init__(self, nome:str, ambiente : Ambiente, nemici : list[Personaggio], premi: list[Oggetto])->None :

        # inizializzazione attributi
        self.nome = nome
        self.ambiente = ambiente  # ereditato dal torneo corrente
        self.nemici = nemici  # lista dei nemici di tutti i tornei
        self.premi = premi  # supporta premio singolo o multiplo
        self.completata = False  # flag per premio in inventario
        self.attiva = False
    def get_nemici(self)->list[Personaggio]:
        return self.nemici

    def rimuovi_nemico(self, nemico : Personaggio)->None:
        self.nemici.remove(nemico)
        testo = f"{nemico} rimosso dalla lista nemici della missione"
        Log.scrivi_log(testo)
        Json.scrivi_dati("data/salvataggio.json",Json.applica_patch(self.to_dict()))

    def rimuovi_nemici_sconfitti(self)->None:
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
        if len(self.nemici) == 0:
            self.completata = True
            testo = f"Missione '{self.nome}' completata"
            Log.scrivi_log(testo)
            return True
        return False

    # aggiunge premio all'inventario del giocatore se la missione è completata
    def assegna_premio(self, inventari_giocatori : list[Inventario] )->None:
        for premio in self.premi:
            inventario = random.choice(inventari_giocatori)
            if inventario.proprietario == None :
                raise ValueError("Non è possibile assegnare un premio ad un inventario senza un personaggio")
            inventario.aggiungi(premio)
            testo = f"Premio {premio.nome} aggiunto all'inventario di {inventario.proprietario.nome} "
            Log.scrivi_log(testo)
            dati_da_salvare = [self.to_dict(), inventario.to_dict()]
            for dati in dati_da_salvare:
                Json.scrivi_dati("data/salvataggio.json",Json.applica_patch(dati))

    #QUESTO METODO E' PROVVISORIO
    def check_missione(self, inventari_vincitori : list[Inventario] )->None:
        self.rimuovi_nemici_sconfitti()
        if self.verifica_completamento():
            self.assegna_premio(inventari_vincitori)

    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON."""
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
        """Ricostruisce l’istanza a partire da un dict serializzato."""
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
@SerializableMixin.register_class
class GestoreMissioni(SerializableMixin):
    """
    È un gestore di istanze della classe Missione, e le gestisce con diversi metodi
    """

    def __init__(self)->None:
        #La proprietà principale di Missioni sarà una lista di oggetti Missione
        self.lista_missioni = self.setup()

    def setup(self)->list[Missione]:
         #Istanzio le missioni
        imboscata = Missione("Imboscata", Foresta(), [Guerriero("Robin Hood"), Guerriero("Little Jhon")], [PozioneCura(),PozioneCura(),BombaAcida()])
        salva_principessa = Missione("Salva la principessa", Palude(),[Ladro("Megera furfante")],[Medaglione()])
        culto = Missione("Sgomina il culto di Graz'zt sul vulcano Gheemir", Vulcano(),[Mago("Cultista1"), Mago("Cultista2"), Mago("Cultista3")],[PozioneCura(),Medaglione()])
        return [imboscata, salva_principessa, culto]

    def mostra(self)->None:
        testo = ("Missioni disponibili:")
        Log.scrivi_log(testo)
        for missione in self.lista_missioni:
            testo = f"-{missione.nome}"
            Log.scrivi_log(testo)

    def finita(self)->bool:
        esito = True
        for missione in self.lista_missioni :
            if missione.completata == False :
                esito = False
            if esito == True:
                testo = f"Missione : {missione.nome} completata"
                missione.attiva = False
                Log.scrivi_log(testo)
        Json.scrivi_dati("data/salvataggio.json",Json.applica_patch(self.to_dict()))
        return esito

    def sorteggia(self)-> Missione | None:
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
            testo = f"Errore: {e}"
            Log.scrivi_log(testo)
            return None

    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON."""
        return {
            "classe": self.__class__.__name__,
            "lista_missioni": [missione.to_dict() for missione in self.lista_missioni]
        }
    @classmethod
    def from_dict(cls, data: dict) -> "GestoreMissioni":
        """Ricostruisce l’istanza a partire da un dict serializzato."""
        gestore = cls()
        gestore.lista_missioni = [Missione.from_dict(missione) for missione in data.get("lista_missioni", [])]
        return gestore