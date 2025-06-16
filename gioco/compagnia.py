from gioco.personaggio import Personaggio
from gioco.classi import Guerriero, Mago, Ladro
from gioco.oggetto import Oggetto, PozioneCura, BombaAcida, Medaglione
from gioco.inventario import Inventario
from gioco.menu_principale import MenuPrincipale
from utils.log import Log
from utils.salvataggio import SerializableMixin

@SerializableMixin.register_class
class Compagnia:
    def __init__(self, menu_principale: MenuPrincipale) -> None:
        self.personaggi_inventari = menu_principale.personaggi_inventari
        self.personaggi = [personaggio_inventario[0] for personaggio_inventario in self.personaggi_inventari]

    def personaggi_presenti(self) -> list[str]:
        nomi = [personaggio.nome for personaggio in self.personaggi]
        msg = ("\nPersonaggi nella compagnia:")
        Log.scrivi_log(msg)
        for personaggio, _ in self.personaggi_inventari:
            msg = f"Nome: {personaggio.nome}, Classe: {personaggio.__class__.__name__}"
            Log.scrivi_log(msg)
        return nomi

    def aggiungi_personaggio(self, personaggio_inventario: tuple[Personaggio, Inventario]) -> None:
        pass

    def rimuovi_personaggio(self, personaggio: Personaggio) -> None:
        if personaggio in self.personaggi:
            self.personaggi_inventari = [pers for pers in self.personaggi_inventari if pers[0] != personaggio]
            self.personaggi.remove(personaggio)
            msg = f"{personaggio.nome} è stato rimosso dalla compagnia con il suo inventario."
            Log.scrivi_log(msg)
        else:
            msg = f"{personaggio.nome} non è presente nella compagnia."
            Log.scrivi_log(msg)

    def mostra_inventari(self) -> None:
        msg = ("\n=== Inventari della compagnia ===")
        Log.scrivi_log(msg)
        for personaggio, inventario in self.personaggi_inventari:
            msg = f"\n{personaggio.nome} - Inventario:"
            Log.scrivi_log(msg)
            for oggetto in inventario.oggetti:
                msg = f" - {oggetto.nome}"
                Log.scrivi_log(msg)

    def get_inventari(self) -> list[Inventario]:
        return [inventario for personaggio, inventario in self.personaggi_inventari]


    def get_personaggi_inventari(self) -> list[tuple[Personaggio, Inventario]]:
        return self.personaggi_inventari

    def to_dict(self) -> dict:
        """Restituisce uno stato serializzabile per session o JSON."""
        return {
            "classe": self.__class__.__name__,
            "personaggi_inventari": [(personaggio.to_dict(), inventario.to_dict()) for personaggio, inventario in self.personaggi_inventari]
        }
    @classmethod
    def from_dict(cls, data: dict) -> "Compagnia":
        """Ricostruisce l’istanza a partire da un dict serializzato."""
        personaggi_inventari = []
        for personaggio_data, inventario_data in data.get("personaggi_inventari", []):
            personaggio = Personaggio.from_dict(personaggio_data)
            inventario = Inventario.from_dict(inventario_data)
            personaggi_inventari.append((personaggio, inventario))
        return cls(personaggi_inventari)