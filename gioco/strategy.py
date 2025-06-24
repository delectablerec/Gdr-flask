import random
from ambiente import Ambiente
from inventario import Inventario
from personaggio import Personaggio
from utils.log import Log
 


 
class StrategiaAttacco ():
    '''
    La classe StrategiaAttacco è una classe base per le strategie di attacco
    dei nemici.
    Ogni strategia di attacco deve derivare da questa classe e implementare il
    metodo esegui_attacco.
    '''
    def __init__(self, nome: 'str' = "Strategia di attacco"):
        self.nome = nome

    @staticmethod
    def esegui_attacco(
        nemico: 'Personaggio',
        bersaglio: 'Personaggio',
        inventario: 'Inventario',
        ambiente: 'Ambiente' = None
    ) -> None:
        '''
        viene definito un metodo astratto che deve essere implementato
        dalle classi derivate.

        Args:
            nemico (Personaggio): il nemico che esegue l'attacco
            bersaglio (Personaggio): il bersaglio dell'attacco
            inventario (Inventario): l'inventario del nemico
            ambiente (Ambiente): l'ambiente di gioco (opzionale)

        Returns:
            None

        Raises:
            NotImplementedError: il metodo è implementato nelle classi
            derivate.
        '''
        raise NotImplementedError(
            "Devi implementare il metodo esegui nella sottoclasse"
        )


'''
le classi si occuperanno di gestire le decisioni del nemico
durante il suo turno
'''


 
class Aggressiva(StrategiaAttacco):
    '''
    la classe Aggressiva rappresenta una strategia in cui nemico decide di
    focalizzarsi sul fare il maggior danno possibile alla salute del bersaglio.
    '''
    def __init__(self):
        super().__init__(nome="Aggressiva")

    @staticmethod
    def esegui_attacco(
        nemico: 'Personaggio',
        bersaglio: 'Personaggio',
        inventario: 'Inventario',
        ambiente: 'Ambiente' = None
    ) -> None:
        '''
        Esegue l'attacco aggressivo del nemico sul bersaglio. l'unico oggetto
        che può essere usato è la Bomba Acida, che infligge danni al bersaglio.

        args:
            nemico (Personaggio): il nemico che esegue l'attacco
            bersaglio (Personaggio): il bersaglio dell'attacco
            inventario (Inventario): l'inventario del nemico
            ambiente (Ambiente): l'ambiente di gioco (opzionale)
        Returns:
            Nessuno
        '''
        Log.scrivi_log(
            f"{nemico} attacca {bersaglio.nome} con un attacco aggressivo!"
        )
        if inventario and inventario.oggetti:
            ogg = next(
                (
                    ogg for ogg in inventario.oggetti
                    if ogg.nome == "Bomba Acida"
                ),
                None
            )
            if ogg and (random.randint(0, 1) == 0):
                inventario.usa_oggetto(
                    oggetto=ogg,
                    bersaglio=bersaglio,
                    ambiente=ambiente
                )
        if bersaglio.sconfitto():
            return
        mod_attacco = ambiente.modifica_attacco_max(nemico) if ambiente else 0
        nemico.attacca(bersaglio, mod_ambiente=mod_attacco)


 
class Difensiva(StrategiaAttacco):
    '''
    La classe Difensiva rappresenta una strategia in cui il nemico si concentra
    sulla propria salute, curandosi quando questa è sotto i 60 punti e
    attaccando il bersaglio altrimenti.
    '''
    def __init__(self):
        super().__init__(nome="Difensiva")

    @staticmethod
    def esegui_attacco(
        nemico: 'Personaggio',
        bersaglio: 'Personaggio',
        inventario: 'Inventario',
        ambiente: 'Ambiente' = None
    ) -> None:
        '''
        Esegue l'attacco difensivo del nemico sul bersaglio.
        Se la salute del nemico è inferiore a 60 punti, usa una Pozione Rossa
        per curarsi e poi attacca il bersaglio, altrimenti attacca soltanto.
        La probabilità di usare la Pozione Rossa è randomica,
        con una probabilità del 50%.

        Args:
            nemico (Personaggio): il nemico che esegue l'attacco
            bersaglio (Personaggio): il bersaglio dell'attacco
            inventario (Inventario): l'inventario del nemico
            ambiente (Ambiente): l'ambiente di gioco (opzionale)

        Returns:
            None

        '''
        Log.scrivi_log(
            f"{nemico.nome} attacca {bersaglio.nome} con un attacco difensivo!"
        )

        if nemico.salute < 60 and inventario and inventario.oggetti:
            ogg = next(
                (
                    ogg for ogg in inventario.oggetti
                    if ogg.nome == "Pozione Rossa"
                ),
                None
            )
            if ogg and (random.randint(0, 1) == 0):
                inventario.usa_oggetto(
                    oggetto=ogg,
                    bersaglio=nemico,
                    ambiente=ambiente
                )

        mod_attacco = ambiente.modifica_attacco_max(nemico) if ambiente else 0
        nemico.attacca(bersaglio, mod_attacco)


 
