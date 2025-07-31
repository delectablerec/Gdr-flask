import random
from typing import Dict
from dataclasses import dataclass
from utils.log import get_logger

'''
1- Logger
2- Factory accetta sia numeri che stringhe tipo dizionario in modo da
    selezionare come numero in console
3- Unificati mod_ modifica_
'''

logger = get_logger(__name__)


@dataclass
class Ambiente:
    """
    Gestisce i modificatori ambientali per Personaggio e Oggetto.
    """
    nome: str
    mod_attacco: int = 0
    mod_cura: float = 0.0

    def modifica_attacco(
        self,
        classe_attaccante: str,
        nome_attaccante: str
    ) -> int:
        raise NotImplementedError

    def modifica_effetto_oggetto(
        self,
        classe_oggetto: str,
        valore_oggetto: int
    ) -> int:
        raise NotImplementedError

    def modifica_cura(self, classe_soggetto: str, nome_soggetto: str) -> int:
        raise NotImplementedError


@dataclass
class Foresta(Ambiente):
    nome: str = "Foresta"
    mod_attacco: int = 5
    mod_cura: float = 5.0

    def modifica_attacco(
        self,
        classe_attaccante: str,
        nome_attaccante: str
    ) -> int:
        if classe_attaccante == "Guerriero":
            logger.info(
                f"{nome_attaccante} guadagna {self.mod_attacco} "
                f"attacco nella Foresta!"
            )
            return self.mod_attacco
        return 0

    def modifica_effetto_oggetto(
        self,
        classe_oggetto: str,
        valore_oggetto: int
    ) -> int:
        return 0

    def modifica_cura(self, classe_soggetto: str, nome_soggetto: str) -> int:
        if classe_soggetto == "Ladro":
            logger.info(
                f"{nome_soggetto} guadagna {int(self.mod_cura)} cura "
                f"extra in Foresta!"
            )
            return int(self.mod_cura)
        return 0


@dataclass
class Vulcano(Ambiente):
    nome: str = "Vulcano"
    mod_attacco: int = 10
    mod_cura: float = -5.0

    def modifica_attacco(
        self,
        classe_attaccante: str,
        nome_attaccante: str
    ) -> int:
        if classe_attaccante == "Mago":
            logger.info(
                f"{nome_attaccante} guadagna {self.mod_attacco} "
                f"attacco nel Vulcano!"
            )
            return self.mod_attacco
        elif classe_attaccante == "Ladro":
            logger.info(
                f"{nome_attaccante} perde {self.mod_attacco} attacco "
                f"nel Vulcano!"
            )
            return -self.mod_attacco
        return 0

    def modifica_effetto_oggetto(
        self,
        classe_oggetto: str,
        valore_oggetto: int
    ) -> int:
        if classe_oggetto == "BombaAcida":
            variazione = random.randint(0, 15)
            logger.info(
                f"Nella {self.nome}, la Bomba Acida guadagna "
                f"{variazione} danni!"
            )
            return variazione
        return 0

    def modifica_cura(self, classe_soggetto: str, nome_soggetto: str) -> int:
        logger.info(
            f"{nome_soggetto} subisce malus di cura {self.mod_cura} "
            f"in Vulcano!"
        )
        return int(self.mod_cura)


@dataclass
class Palude(Ambiente):
    nome: str = "Palude"
    mod_attacco: int = -5
    mod_cura: float = 0.3

    def modifica_attacco(
        self,
        classe_attaccante: str,
        nome_attaccante: str
    ) -> int:
        if classe_attaccante in ["Guerriero", "Ladro"]:
            logger.info(
                f"{nome_attaccante} perde {-self.mod_attacco} "
                f"attacco nella Palude!"
            )
            return self.mod_attacco
        return 0

    def modifica_effetto_oggetto(
        self,
        classe_oggetto: str,
        valore_oggetto: int
    ) -> int:
        if classe_oggetto == "PozioneCura":
            riduzione = int(valore_oggetto * self.mod_cura)
            logger.info(
                f"Nella {self.nome}, la Pozione Cura ha effetto "
                f"ridotto di {riduzione} punti!"
            )
            return -riduzione
        return 0

    def modifica_cura(self, classe_soggetto: str, nome_soggetto: str) -> int:
        return 0


class AmbienteFactory:
    """
    Factory per la generazione di ambienti.
    """
    @staticmethod
    def get_opzioni() -> Dict[str, Ambiente]:
        # Permetti selezione sia per numero che per nome utile in console
        return {
            "1": Foresta(),
            "foresta": Foresta(),
            "2": Vulcano(),
            "vulcano": Vulcano(),
            "3": Palude(),
            "palude": Palude()
        }

    @staticmethod
    def usa_ambiente(scelta: str) -> Ambiente:
        mapping = AmbienteFactory.get_opzioni()
        chiave = str(scelta).strip().lower()
        if chiave in mapping:
            env = mapping[chiave]
            logger.info(f"Selezionato ambiente: {env.nome}")
            return env
        logger.warning(
            f"Scelta ambiente sconosciuta: {scelta}, uso Foresta di default."
        )
        return Foresta()

    @staticmethod
    def ambiente_random() -> Ambiente:
        opzioni = list(
            {
                k: v for k, v in AmbienteFactory.get_opzioni().items()
                if len(k) == 1
            }.values()
        )
        random_choice = random.choice(opzioni)
        logger.info(f"Ambiente Casuale Selezionato: {random_choice.nome}")
        return random_choice
