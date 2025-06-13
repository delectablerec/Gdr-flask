import random

from utils.interfaccia import InterfacciaUtente
from utils.log import Log
from oggetti.oggetto import PozioneCura, BombaAcida, Medaglione
from inventario.inventario import Inventario
from missioni.missione import Missione
from personaggi.personaggio import Personaggio
from patterns.strategy_patterns import StrategiaAttacco, StrategiaAttaccoFactory
from gioco.turno import Turno
from utils.salvataggio import SerializableMixin, Json


@SerializableMixin.register_class
class Scontro:
    """
    Classe che gestisce uno scontro tra giocatori e nemici in una determinata missione.

    Questa classe si occupa di:
    - Inizializzare lo scontro con i dati di missione e personaggi.
    - Costruire e preparare la lista dei nemici con strategia e inventario.
    - Eseguire il ciclo di combattimento a turni.
    - Determinare l’esito finale (vittoria o sconfitta).
    - Stampare lo stato finale dei personaggi.
    """
    def __init__(self,
                 missione: Missione,
                 giocatori: list[tuple[Personaggio, Inventario]]
                ):
        self.missione = missione
        self.ambiente = missione.ambiente
        self.giocatori = giocatori
        self.nemici = self.setup_nemici(self.missione.get_nemici())
        self.counter_turni = 0
        self.inventari_nemici = []

    def crea_inventario_base(self, proprietario: Personaggio) -> Inventario:
        """
        Crea un inventario base per un personaggio nemico con oggetti standard.

        Args:
            proprietario (Personaggio): Il personaggio a cui assegnare l'inventario.

        Returns:
            Inventario: L'inventario creato con oggetti di base.
        """
        inventario = Inventario(proprietario=proprietario)
        inventario.oggetti.append(PozioneCura())
        inventario.oggetti.append(BombaAcida())
        inventario.oggetti.append(Medaglione())
        return inventario

    def setup_nemici(self, lista_nemici: list[Personaggio]) -> list[tuple[Personaggio, StrategiaAttacco, Inventario]]:
        """
        Metodo per creare una lista di nemici con strategia e inventario.

        Args:
            lista_nemici (list[Personaggio]): Lista dei personaggi nemici base.

        Returns:
            list[tuple[Personaggio, StrategiaAttacco, Inventario]]: Lista di tuple che rappresentano i nemici preparati.
        """
        nemici_preparati = []
        for nemico in lista_nemici:
            strategia = StrategiaAttaccoFactory.strategia_random()
            inventario = self.crea_inventario_base(nemico)
            nemici_preparati.append((nemico, strategia, inventario))
        return nemici_preparati

    def esegui_scontro(self) -> bool:
        """
        Esegue l'intero ciclo dello scontro tra giocatori e nemici.

        Il metodo gestisce i turni, determina l'ordine di combattimento e controlla
        le condizioni di vittoria o sconfitta.

        Args:
            None

        Returns:
            bool: True se i giocatori vincono lo scontro, False se vengono sconfitti.
        """
        print(f"\n=== Inizio dello scontro ===")
        print(f"Ambiente: { self.ambiente.nome }")
        #Log.scrivi_log(f"Inizio dello scontro nell'ambiente: {self.ambiente.nome}.")

        for nemico in self.nemici:
            print(f"Nemico: {nemico[0].nome}")

        turno_corrente = Turno(
                giocatori=self.giocatori,
                nemici=self.nemici,
                ambiente=self.ambiente
            )

        while True:
            self.counter_turni += 1
            print(f"\n=== Turno {self.counter_turni} ===")
            #Log.scrivi_log(f"Inizio del turno {self.counter_turni}.")

            ordine = [
                personaggio for personaggio in turno_corrente.personaggi
                if not personaggio.sconfitto()
            ]
            print("Ordine di combattimento:")
            for personaggio in ordine:
                print(f"- {personaggio.nome}")
                #Log.scrivi_log(f"Ordine combattimento turno {self.counter_turni}: {personaggio.nome}.")

            var = turno_corrente.gestisci_turno()

            self.missione.rimuovi_nemici_sconfitti()

            if var == 1:
                self.concludi_sconfitta()
                self.stampa_risultati_finali()
                return False
            elif var == 2:
                self.concludi_vittoria()
                self.stampa_risultati_finali()
                return True
            else:
                self.stampa_risultati_finali()

    def concludi_vittoria(self):
        """
        Gestisce la logica e i messaggi di fine scontro in caso di vittoria.

        Args:
            None

        Returns:
            None
        """
        print("\nTutti i nemici sono stati sconfitti!")
        Log.scrivi_log("Esito scontro: VITTORIA dei giocatori.")

    def concludi_sconfitta(self):
        """
        Gestisce la logica e i messaggi di fine scontro in caso di sconfitta.

        Args:
            None

        Returns:
            None
        """
        print("\nTutti i personaggi sono stati sconfitti.")
        Log.scrivi_log("Esito scontro: SCONFITTA dei giocatori.")

    def stampa_risultati_finali(self):
        """
        Stampa e registra lo stato finale dei personaggi al termine dello scontro.

        Args:
            None

        Returns:
            None
        """
        print("\n=== Risultati finali ===")
        Log.scrivi_log("Stato finale dei personaggi: ")
        for g, _ in self.giocatori:
            stato = "Sconfitto" if g.sconfitto() else "Vivo"
            print(f"{g.nome}: {stato}")
            Log.scrivi_log(f"{g.nome}: {stato }")