class Equilibrata(StrategiaAttacco):
    '''
    La classe Equilibrata rappresenta una strategia in cui il nemico decide di
    curarsi quando la salute è sotto i 40 punti, altrimenti di usare una bomba
    acida e infine attaccare il bersaglio
    l'uso degli oggetti è randomico.
    '''
    def __init__(self):
        super().__init__(nome="Equilibrata")

    @staticmethod
    def esegui_attacco(
        nemico: 'Personaggio',
        bersaglio: 'Personaggio',
        inventario: 'Inventario',
        ambiente: 'Ambiente' = None
    ) -> None:
        '''

        Esegue l'attacco equilibrato del nemico sul bersaglio. Se la salute
        del nemico è inferiore a 40 punti, usa una Pozione Rossa per curarsi e
        poi attacca il bersaglio, altrimenti usa una Bomba Acida per infliggere
        danni al bersaglio e poi attacca.
        L'uso degli oggetti avviene in modo randomico, con una probabilità del
        33% per ciascun oggetto.

        Args:
            nemico (Personaggio): il nemico che esegue l'attacco
            bersaglio (Personaggio): il bersaglio dell'attacco
            inventario (Inventario): l'inventario del nemico
            ambiente (Ambiente): l'ambiente di gioco (opzionale)

        Returns:
            None
        '''
        Log.scrivi_log(
            f"{nemico.nome} attacca {bersaglio.nome} "
            "con un attacco equilibrato!"
        )
        if nemico.salute < 40:
            if inventario and inventario.oggetti:
                ogg = next(
                    (
                        ogg for ogg in inventario.oggetti
                        if ogg.nome == "Pozione Rossa"
                    ),
                    None
                )
                if ogg and (random.randint(0, 2) == 0):
                    inventario.usa_oggetto(
                        oggetto=ogg,
                        bersaglio=nemico,
                        ambiente=ambiente
                    )
        elif inventario and inventario.oggetti:
            ogg = next(
                (
                    ogg for ogg in inventario.oggetti
                    if ogg.nome == "Bomba Acida"
                ),
                None
            )
            if ogg and (random.randint(0, 2) == 0):
                inventario.usa_oggetto(
                    ogg,
                    bersaglio=bersaglio,
                    ambiente=ambiente
                )
                if bersaglio.sconfitto():
                    return

        mod_attacco = ambiente.modifica_attacco_max(nemico) if ambiente else 0
        nemico.attacca(bersaglio, mod_attacco)
# ----------------------------------------------------------------------------


class StrategiaAttaccoFactory:
    '''
    la classe StrategiaAttaccoFactory è una factory che crea le istanze delle
    classi derivate di StrategiaAttacco in base
    al tipo di strategia richiesta o randomicamente.
    '''
    @staticmethod
    def strategia_random() -> StrategiaAttacco:
        '''
        Restituisce una strategia randomica tra le tre disponibili utilizzando
        l'altro metodo usa_strategia.

        Args:
            None

        Returns:
            StrategiaAttacco: un'istanza della strategia randomica.
        '''
        random_choice = random.choice(
            ["aggressiva", "difensiva", "equilibrata"]
        )
        return StrategiaAttaccoFactory.usa_strategia(random_choice)

    @staticmethod
    def usa_strategia(tipo: str) -> StrategiaAttacco:
        '''
        Restituisce un'istanza della strategia richiesta in base
        al tipo passato come argomento.

        Args:
            tipo (str): il tipo di strategia da utilizzare
                può essere "aggressiva", "difensiva" o "equilibrata".

        Returns:
            StrategiaAttacco: un'istanza della strategia richiesta.

        Raises:
            ValueError: se il tipo di strategia non è valido.
        '''
        tipo = tipo.lower()
        if tipo == "aggressiva":
            return Aggressiva()
        elif tipo == "difensiva":
            return Difensiva()
        elif tipo == "equilibrata":
            return Equilibrata()
        else:
            raise ValueError(f"Tipo di strategia sconosciuto: {tipo}")
