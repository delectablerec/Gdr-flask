import random
from utils.log import get_logger
from gioco.ambiente import Ambiente
from gioco.inventario import Inventario
from enum import Enum

'''
1- dataclass per le strategie non serve, non ci sono campi dinamici da
serializzare (basta l'attributo nome)
2- il logger è già configurato in gioco/__init__.py, non serve ripeterlo qui
3- Costruttori con super() per logging coerente e possibilità di parametri
4- Enum
'''

logger = get_logger(__name__)


class TipoStrategia(Enum):
    """Tipi di strategie per gli NPC.

    Attributes:
        Enum (str): La descrizione della strategia.
    """
    AGGRESSIVA = "aggressiva"
    DIFENSIVA = "difensiva"
    EQUILIBRATA = "equilibrata"

class Strategia:
    """
    Classe base per le strategie di comportamento degli NPC nel gioco.
    Questa classe definisce l'interfaccia per le diverse strategie che
    gli NPC possono usare per prendere decisioni sull'uso dell'inventario e
    le modifiche agli attributi.

    Attributes:
        nome (str): Il nome della strategia, qui predefinito a
            "Strategia base".

    Methods:
        uso_inventario_npc: Determina come un NPC usa gli oggetti
            del proprio inventario.
    """

    nome = "Strategia base"

    def __init__(self):
        logger.info(f"[Strategia] Selezionata: {self.nome}")

    def uso_inventario_npc(
        self,
        salute_npc: int,
        inventario: Inventario,
        ambiente: Ambiente = None,
    ) -> int | None:
        """
        Determina come un NPC usa gli oggetti del proprio inventario.
        Args:
            salute_npc (int): La salute attuale dell'NPC.
                inventario (Inventario): L'inventario dell'NPC.
            ambiente (Ambiente, optional): L'ambiente attuale.
                Defaults to None.

        Raises:
            NotImplementedError: Se il metodo non è implementato
                nelle sottoclassi.

        Returns:
            int | None: Il risultato dell'uso dell'oggetto o None se non
                viene usato nulla.
        """

        logger.info(
            f"[Strategia {self.nome}] Nessun comportamento specificato."
        )
        raise NotImplementedError("Implementare nelle sottoclassi.")


class Aggressiva(Strategia):
    """
    Strategia aggressiva per gli NPC.
    """
    nome = "Aggressiva"

    def __init__(self):
        super().__init__()
        logger.info("NPC userà strategia AGGRESSIVA: danni massimi!")

    def uso_inventario_npc(self, salute_npc, inventario, ambiente=None):
        """
        Determina come un NPC usa gli oggetti del proprio inventario:
            essendo che la strategia è aggressiva, l'NPC si focalizza nel
            cercare di fare il maggior danno possibile.
        In pratica ha una probabilita del 34% di usare il Medaglione,
        50% di usare la Bomba Acida, altrimenti non usa nulla.

        Args:
            salute_npc (int): La salute attuale dell'NPC.
            inventario (Inventario): L'inventario dell'NPC.
            ambiente (Ambiente, optional): L'ambiente attuale.
                Defaults to None.

        Returns:
            int | None: Il risultato dell'uso dell'oggetto o None se non
                viene usato nulla.
        """

        if inventario and inventario.oggetti:
            ogg = next(
                (o for o in inventario.oggetti if o.nome == "Medaglione"),
                None
            )
            if ogg and random.random() < 0.34:  # 34%
                logger.info("NPC usa Medaglione!")
                return inventario.usa_oggetto(oggetto=ogg, ambiente=ambiente)
            ogg = next(
                (o for o in inventario.oggetti if o.nome == "Bomba Acida"),
                None
            )
            if ogg and random.random() < 0.5:  # 50%
                logger.info("NPC usa Bomba Acida!")
                return inventario.usa_oggetto(oggetto=ogg, ambiente=ambiente)
        logger.info("NPC non usa oggetti (Aggressiva).")
        return None


class Difensiva(Strategia):
    """
    Strategia difensiva per gli NPC.
    """
    nome = "Difensiva"

    def __init__(self):
        super().__init__()
        logger.info("NPC userà strategia DIFENSIVA: si cura se serve.")

    def uso_inventario_npc(self, salute_npc, inventario, ambiente=None):
        """
        Determina come un NPC usa gli oggetti del proprio inventario:
            essendo che la strategia è difensiva, l'NPC si focalizza nel
            cercare di curarsi se la salute è bassa, altrimenti usa
            il Medaglione per aumentare il suo attacco.
        In pratica ha una probabilità del 25% di usare la Super Pozione Rossa
        nel caso la salute sia sotto il 30%, 50% di usare la Pozione Rossa
        se la salute è sotto il 60%, 15% di usare il Medaglione se non sceglie
        una delle altre due opzioni, altrimenti non usa nulla.

        Args:
            salute_npc (int): La salute attuale dell'NPC.
            inventario (Inventario): L'inventario dell'NPC.
            ambiente (Ambiente, optional): L'ambiente attuale.
                Defaults to None.

        Returns:
            int | None: Il risultato dell'uso dell'oggetto o None se non
                viene usato nulla.
        """

        if inventario and inventario.oggetti:
            if salute_npc < 30:
                ogg = next(
                    (
                        o for o in inventario.oggetti
                        if o.nome == "Super Pozione Rossa"
                    ),
                    None
                )
                if ogg and random.random() < 0.25:
                    logger.info("NPC usa Super Pozione Rossa (Difensiva).")
                    return inventario.usa_oggetto(
                        oggetto=ogg, ambiente=ambiente
                    )
            if salute_npc < 60:
                ogg = next(
                    (
                        o for o in inventario.oggetti
                        if o.nome == "Pozione Rossa"
                    ),
                    None
                )
                if ogg and random.random() < 0.5:
                    logger.info("NPC usa Pozione Rossa (Difensiva).")
                    return inventario.usa_oggetto(
                        oggetto=ogg, ambiente=ambiente
                    )
            ogg = next(
                (o for o in inventario.oggetti if o.nome == "Medaglione"),
                None
            )
            if ogg and random.random() < 0.15:
                logger.info("NPC usa Medaglione (Difensiva).")
                return inventario.usa_oggetto(
                    oggetto=ogg, ambiente=ambiente
                )
        logger.info("NPC non usa oggetti (Difensiva).")
        return None


