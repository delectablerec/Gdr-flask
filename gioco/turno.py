import random
from gioco.ambiente import Ambiente
from gioco.inventario import Inventario
from utils.interfaccia import InterfacciaUtente as I_U # Da modificare
from gioco.strategy_patterns import StrategiaAttacco # Da modificare.strategy_patterns sarà in strategy?
from gioco.personaggio import Personaggio
from gioco.classi import Guerriero, Mago, Ladro
from utils.salvataggio import SerializableMixin


@SerializableMixin.register_class
class Turno(SerializableMixin):
    """
    Classe per gestire il turno di possibili personaggi multipli nel gioco.
    in inizializzazione prende una lista di personaggi,
    una lista di tuple (abbinamento nemico e il pattern correlato) e
    l'ambiente e gestisce il turno

    """

    def __init__(
        self,
        giocatori: list[tuple[Personaggio, Inventario]],
        nemici: list[tuple[Personaggio, StrategiaAttacco, Inventario]],
        alleati: list[tuple[Personaggio, StrategiaAttacco, Inventario]] = None,
        ambiente: Ambiente = None
    ) -> None:

        self.giocatori = giocatori
        self.nemici = nemici
        self.alleati = alleati if alleati is not None else []
        self.personaggi = self._lista_personaggi(giocatori, nemici, alleati)
        self.ambiente = ambiente
        self.giocatori_list = [giocatore for giocatore, _ in self.giocatori]
        self.nemici_list = [nemico for nemico, _, _ in self.nemici]
        self.alleati_list = (
            [alleato for alleato, _, _ in self.alleati]
            if alleati is not None else []
        )

    # metodi pubblici della classe

    def gestisci_turno(self) -> int:
        """
        Gestisce il turno dei personaggi.
        Itera attraverso la lista dei personaggi e gestisce il turno
        di ciascun personaggio, sia che sia un giocatore, un nemico o un alleato.
        Se un personaggio è sconfitto, viene rimosso dalla lista dei personaggi.
        Se tutti i personaggi giocatori o nemici sono stati sconfitti,
        il turno termina.

        Args:
            None

        Returns:
            int: 1 se i giocatori sono stati sconfitti,
                 2 se i nemici sono stati sconfitti,
                 0 se il turno continua
        """

        value = 0
        for personaggio in list(self.personaggi):
            self._rimozione_sconfitti_da_lista([self.giocatori_list, self.nemici_list])
            if personaggio.sconfitto():
                continue  # Salta il turno se il personaggio è sconfitto

            if personaggio in self.giocatori_list:
                # Se il personaggio è un giocatore,
                # gestisce il turno del giocatore
                print(f"\nTurno del giocatore {personaggio.nome}\n")
                self._turno_player((
                    personaggio,
                    next(
                        inv for p, inv in self.giocatori
                        if p == personaggio
                    )
                ))

            elif personaggio in self.nemici_list:
                self._turno_npc(personaggio)
            elif personaggio in self.alleati_list:
                raise NotImplementedError(
                    "Gestione del turno degli alleati non implementata."
                )
            value = self.controllo_vittoria_sconfitta()
            if value != 0:
                break
        # Controlla se ci sono personaggi, giocatori o nemici sconfitti dopo
        # il turno e li rimuove dalla lista collegate
        if value != 0:
            self._rimozione_sconfitti_da_lista([self.personaggi])
        return value

    # metodi opzionali, sono in uso all'interno della classe,
    # ma possono essere usati esternamente
    def ordine_combattimento(
        self,
        personaggi: list[Personaggio] = None
    ) -> list[Personaggio]:
        """
        Ordina i personaggi giocanti e in maniera randomica.
        Il metodo genera un valore (compreso tra 1 e 5*len(personaggi) )
        per ciascuno dei personaggi e li ordina in base a questo valore.
        I personaggi di tipo Guerriero, Mago e Ladro hanno
        un bonus di iniziativa rispettivamente di 2, 0 e 4.
        In caso di parità per il secondo personaggio
        l'iniziativa viene ritirata.


        Args:
            list[Personaggio] personaggi: Lista dei personaggi
            da ordinare. Se non viene specificata, viene usata
            la lista dei personaggi del turno.

        Returns:
            list[Personaggio]: Lista dei personaggi ordinati per
            il tiro di iniziativa.
        """
        if personaggi is None:
            personaggi = self.personaggi
        lista_per_iniziativa = []
        for personaggio in personaggi:
            if isinstance(personaggio, Guerriero):
                bonus_iniziativa = 2
            elif isinstance(personaggio, Mago):
                bonus_iniziativa = 0
            elif isinstance(personaggio, Ladro):
                bonus_iniziativa = 4

            while True:
                iniziativa = random.randint(1, 5 * len(personaggi))
                iniziativa += bonus_iniziativa
                # Controlla che nessun altro personaggio
                # abbia già questo valore di iniziativa
                if iniziativa not in [x[0] for x in lista_per_iniziativa]:
                    lista_per_iniziativa.append((iniziativa, personaggio))
                    break

        # Ordina i personaggi per valore di iniziativa (ordine crescente)
        lista_per_iniziativa.sort(key=lambda x: x[0])

        # Restituisce solo la lista di personaggi già ordinati
        return [personaggio for _, personaggio in lista_per_iniziativa]

    def controllo_vittoria_sconfitta(self) -> int:
        """
        Controlla se ci sono giocatori sconfitti.
        non richiede argomenti essendo una funzione interna della classe.
        ritorna 1 se tutti i personaggi della lista giocatori sono stati sconfitti,
        ritorna 2 se tutti i personaggi della lista nemici sono stati sconfitti,
        e ritorna 0 se nessuno dei due gruppi è stato sconfitto

        Args:
            None

        Returns:
            int: 1 se tutti i personaggi giocatori sono stati sconfitti,
                 2 se tutti i personaggi nemici sono stati sconfitti,
                 0 se nessuno dei due gruppi è stato sconfitto.
        """
        value = 0
        liste = [self.giocatori_list, self.nemici_list]
        if not liste[0]:
            value = 1
            print("Tutti i personaggi giocatori sono stati sconfitti!")
        elif not liste[1]:
            value = 2
            print("Tutti i nemici sono stati sconfitti!")
        else:
            for lista in liste:
                control = True
                for personaggio in lista:
                    if not personaggio.sconfitto():
                        control = False
                        break
                if control:
                    if lista is self.giocatori_list:
                        value = 1
                        print("Tutti i personaggi giocatori sono stati sconfitti!")
                    if lista is self.nemici_list:
                        value = 2
                        print("Tutti i nemici sono stati sconfitti!")
                    break
        return value
    # metodi interni della classe

    def _lista_personaggi(
        self,
        giocatori,
        nemici,
        alleati
    ) -> list[Personaggio]:
        """
        Costruttore automatico della lista dei personaggi coinvolti nel turno.

        Args:
            giocatori (list[tuple[Personaggio, Inventario]]): Lista dei giocatori,
            dove ogni elemento è un una tupla contenente il personaggio e l'inventario
            dei giocatori.
            nemici (list[tuple[Personaggio, StrategiaAttacco, Inventario]]): Lista dei nemici,
            dove ogni elemento è una tupla contenente il personaggio, la strategia di attacco
            e l'inventario del nemico.
            alleati (list[tuple[Personaggio, StrategiaAttacco, Inventario]]): Lista degli alleati,
            dove ogni elemento è una tupla contenente il personaggio, la strategia di attacco
            e l'inventario dell'alleato. Può essere None se non ci sono alleati.

        Returns:
            list[Personaggio]: Lista dei personaggi ordinati per il turno.
        """
        personaggi = []
        personaggi += [giocatore for giocatore, _ in giocatori]
        personaggi += [nemico for nemico, _, _ in nemici]
        if alleati:
            personaggi += [alleato for alleato, _, _ in alleati]
        return self.ordine_combattimento(personaggi)

    def _turno_player(self, player: tuple[Personaggio, Inventario]) -> None:
        """
        Gestisce il turno di un personaggio giocatore.
        Chiede se vuole usare un oggetto e attaccare dopo
        o attaccare direttamente. Il metodo esce anticipatamente
        se viene rilevata una condizione di vittoria o sconfitta
        (ad esempio, se tutti i giocatori o i nemici sono stati sconfitti).

        Args:
            player (tuple[Personaggio, Inventario]): Tupla del personaggio
            dell'utente che sta giocando il turno con il suo inventario.

        Returns:
            None
        """
        # Logica per gestire il turno del giocatore
        self._uso_inventario_player(player)
        if (
            self.controllo_vittoria_sconfitta() != 0
        ):
            return  # Esce se tutti i giocatori o i nemici sono stati sconfitti
        self._rimozione_sconfitti_da_lista([self.nemici_list])
        self._attacco_player(player[0])

    def _uso_inventario_player(
        self, player: tuple[Personaggio, Inventario]
    ) -> None:
        """
        Gestisce l'uso dell'inventario da parte del giocatore.
        Chiede al giocatore se vuole usare un oggetto dal suo inventario.
        se usando un oggetto contro un bersaglio questo viente sconfitto 
        si ottiene linventario

        Args:
            player (tuple[Personaggio, Inventario]): Tupla del personaggio
            dell'utente che sta giocando il turno con il suo inventario.

        Returns:
            None
        """
        if I_U.conferma("Vuoi usare un oggetto dal tuo inventario?"):
            bersagli=[
                personaggio for personaggio
                in self.personaggi
                if not personaggio.sconfitto()
            ]
            player[1].cerca_e_usa_multi(bersagli=bersagli,
            ambiente=self.ambiente
            )

            self._controllo_personaggio_sconfitto(
                player=player[0],
                lista=bersagli
            )

    def _attacco_player(self, giocatore: Personaggio) -> None:
        """
        Gestisce l'attacco del giocatore selezionato.
        Chiede al giocatore di selezionare un nemico da attaccare

        Args:
            giocatore (Personaggio): Il personaggio giocatore che sta attaccando.

        Returns:
            None
        """
        print("nemici nello scontro:")
        for indx, nem in enumerate(self.nemici_list):
            print(f"{indx + 1} - {nem.nome} ({nem.salute}/{nem.salute_max} salute, classe: {nem.__class__.__name__}) ")

        scelta = I_U.chiedi_numero(
            "Chi vuoi attaccare?",
            1,
            len(self.nemici_list))

        scelta -= 1  # Per allineare l'indice a zero
        bersaglio_assalto= self.nemici_list[scelta]

        giocatore.attacca(
            bersaglio=bersaglio_assalto,
            mod_ambiente=(
                self.ambiente.modifica_attacco_max(giocatore)
                if self.ambiente else 0
            )
        )
        self._controllo_personaggio_sconfitto(
            player=giocatore,
            lista=self.nemici_list
        )

    def _controllo_personaggio_sconfitto(self, player: Personaggio, lista: list[Personaggio]) -> None:
        """
        Controlla se un personaggio o una lista è stato appena sconfitto e riversa l'inventario
        del personaggio sconfitto nell'inventario del giocatore.

        Args:
            player (Personaggio): Il personaggio giocatore che sta giocando il turno.
            lista (list[Personaggio]): Lista di personaggi da controllare per la sconfitta.

        Returns:
            None
        """
        for bersaglio in lista:
            if bersaglio.sconfitto():
                inventario_sconfitto = next(
                    inv for p, _, inv in self.nemici
                    if p == bersaglio
                )
                inventario_player = next(
                    inv for p, inv in self.giocatori
                    if p == player
                )
                inventario_player.riversa(inventario_sconfitto)
                break

    def _turno_npc(self, npc: Personaggio) -> None:
        """
        Gestisce il turno di un personaggio NPC.
        Se il personaggio ha una strategia di attacco,
        usa quella strategia per attaccare un bersaglio.
        Altrimenti, seleziona un bersaglio casuale tra i giocatori
        e attacca con l'attacco di base del personaggio.

        Args:
            npc (Personaggio): Il personaggio che sta giocando il turno.

        Returns:
            None
        """
        # Trova il nemico corrispondente
        nemico = next(nem for nem in self.nemici if nem[0] == npc)

        # Ottiene la strategia di attacco del nemico, se esiste
        strategia = nemico[1]  # Usa direttamente la strategia dal nemico trovato

        # Ottiene l'inventario del nemico, se esiste
        nemico_inventario = nemico[2] if len(nemico) > 2 else None

        if strategia: # Se c'è una strategia, usa la sua funzione per attaccare
            strategia.esegui_attacco(
                nemico=nemico[0],
                bersaglio=self._npc_selezione_bersaglio_semplice(),
                inventario=nemico_inventario,
                ambiente=self.ambiente
            )
        else: # Se non c'è una strategia, usa l'attacco di base dell'npc
            nemico[0].attacca(
                bersaglio=self._npc_selezione_bersaglio_semplice(),
                 mod_ambiente=(
                    self.ambiente.modifica_attacco_max(nemico[0])
                    if self.ambiente else 0
                    ))

    def _npc_selezione_bersaglio_semplice(self) -> Personaggio:
        """
        Seleziona un bersaglio tra i giocatori disponibili,
        la cui salute sia maggiore di 0, per l'attacco dei npc nemici.

        Args:
            None

        Returns:
            Personaggio: Il bersaglio selezionato.
        """
        bersagli_disponibili = [
            giocatore for giocatore, _ in self.giocatori
            if not giocatore.sconfitto()
        ]
        if not bersagli_disponibili:
            raise ValueError("Non ci sono bersagli disponibili per l'attacco.")
        return random.choice(bersagli_disponibili)

    def _rimozione_sconfitti_da_lista(self, liste_da_controllare: list[list[Personaggio]]) -> None:
        """
        Rimuove i personaggi sconfitti dalla lista fornita.
        Questa funzione è utile per mantenere la lista dei personaggi
        aggiornata rimuovendo quelli che sono stati sconfitti.

        Args:
            liste_da_controllare (list[list[Personaggio]]): Lista di liste
            contenenti i personaggi da controllare per la sconfitta.

        Returns:
            None
        """
        for lista in liste_da_controllare:
            pers_da_rimuovere = []
            for personaggio in list(lista):
                if personaggio.sconfitto():
                    pers_da_rimuovere.append(personaggio)
            for personaggio in pers_da_rimuovere:
                lista.remove(personaggio)
                
    def to_dict(self) -> dict:
        return {
            "classe": self.__class__.__name__,
            "giocatori": [
                (giocatore.to_dict(), inventario.to_dict())
                for giocatore, inventario in self.giocatori
            ],
            "nemici": [
                (
                    nemico.to_dict(),
                    strategia.to_dict(),
                    inventario.to_dict()
                )
                for nemico, strategia, inventario in self.nemici
            ],
            "alleati": [
                (
                    alleato.to_dict(),
                    strategia.to_dict(),
                    inventario.to_dict()
                )
                for alleato, strategia, inventario in self.alleati
            ] if self.alleati else [],
            "ambiente": self.ambiente.to_dict() if self.ambiente else None
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> "Turno":
        from gioco.inventario import Inventario
        from gioco.strategy_patterns import StrategiaAttacco
        from gioco.personaggio import Personaggio
        from gioco.ambiente import Ambiente

        giocatori = [
            (Personaggio.from_dict(p), Inventario.from_dict(inv))
            for p, inv in data["giocatori"]
        ]
        nemici = [
            (
                Personaggio.from_dict(p),
                StrategiaAttacco.from_dict(s),
                Inventario.from_dict(inv)
            )
            for p, s, inv in data["nemici"]
        ]
        alleati = [
            (
                Personaggio.from_dict(p),
                StrategiaAttacco.from_dict(s),
                Inventario.from_dict(inv)
            )
            for p, s, inv in data.get("alleati", [])
        ]
        ambiente = (
            Ambiente.from_dict(data["ambiente"])
            if data.get("ambiente") else None
        )

        return cls(
            giocatori=giocatori,
            nemici=nemici,
            alleati=alleati,
            ambiente=ambiente
        )

