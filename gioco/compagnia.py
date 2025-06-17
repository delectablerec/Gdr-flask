from gioco.personaggio import Personaggio
from gioco.classi import Guerriero, Mago, Ladro
from gioco.oggetto import Oggetto, PozioneCura, BombaAcida, Medaglione
from gioco.inventario import Inventario
from gioco.menu_principale import MenuPrincipale
from utils.log import Log
from utils.salvataggio import SerializableMixin
from utils.messaggi import Messaggi

@SerializableMixin.register_class
class Compagnia:
    """
    Gestisce i personaggi_inventari del party e i loro inventari, aggiunta/rimozione personaggi_inventari.
    Associazione automatica degli inventari, passaggio di oggetti tra inventari

    Attributes:
        personaggi_inventari (list): Lista di tuple (personaggio[Personaggio], inventario[inventario]).
        personaggi (list): Lista di soli personaggi estratti da personaggi_inventari.
    """
    def __init__(self, menu_principale: MenuPrincipale) -> None:
        """
        Inizializza la compagnia con i personaggi e inventari recuperati dal MenuPrincipale.

        Args:
            menu_principale (MenuPrincipale): Istanza del menu principale da cui recuperare i personaggi_inventari.

        Returns:
            None
        """
        self.personaggi_inventari = menu_principale.personaggi_inventari
        self.personaggi = [personaggio_inventario[0] for personaggio_inventario in self.personaggi_inventari]

    def personaggi_presenti(self) -> list[str]:
        nomi = [personaggio.nome for personaggio in self.personaggi]
        msg = ("\nPersonaggi nella compagnia:")
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        for personaggio, _ in self.personaggi_inventari:
            msg = f"Nome: {personaggio.nome}, Classe: {personaggio.__class__.__name__}"
            Messaggi.add_to_messaggi(msg)
            Log.scrivi_log(msg)
        return nomi

    def aggiungi_personaggio(self, personaggio_inventario: tuple[Personaggio, Inventario]) -> None:
        """
        Aggiunge un personaggio alla compagnia e associa il suo inventario.

        Args:
            personaggio_inventario (tuple[Personaggio, Inventario]): Tupla contenente il personaggio e il suo inventario.

        Returns:
            None
        """
        pass

    def rimuovi_personaggio(self, personaggio: Personaggio) -> None:
        """
        Rimuove un personaggio e il relativo inventario dalla compagnia.

        Args:
            personaggio (Personaggio): Il personaggio da rimuovere insieme al suo inventario.

        Returns:
            None
        """
        if personaggio in self.personaggi:
            self.personaggi_inventari = [pers for pers in self.personaggi_inventari if pers[0] != personaggio]
            self.personaggi.remove(personaggio)
            msg = f"{personaggio.nome} è stato rimosso dalla compagnia con il suo inventario."
            Messaggi.add_to_messaggi(msg)
            Log.scrivi_log(msg)
        else:
            msg = f"{personaggio.nome} non è presente nella compagnia."
            Messaggi.add_to_messaggi(msg)
            Log.scrivi_log(msg)

    def mostra_inventari(self) -> None:
        """
        Visualizza tutti i personaggi_inventari con i loro inventari associati.

        Args:
            None

        Returns:
            None
        """
        msg = ("\n=== Inventari della compagnia ===")
        Messaggi.add_to_messaggi(msg)
        Log.scrivi_log(msg)
        for personaggio, inventario in self.personaggi_inventari:
            msg = f"\n{personaggio.nome} - Inventario:"
            Messaggi.add_to_messaggi(msg)
            Log.scrivi_log(msg)
            for oggetto in inventario.oggetti:
                msg = f" - {oggetto.nome}"
                Messaggi.add_to_messaggi(msg)
                Log.scrivi_log(msg)

    def get_inventari(self) -> list[Inventario]:
        """
        Restituisce la lista degli inventari dei personaggi_inventari nella compagnia.

        Args:
            None

        Returns:
            list[Inventario]: Lista degli inventari dei personaggi_inventari.
        """
        return [inventario for personaggio, inventario in self.personaggi_inventari]


    def get_personaggi_inventari(self) -> list[tuple[Personaggio, Inventario]]:
        """
        Restituisce la lista dei personaggi_inventari nella compagnia.

        Args:
            None

        Returns:
            list[tuple[Personaggio, Inventario]]: Lista di tuple contenenti i personaggi e i loro inventari.
        """
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