class Equilibrata(Strategia):
    """
    Strategia equilibrata per gli NPC.
    """
    nome = "Equilibrata"

    def __init__(self):
        super().__init__()
        logger.info("NPC userà strategia EQUILIBRATA.")

    def uso_inventario_npc(self, salute_npc, inventario, ambiente=None):
        """
        Determina come un NPC usa gli oggetti del proprio inventario:
            essendo che la strategia è equilibrata, l'NPC usa gli oggetti
            in modo bilanciato tra cura e danno.
        In pratica ha una probabilità del 25% di usare il Medaglione,
        del 33% di usare la Pozione Rossa se la salute è sotto i 40
        punti ferita o del 33% di usare la Bomba Acida.

        Args:
            salute_npc (int): La salute attuale dell'NPC.
            inventario (Inventario): L'inventario dell'NPC.
            ambiente (Ambiente, optional): L'ambiente attuale.
                Defaults to None.

        Returns:
            int | None: Il risultato dell'uso dell'oggetto o None se non
                viene usato nulla.

        """
        if inventario and inventario.oggetti:
            ogg = next(
                (o for o in inventario.oggetti if o.nome == "Medaglione"),
                None
            )
            if ogg and random.random() < 0.25:
                logger.info("NPC usa Medaglione (Equilibrata).")
                return inventario.usa_oggetto(oggetto=ogg, ambiente=ambiente)
            if salute_npc < 40:
                ogg = next(
                    (
                        o for o in inventario.oggetti
                        if o.nome == "Pozione Rossa"
                    ),
                    None
                )
                if ogg and random.random() < 0.33:
                    logger.info("NPC usa Pozione Rossa (Equilibrata).")
                    return inventario.usa_oggetto(
                        oggetto=ogg, ambiente=ambiente
                    )
            ogg = next(
                (o for o in inventario.oggetti if o.nome == "Bomba Acida"),
                None
            )
            if ogg and random.random() < 0.33:
                logger.info("NPC usa Bomba Acida (Equilibrata).")
                return inventario.usa_oggetto(
                    oggetto=ogg, ambiente=ambiente
                )
        logger.info("NPC non usa oggetti (Equilibrata).")
        return None

# --------- FACTORY ------------


class StrategiaFactory:
    """
    Factory per creare istanze di strategie basate su tipo.
    i suoi metodi statici permettono di ottenere una strategia
    casuale o una strategia specifica basata su un tipo fornito.

    Attributes:
        _mappa (dict): Mappa dei tipi di strategia a classi concrete.

    Methods:
        strategia_random: Restituisce una strategia casuale tra quelle
            contenute in _mappa.
        usa_strategia: Restituisce una strategia basata sul tipo fornito.
    """
    _mappa = {
        TipoStrategia.AGGRESSIVA: Aggressiva,
        TipoStrategia.DIFENSIVA: Difensiva,
        TipoStrategia.EQUILIBRATA: Equilibrata
    }

    @staticmethod
    def strategia_random() -> Strategia:
        """
        Restituisce una strategia casuale tra quelle contenute in _mappa.

        Returns:
            Strategia: Un'istanza di una strategia casuale.
        """
        cls = random.choice(list(StrategiaFactory._mappa.values()))
        return cls()

    @staticmethod
    def usa_strategia(tipo: str) -> Strategia:
        """
        Restituisce una strategia basata sul tipo fornito.
        Cerca il tipo nell'enum TipoStrategia e restituisce
        l'istanza corrispondente dalla mappa. Se il tipo non è valido,
        solleva un ValueError.

        Args:
            tipo (str): Il tipo di strategia da utilizzare.

        Returns:
            Strategia: Un'istanza della strategia richiesta.

        Raises:
            ValueError: Se il tipo di strategia non è valido.
        """
        try:
            tipo_enum = TipoStrategia(tipo.lower())
            return StrategiaFactory._mappa[tipo_enum]()
        except (ValueError, KeyError):
            raise ValueError(f"Tipo di strategia sconosciuto: {tipo}")
