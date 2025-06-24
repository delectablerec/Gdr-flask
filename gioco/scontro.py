import random

from utils.log import Log
from gioco.oggetto import PozioneCura, BombaAcida, Medaglione
from gioco.inventario import Inventario
from gioco.missione import Missione
from gioco.personaggio import Personaggio
from gioco.strategy import StrategiaAttacco, StrategiaAttaccoFactory
from gioco.turno import Turno
 , Json


class Scontro:
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
        inventario = Inventario(proprietario=proprietario)
        inventario.oggetti.append(PozioneCura())
        inventario.oggetti.append(BombaAcida())
        inventario.oggetti.append(Medaglione())
        return inventario

    def setup_nemici(self, lista_nemici: list[Personaggio]) -> list[tuple[Personaggio, StrategiaAttacco, Inventario]]:
        nemici_preparati = []
        for nemico in lista_nemici:
            strategia = StrategiaAttaccoFactory.strategia_random()
            inventario = self.crea_inventario_base(nemico)
            nemici_preparati.append((nemico, strategia, inventario))
        return nemici_preparati

    def esegui_scontro(self) -> bool:
        msg = ("\n=== Inizio dello scontro ===")
        Log.scrivi_log(msg)
        msg = f"Ambiente: { self.ambiente.nome }"
        Log.scrivi_log(msg)

        for nemico in self.nemici:
            msg = f"Nemico: {nemico[0].nome}"
            Log.scrivi_log(msg)


        turno_corrente = Turno(
                giocatori=self.giocatori,
                nemici=self.nemici,
                ambiente=self.ambiente
            )

        while True:
            self.counter_turni += 1
            msg = f"\n=== Turno {self.counter_turni} ==="
            Log.scrivi_log(msg)

            ordine = [
                personaggio for personaggio in turno_corrente.personaggi
                if not personaggio.sconfitto()
            ]
            msg = ("Ordine di combattimento:")
            Log.scrivi_log(msg)
            for personaggio in ordine:
                msg = f"- {personaggio.nome}"
                Log.scrivi_log(msg)
                msg = f"Ordine combattimento turno {self.counter_turni}: {personaggio.nome}."
                Log.scrivi_log(msg)

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
        msg = ("\nTutti i nemici sono stati sconfitti!")
        Log.scrivi_log(msg)

    def concludi_sconfitta(self):
        msg = ("\nTutti i personaggi sono stati sconfitti.")
        Log.scrivi_log(msg)

    def stampa_risultati_finali(self):
        msg = ("\n=== Risultati finali ===")
        Log.scrivi_log(msg)
        msg = ("Stato finale dei personaggi: ")
        Log.scrivi_log(msg)
        for g, _ in self.giocatori:
            stato = "Sconfitto" if g.sconfitto() else "Vivo"
            msg = f"{g.nome}: {stato}"
            Log.scrivi_log(msg)

    def to_dict(self) -> dict:
        return {
            "classe": self.__class__.__name__,
            "missione": self.missione.to_dict(),
            "giocatori": [(g.to_dict(), i.to_dict()) for g, i in self.giocatori],
            "nemici": [(n[0].to_dict(), n[1].to_dict(), n[2].to_dict()) for n in self.nemici],
            "counter_turni": self.counter_turni,
            "inventari_nemici": [i.to_dict() for i in self.inventari_nemici]
        }
    @classmethod
    def from_dict(cls, data: dict) -> "Scontro":
        missione = Missione.from_dict(data["missione"])
        giocatori = [(Personaggio.from_dict(g), Inventario.from_dict(i)) for g, i in data["giocatori"]]
        nemici = [(Personaggio.from_dict(n[0]), n[1], Inventario.from_dict(n[2])) for n in data["nemici"]]
        scontro = cls(missione=missione, giocatori=giocatori)
        scontro.nemici = nemici
        scontro.counter_turni = data.get("counter_turni", 0)
        scontro.inventari_nemici = [Inventario.from_dict(i) for i in data.get("inventari_nemici", [])]
        return scontro