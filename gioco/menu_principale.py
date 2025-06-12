from utils.interfaccia import InterfacciaUtente as IU
from utils.salvataggio import Json, SerializableMixin
from personaggi.personaggio import Personaggio
from personaggi.classi import Guerriero, Ladro, Mago
from inventario.inventario import Inventario
from oggetti.oggetto import Oggetto, PozioneCura, BombaAcida, Medaglione
from ambienti.ambiente import Ambiente
from missioni.missione import Missione
from utils.salvataggio import SerializableMixin
from flask import Flask
from flask_session import Session
from gioco.routes import gioco
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '...'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.register_blueprint(gioco)

@SerializableMixin.register_class
class MenuPrincipale(SerializableMixin):
    """
    Gestisce il menu principale del gioco, inclusa la creazione di nuovi personaggi,
    il caricamento di giochi salvati e la generazione degli inventari iniziali.
    """

    def __init__(self)-> None:
        """
        Inizializza una nuova istanza della classe Menu.

        Args:
            None

        Attributes:
            giocatore (None): Riservato per eventuale giocatore principale (non ancora utilizzato).
            personaggi (list): Lista dei personaggi creati o caricati.
            inventari (list): Lista degli inventari associati ai personaggi.
            personaggi_inventari (list): Lista di tuple (Personaggio, Inventario).

        Returns:
            None
        """
        self.giocatore = None
        self.personaggi = []
        self.inventari = []
        self.personaggi_inventari = []
        self.nemici = []
        self.ambiente = None
        self.missione = None
    def mostra_menu(self) -> None:
        """
        Mostra il menu principale all'utente per scegliere tra un nuovo gioco(1)
        o il caricamento di un gioco salvato(2).

        Args:
            None

        Returns:
            None
        """
        opzioni = ["1"]
        if os.path.exists("data/salvataggio.json"):
            opzioni.append("2")
        scelta = IU.chiedi_input("1: Nuovo Gioco\n" + ("2: Gioco Salvato\n" if "2" in opzioni else "") + "Scegli: ", opzioni=opzioni)
        if scelta == "1":
            self.crea_nuovo_salvataggio()
        if scelta == "2":
            self.carica_salvataggio()

    def crea_nuovo_salvataggio(self)-> None:
        """
        Avvia una nuova partita chiedendo all'utente quanti personaggi creare.
        Per ogni personaggio creato viene generato un inventario iniziale.
        """
        if os.path.exists("data/salvataggio.json"):
            os.remove("data/salvataggio.json")
        num_personaggi = IU.chiedi_numero("Quanti personaggi vuoi creare? : ", minimo=1)
        for _ in range(num_personaggi):
            personaggio = self.crea_personaggio()
            self.personaggi.append(personaggio)
            zaino_personaggio = self.crea_inventario(personaggio)
            self.inventari.append(zaino_personaggio)
            self.personaggi_inventari.append((personaggio, zaino_personaggio))

    def carica_salvataggio(self) -> None:
        dati = Json.carica_dati("data/salvataggio.json")
        if dati is None:
            print("Errore nel caricamento del salvataggio.")
            return

        self.personaggi_inventari = []
        self.nemici = []

        personaggi_dati = dati.get("personaggi", [])
        inventari_dati = dati.get("inventari", [])

        if len(personaggi_dati) != len(inventari_dati):
            print("Attenzione: numero di personaggi e inventari non corrispondono.")

        for i, pg_dict in enumerate(personaggi_dati):
            pg = SerializableMixin.from_dict(pg_dict)
            inv = SerializableMixin.from_dict(inventari_dati[i]) if i < len(inventari_dati) else None
            self.personaggi_inventari.append((pg, inv))

   
        nemici_dati = dati.get("nemici", [])
        inventari_nemici_dati = dati.get("inventari_nemici", [])

        if len(nemici_dati) != len(inventari_nemici_dati):
            print("Attenzione: numero di nemici e inventari nemici non corrispondono.")

        for i, nem_dict in enumerate(nemici_dati):
            personaggio = SerializableMixin.from_dict(nem_dict.get("personaggio", {}))
            inventario = SerializableMixin.from_dict(inventari_nemici_dati[i]) if i < len(inventari_nemici_dati) else None
            strategia_attacco = None  # TODO: deserializza la strategia se necessario
            self.nemici.append((personaggio, strategia_attacco, inventario))

        gestore_missioni_dict = dati.get("gestore_missioni") or dati.get("missioni")
        if gestore_missioni_dict:
            self.gestore_missioni = SerializableMixin.from_dict(gestore_missioni_dict)
        else:
            print("Nessun dato missioni trovato nel salvataggio.")
            self.gestore_missioni = None



    print("Salvataggio caricato correttamente.")
    def crea_personaggio(self) -> Personaggio:
        """
        Crea un nuovo personaggio tramite input utente.

        Args:
            None

        Returns:
            Personaggio(object): L'istanza del personaggio creato.
        """
        print("Crea un nuovo personaggio\n")
        pg_name = IU.chiedi_input("Nome del personaggio : ")
        classi_disponibili = [Ladro, Guerriero, Mago]
        for indx, classe in enumerate(classi_disponibili, start=1):
            print(f"{indx}- {classe.__name__}")
        idnx_pg_classe = IU.chiedi_numero("Classe del personaggio : ", minimo=1, massimo=len(classi_disponibili))
        pg = classi_disponibili[idnx_pg_classe - 1](pg_name)
        return pg

    def crea_inventario(self, pg: Personaggio = None) -> Inventario:
        """
        Crea un inventario iniziale per un personaggio e permette di scegliere un oggetto iniziale.

        Args:
            pg (Personaggio, optional): Il personaggio a cui assegnare l'inventario.

        Returns:
            Inventario(object): L'inventario creato con l'oggetto iniziale selezionato.
        """
        zaino = Inventario(proprietario=pg)
        print("Cominci la tua avventura con un :")
        oggetti_disponibili = [PozioneCura, BombaAcida, Medaglione]
        for indx, obj in enumerate(oggetti_disponibili, start=1):
            print(f"{indx}- {obj.__name__}")
        indx_initial_gift = IU.chiedi_numero("Scegli :", minimo=1, massimo=len(oggetti_disponibili))
        zaino.aggiungi(oggetti_disponibili[indx_initial_gift - 1]())
        return zaino