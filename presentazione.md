# 1. Metodologia organizzattiva, suddivisione dei compiti e versionamento - Enrico Trotti

Durante lo sviluppo di **Saltatio Mortis**, abbiamo adottato un approccio organizzativo collaborativo, con metodologie agili, anche se in forma semplificata. La gestione del progetto è stata fondamentale, vista la complessità e la varietà degli elementi da sviluppare: **personaggi**, **oggetti**, **missioni**, **ambienti** e **strategie** di gioco.

---

###  Suddivisione dei compiti

Ogni giorno, al mattino, il gruppo si riuniva per discutere gli obiettivi della giornata. Decidavamo insieme quali funzionalità implementare e chi se ne sarebbe occupato. La suddivisione dei compiti è stata fatta sia in base alle **competenze** individuali che agli **interessi personali**, focalizzandoci anche sulle debolezze di ciascuno in modo da rinforzare le conoscenze di ciascuno cosicché non ci fosse nessuno di indispensabile ad una parte del progetto.

Ad esempio:
- Mentre alcuni si sono occupati della **logica di gioco** (classi per personaggi, missioni, oggetti…)
- Altri hanno lavorato sulla **struttura dell’interfaccia** con Flask.
- E altri hanno seguito la parte relativa alla **gestione dei dati**.

>  *Tutti i membri hanno collaborato attivamente al confronto e al debugging collettivo, con uno scambio continuo di idee e codice.*

---

###  Versionamento e collaborazione

Abbiamo usato **Git** e **GitHub** per la gestione del codice e il versionamento. Ogni membro lavorava su **branch separati** , per evitare conflitti e mantenere il codice sempre funzionante nel branch chiamato `develop`.

Usavamo:
- **Commit frequenti** e descrittivi in modo da poter rendere partecipi tutti anche delle più piccole implementazioni
- **Pull Request** per il confronto e l’approvazione delle modifiche

---

###  Risultati e competenze acquisite

Grazie a questa esperienza abbiamo imparato a:
- Lavorare in gruppo con ruoli **chiari ma flessibili**
- Utilizzare strumenti professionali come **Git**, **GitHub**, **Markdown**, **Flask**, **Marshmallow**, **Blueprint**,...
- Gestire un progetto reale in modo **collaborativo** ed efficace
- Adottare una **mentalità di problem solving**, confrontandoci continuamente per risolvere bug o migliorare funzionalità

>  _Questa suddivisione del lavoro ci ha permesso di **massimizzare l'efficienza** e **minimizzare i conflitti**, mantenendo sempre una visione d'insieme sullo sviluppo del gioco._




<!-- Le metodologie agili sono un modo di lavorare in team che:

Suddivide il lavoro in piccoli blocchi (iterazioni o sprint).

Prevede incontri frequenti (come le riunioni mattutine nel tuo esempio).

Favorisce la collaborazione tra i membri del gruppo.

Punta a consegnare valore in modo incrementale e continuo.

Si adatta facilmente ai cambiamenti o agli imprevisti.


In riferimento al tuo progetto:

Vi siete organizzati giorno per giorno, definendo gli obiettivi in base all’evoluzione del progetto (in stile scrum daily meeting).

Avete discusso e assegnato i compiti in modo collaborativo e dinamico.

Avete fatto attenzione alla formazione reciproca, cercando di colmare le lacune individuali (un concetto caro all'agilità: team cross-funzionali).

Avete adattato la pianificazione in base a come andavano avanti i lavori.-->

# 2. 

# 3. Struttura del progetto in classi, blueprint - Matteo Ariotti
## Cosa é una classe?
- Una classe è un modello per l'istanza di un oggetto e questo oggetto ha le caratteristiche definite nel suo costruttore.
Es. of costruttore

```python
class Personaggio:
    def __init__(self, nome, salute, attacco, destrezza):
        self.nome = nome
        self.salute = salute
        self.attacco = attacco
        self.destrezza = destrezza
```
Es. di instanziazione

```python
personaggio1 = Personaggio("Alex", 100, 10, 15)
personaggio2 = Personaggio("Rex", 80, 8, 12)
```
Queste sono le caratteristiche dell'oggetto che verrà creato.
Ogni classe può avere i suoi metodi, ovvero delle azioni che puo eseguire l'oggetto.

Es. di un metodo

```python
class Personaggio:
    def attacca(self):
        print(f"{self.nome} attacca!")
    def subi
```
Ora quando verrà richiamato il metodo attacca, verrà stampato il nome del personaggi che sta abbaiando.


Es. di richiamo del metodo

```python
personaggio1.attacca() # Alex attacca!
personaggio2.attacca() # Rex attacca!
```
Seppur dovessimo avere diversi tipi di personaggi, possiamo usare lo stesso metodo per ogni personaggi e ottenere una stampa personalizzata agli attributi dei personaggi.

## Cosa é un blueprint?
Un blueprint è un oggetto che rappresenta una parte di un'applicazione web. In Flask usare blueprint permette un approccio modulare, suddividendo l'applicazione in componenti riutilizzabili e indipendenti, ognuno con le proprie route.
Quindi permette di gestire un grande progetto in maniera piú organizzata e scalabile, senza il bisogno di dipendere da altri.

Es. di un blueprint

```python
from flask import Blueprint

app_bp = Blueprint('app', __name__)

@app_bp.route('/home')
def home():
    return 'Hello, World!'
```
Questo blueprint ora che è stato creato potrà essere riutilizzato per altre applicazioni che ne avranno bisogno, evitando di riscrivere codice da 0.

## Perché gli abbiamo utilizzati per questo progetto?

Aver utilizzato i blueprint e le classi per il progetto ha permesso lo sviluppo in camere stagne di ogni singolo componente, senza il bisogno di dipendere da altri. Ciò permette di creare un grande progetto in maniera piú organizzata e con tempi ridotti.

Ogni blueprint/classe puó essere pensato come un mattoncino Lego. Ogni mattoncino ha delle sue caratteristiche (forma, colore, dimensioni) e puo essere riutilizzato per diverse costruzioni. 
Questo rende il lavoro svolto completamente riutilizzabile per futuri progetti, riducendo il carico di lavoro

-----------
- ### Standard per la documentazione, Docstring e Sphinx (Konrad)

#### Introduzione

Nel nostro progetto per mantenere traccia di quanto dovevevamo implementare (o che avevamo già implementato) nel codice abbiamo deciso di adottare uno standard comune per ridurre le possibilità di confusione tra i vari membri del team.
La scelta finale è caduta un approccio professionale basato su Sphinx e docstring in stile Google, garantendo una documentazione automatica, coerente e facilmente mantenibile per tutto il codice.

#### Sphinx: Il Motore della Documentazione

Sphinx è molto più di un semplice generatore di documentazione: è un ecosistema completo che trasforma il codice Python in documentazione web navigabile e professionale.

Perché Sphinx è Fondamentale
Sphinx non si limita a leggere i commenti nel codice. Attraverso il meccanismo di _importazione dinamica*, Sphinx esegue effettivamente il nostro codice Python per estrarre informazioni dettagliate su classi, metodi, parametri e type hints. Questo significa che ogni volta che modifichiamo una funzione, la documentazione si aggiorna automaticamente senza intervento manuale.

Come Funziona nel Nostro Progetto
La configurazione in conf.py definisce il comportamento del sistema:

```python
    # Sphinx "vede" il nostro codice grazie a questo path
    sys.path.insert(0, os.path.abspath('..'))
```

Questa riga è cruciale: dice a Sphinx dove trovare il nostro package saltatio_mortis, permettendogli di importare tutti i moduli.

Le estensioni sono il cuore del sistema:
    - **autodoc**: L'estensione che fa la "magia" - scansiona il codice Python, importa i moduli e estrae automaticamente firme delle funzioni, docstring e metadati
    - **napoleon**: Traduce le nostre docstring in stile Google nel formato reStructuredText che Sphinx comprende nativamente
    - **sphinx_autodoc_typehints**: Legge i type hints Python e li integra elegantemente nella documentazione finale

#### Standard DocString: Stile Google in Italiano

Abbiamo adottato lo stile Google per la sua leggibilità e il supporto nativo in Sphinx
(tra i vari formati disponibili (Sphinx nativo, NumPy, Google), quello di Google offre il miglior equilibrio tra leggibilità nel codice sorgente e ricchezza informativa).

Perché in Italiano
Abbiamo fatto la scelta consapevole di scrivere le docstring in italiano per diversi motivi:

1. Coerenza linguistica: Il progetto è sviluppato da un team italiano per un contesto italiano
2. Accessibilità: Facilita la comprensione per tutti i membri del team
3. Terminologia specifica: I termini del dominio del gioco (personaggio, missione, inventario) sono più naturali in italiano

_Esempio Pratico dal Nostro Codice_:

  ```python
      def usa_inventario_automatico(
      inventario: Inventario,
      pg: Personaggio,
      missione: Missione,
      bersagli: list[Personaggio],
      strategia: Strategia = None
  ) -> tuple[int | None, str]:
      """
      Utilizza un oggetto dall'inventario in modo automatico.

      Args:
          inventario (Inventario): L'inventario da cui utilizzare l'oggetto.
          pg (Personaggio): Il personaggio che utilizza l'oggetto.
          missione (Missione): La missione corrente.
          bersagli (list[Personaggio]): I bersagli dell'effetto dell'oggetto.
          strategia (Strategia, optional): Strategia da utilizzare.

      Returns:
          tuple[int | None, str]: Il risultato dell'uso dell'oggetto e messaggio descrittivo.

      Raises:
          None
      """
      """codice del metodo"""
  ```

Ogni docstring segue sempre la stessa struttura, seppur alcuni elementi possano essere opzionali:

- **Prima riga**: Descrizione concisa in una frase
- **Paragrafo descrittivo**: Contesto e dettagli implementativi quando necessario
- **Args**: Ogni parametro in ingresso con tipo e descrizione dettagliata
- **Returns**: Cosa restituisce la funzione
- **Raises**: Eccezioni che potrebbero essere sollevate
- **Example**: Esempi pratici di utilizzo quando utile

##### Integrazione di Type Hints

I type hints rappresentano un ponte fondamentale tra il codice moderno Python e la documentazione. Non sono semplici "decorazioni" - sono metadati che Sphinx utilizza per arricchire la documentazione.

Come Funzionano nella Pratica
Quando scriviamo:

  ```python
      def crea_personaggio(nome: str, classe: Type[Personaggio], livello: int = 1) -> Personaggio:
  ```

- Sphinx legge questi type hints e:
  1. **Valida la coerenza**: Controlla che la documentazione sia allineata con i tipi dichiarati
  2. **Genera collegamenti**: Crea automaticamente link tra classi correlate (Type[Personaggio] diventa un link cliccabile alla classe Personaggio)
  3. **Arricchisce la presentazione**: I tipi vengono mostrati in modo elegante nella documentazione finale

Vantaggi Pratici

1. **Sviluppo più sicuro**: Gli IDE possono fare controlli statici
2. **Refactoring sicuro**: Cambiare un tipo aggiorna automaticamente tutta la documentazione
3. **Navigazione intelligente**: Click su un tipo porta alla sua definizione
4. **Documentazione sempre aggiornata**: Impossibile avere disallineamento tra codice e docs

##### Generazione Automatica

Il processo di generazione della documentazione è il momento in cui tutto si unisce: codice, docstring, type hints e configurazione Sphinx convergono per produrre una documentazione web completa.

###### Il Processo Passo-Passo

  1. _Scansione dei file_: Sphinx legge tutti i file .rst nella directory docs/
  2. _Parsing delle direttive_: Interpreta le direttive .. automodule:: per sapere quali moduli documentare
  3. _Importazione dinamica_: Esegue i vari import per ogni modulo specificato
  4. _Estrazione metadati_: Legge docstring, type hints, firme delle funzioni, gerarchie di classe
  5. _Rendering HTML_: Trasforma tutto in pagine HTML navigabili

Dopo l'esecuzione, la directory build/html/ contiene:

- index.html: Homepage con overview del progetto
- Pagine per modulo: gioco.personaggio.html, auth.routes.html, etc.
- Indici: Indice generale, indice per moduli, ricerca
- Assets: CSS, JavaScript, font per il tema Furo
- Sitemaps: Per l'integrazione con motori di ricerca

###### Vantaggi del Processo Automatico

1) **Zero manutenzione**: Aggiungere una nuova funzione la rende automaticamente visibile nella documentazione
2) **Consistenza garantita**: Impossibile dimenticare di documentare qualcosa
3) **Ricerca integrata**: JavaScript automatico per cercare attraverso tutta la documentazione
4) **Responsive design**: Funziona perfettamente su mobile e desktop
5) **Velocità**: Build completo in pochi secondi anche per progetti grandi

La documentazione diventa così una "finestra vivente" sul nostro codice, che si aggiorna e evolve automaticamente insieme al progetto.

#### Benefici Ottenuti

1) Manutenibilità
    - La documentazione si aggiorna automaticamente con il codice
    - Nessuna possibilità di disallineamento tra docs e implementazione
2) Professionalità
    - Standard industriale riconosciuto
    - Navigazione intuitiva e ricerca integrata
    - Output HTML responsive e moderno (tema Furo)
3) Collaborazione
    - Standard condiviso tra tutti i membri del team
    - Facilita onboarding di nuovi sviluppatori
    - Code review più efficaci
4) Coerenza
    - Formato uniforme per tutto il progetto
    - Documenti sia funzioni pubbliche che private
    - Visualizzazione chiara delle gerarchie di classe

#### Conclusioni

  L'implementazione di Sphinx con docstring Google ha trasformato la nostra documentazione da un processo manuale e soggetto a errori in un sistema automatizzato che garantisce coerenza, completezza e professionalità, rappresentando una best practice fondamentale per qualsiasi progetto software serio.

# 4. ORM SQLAlchemy, Utenti, Admin e Privilegi - Fabrice Ghislain Tebou

Questa sezione del progetto gestisce la parte **backend relativa agli utenti**, i ruoli e i privilegi, sfruttando **Flask**, **SQLAlchemy** e il modulo di autenticazione **Flask-Login**.

## Funzionalità principali

- **Gestione utenti**: registrazione, login/logout e area personale.
  - La registrazione richiede nome utente, email, password e conferma password.
  - Il login/logout gestisce l’accesso al sistema con privilegi differenti in base al tipo di utente.
  - L’area personale permette di:
    - Creare personaggi (nome, classe: Mago, Ladro, Guerriero) con inventario iniziale.
    - Visualizzare e gestire i propri personaggi (inventario, dettagli, modifiche, eliminazione).
    - Aggiornare le informazioni personali.
    - Caricare crediti (solo Admin).
    - Eliminare l’account utente.

- **Ruoli e privilegi**:
  - **Utente standard (Player)**: può giocare, completare missioni e interagire con NPC.
  - **Admin**: oltre ai privilegi del Player, può:
    - Caricare crediti sugli account degli utenti.
    - Promuovere utenti da Player a Admin.

- **Sicurezza**:
  - Password protette tramite hashing (`generate_password_hash` e `check_password_hash` di Werkzeug).
  - Rotte protette con decoratori (`@login_required`, `@admin_required`).
  - Menu principale accessibile solo agli utenti autenticati.

---

## Struttura dati e ORM SQLAlchemy

Abbiamo scelto **SQLAlchemy** come ORM (Object Relational Mapper) al posto delle query SQL tradizionali per gestire i dati utente.  
Questa scelta ha portato vantaggi significativi in termini di **sicurezza**, **manutenibilità** e **astrazione dal database**.

### Vantaggi principali di SQLAlchemy

1. **Approccio orientato agli oggetti**  
   Permette di manipolare i dati come oggetti Python anziché tramite query testuali.  
   Le operazioni CRUD diventano semplici metodi (`db.session.add(user)`, `user.email`, ecc.), rendendo il codice più leggibile e pulito.

2. **Astrazione dal database**  
   SQLAlchemy funziona con diversi motori (SQLite, MySQL, PostgreSQL, ecc.) senza modifiche al codice.  
   Questo aumenta la **portabilità** e facilita la manutenzione a lungo termine.

3. **Sicurezza integrata**  
   Genera query automaticamente protette contro **SQL injection** e gestisce in modo sicuro transazioni e sessioni.

4. **Gestione semplificata delle relazioni**  
   Gestisce facilmente relazioni tra tabelle (one-to-many, many-to-many) senza dover scrivere JOIN manuali.

5. **Codice più pulito e meno ridondante**  
   I modelli rappresentano le tabelle e includono vincoli, relazioni e logica personalizzata.  
   Questo riduce il codice duplicato e migliora la scalabilità del backend.

6. **Integrazione naturale con Flask** 
   Con `Flask-SQLAlchemy` e `Flask-Login`, la gestione delle sessioni utente, dei ruoli e dell’autenticazione è diretta e sicura.

### Esempio pratico

**SQL classico:**
```python
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
user = cursor.fetchone()
```

**SQLAlchemy:**

```python
user = User.query.filter_by(email=email).first()
```

Il secondo approccio è più leggibile, sicuro e integrato con la logica dell’applicazione.

---

### Modelli principali

```python
class UserRole(enum.Enum):
    PLAYER = "PLAYER"
    ADMIN = "ADMIN"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    crediti = db.Column(db.Float, nullable=False)
    ruolo = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.PLAYER)
    character_ids = db.Column(JSON, nullable=False, default=list)

    def is_admin(self):
        return self.ruolo == UserRole.ADMIN

    def is_player(self):
        return self.ruolo == UserRole.PLAYER

    def has_role(self, role: str):
        return self.ruolo == UserRole[role]
```

---

## Esempi d’uso

* **Registrazione:**

  ```
  Nome utente: Antonio
  Email: antonio@gamer.it
  Password: 1234
  Conferma password: 1234
  ```

* **Login:**

  ```
  Email: antonio@gamer.it
  Password: 1234
  ```

---

## Bug noti / Limiti

* Sistema di **reset password** ancora da implementare.
* Miglioramenti possibili nella sicurezza (password più robuste, suggerimenti, politiche di complessità).
* Battaglie attualmente automatizzate: aggiungere modalità manuale.
* Possibilità futura di introdurre un ruolo `Developer` con accesso a una sezione **Statistics** per analisi utenti (livello, vittorie, tempo giocato, cluster comportamentali, ecc.).

---

## Update futuri

* Gestione avanzata dei privilegi per più tipi di Admin.
* Logging delle attività utente.
* Integrazione con interfaccia web per la gestione da Admin.
* Creazione dinamica di ruoli personalizzati.
* Possibilità di far giocare più personaggi contemporaneamente (funzionalità asincrona).

# 5. Transizione a Flask: dalla console all'applicazione web - Enrico Maddaloni

A un certo punto, durante lo sviluppo del progetto, a causa dell'aumentare della complessità dello stesso, è stato necessario dare un'interfaccia grafica al software.

> Invece di scrivere (*input*) e leggere (*output*) nel terminale, adesso scriviamo gli input e leggiamo gli output della nostra applicazione all'interno di pagine web (*templates*).

Come far comunicare questi *template* con la nostra applicazione?

## Flask: cos'è Flask?

**Flask** è un framework (letteralmente un'*impalcatura* che facilita il lavoro) Python che ci aiuta a gestire le interazioni tra l'applicazione e le pagine web, creando, per l'appunto, un'**applicazione web**.

## Come abbiamo effettuato la transizione a Flask:

- Abbiamo isolato la logica del programma dal resto, eliminando tutte le richieste di input e gli output in terminale.

Con un'**interfaccia web**, cambiano alcune cose:

- **Input:** vengono sostituiti con form e pulsanti. Questo sarà per l'utente il modo di comunicare con il software. Quando l'utente preme un pulsante, il browser (Es. Google Chrome, Firefox...) manda i dati al programma, che li elabora e restituisce un risultato.
- **Output:** il risultato di queste elaborazioni viene inviato a schermo su pagine web interattive.

- Una volta ottenuta un'applicazione web funzionante, abbiamo curato, anche se essenzialmente, il layout e lo stile delle pagine web.

## I vantaggi della transizione

- **Accessibilità:** Chiunque può utilizzare l'applicazione da browser. L'interfaccia web permette di inserire dati, cliccando pulsanti invece di scrivere comandi in console.
- **Flessibilità:** Una volta portato il programma su web, diventa molto più facile l'aggiunta e il testing di nuove funzionalità


# 6. Standard per la documentazione, Docstring e Sphinx - Konrad Chiara

Questo file contiene due versioni della presentazione: una da 5 minuti e 30 secondi e una da 5 minuti.

---

## Versione 1 — Presentazione completa (5 minuti e 30 secondi)

### Introduzione (30 secondi)

Buongiorno, oggi vi parlerò degli standard per la documentazione adottati nel nostro progetto "Saltatio Mortis".

Nel nostro team abbiamo dovuto affrontare una sfida comune: come mantenere traccia di ciò che dovevamo implementare e di quello che avevamo già sviluppato, evitando confusione tra i membri del team.

La nostra soluzione è stata adottare un approccio professionale basato su **Sphinx** e **docstring in stile Google**, che garantisce documentazione automatica, coerente e facilmente mantenibile per tutto il codice.

### Sphinx: Il Motore della Documentazione (2 minuti)

Sphinx è molto più di un semplice generatore di documentazione: è un ecosistema completo che trasforma il nostro codice Python in documentazione web navigabile e professionale.

La caratteristica fondamentale di Sphinx è che non si limita a leggere i commenti nel codice. Attraverso il meccanismo di **importazione dinamica**, Sphinx esegue effettivamente il nostro codice Python per estrarre informazioni dettagliate su classi, metodi, parametri e type hints. Questo significa che ogni volta che modifichiamo una funzione, la documentazione si aggiorna automaticamente senza intervento manuale.

Nel nostro progetto, la configurazione in `conf.py` è cruciale. La riga più importante è:

```python
import os, sys
# Sphinx "vede" il nostro codice grazie a questo path
sys.path.insert(0, os.path.abspath('..'))
```

Questa riga dice a Sphinx dove trovare il nostro package `saltatio_mortis`, permettendogli di importare tutti i moduli.

Le estensioni sono il cuore del sistema e ne abbiamo configurate tre fondamentali:

- **autodoc**: scansiona il codice Python, importa i moduli ed estrae automaticamente firme delle funzioni, docstring e metadati
- **napoleon**: traduce le nostre docstring in stile Google nel formato reStructuredText che Sphinx comprende nativamente
- **sphinx_autodoc_typehints**: legge i type hints Python e li integra elegantemente nella documentazione finale

### Standard DocString: Stile Google in Italiano (2 minuti)

Abbiamo adottato lo stile Google per la sua leggibilità e il supporto nativo in Sphinx. Tra i vari formati disponibili (Sphinx nativo, NumPy, Google), quello Google offre il miglior equilibrio tra leggibilità nel codice sorgente e ricchezza informativa.

Abbiamo fatto la scelta consapevole di scrivere le docstring in italiano per:

1. Coerenza linguistica (team e contesto italiano)
2. Accessibilità per tutti i membri del team
3. Terminologia del dominio (personaggio, missione, inventario) più naturale

Esempio pratico dal nostro codice:

```python
def usa_inventario_automatico(
    inventario: Inventario,
    pg: Personaggio,
    missione: Missione,
    bersagli: list[Personaggio],
    strategia: Strategia | None = None,
) -> tuple[int | None, str]:
    """
    Utilizza un oggetto dall'inventario in modo automatico.

    Args:
        inventario (Inventario): L'inventario da cui utilizzare l'oggetto.
        pg (Personaggio): Il personaggio che utilizza l'oggetto.
        missione (Missione): La missione corrente.
        bersagli (list[Personaggio]): I bersagli dell'effetto dell'oggetto.
        strategia (Strategia, optional): Strategia da utilizzare.

    Returns:
        tuple[int | None, str]: Il risultato dell'uso dell'oggetto e messaggio descrittivo.
    """
```

Ogni docstring segue una struttura standard: descrizione concisa, parametri con tipo e descrizione, cosa restituisce, ed eventuali eccezioni.

### Type Hints e Automazione (30 secondi)

I type hints sono metadati che Sphinx utilizza per arricchire la documentazione.

Sphinx con i type hints:

- Valida la coerenza tra documentazione e tipi dichiarati
- Genera collegamenti automatici tra classi correlate
- Mostra i tipi in modo elegante nella documentazione finale

Il processo è automatico: Sphinx scansiona i file, importa i moduli, estrae docstring e type hints e genera HTML navigabile con ricerca.

### Benefici e Conclusioni (30 secondi)

Benefici principali:

1. Manutenibilità: documentazione sempre aggiornata con il codice
2. Professionalità: standard industriale, navigazione intuitiva, output moderno
3. Collaborazione: standard condiviso, onboarding più facile, code review efficaci
4. Coerenza: formato uniforme e gerarchie di classe chiare

Conclusione: Sphinx con docstring Google ha trasformato la documentazione in una "finestra vivente" sul codice, automatizzata, coerente e professionale.

---

## Versione 2 — Presentazione ridotta (5 minuti)

### Introduzione (45 secondi)

Buongiorno, oggi vi parlerò degli standard per la documentazione adottati nel nostro progetto "Saltatio Mortis".

Per evitare confusione e allineare il team, abbiamo adottato **Sphinx** con **docstring in stile Google** per ottenere documentazione automatica e sempre aggiornata.

### Sphinx: Il Sistema di Documentazione (2 minuti)

Sphinx trasforma il codice Python in documentazione web navigabile ed esegue **importazione dinamica** del codice per estrarre firme, docstring e type hints. Ogni modifica al codice aggiorna la documentazione.

Configurazione chiave in `conf.py`:

```python
import os, sys
sys.path.insert(0, os.path.abspath('..'))
```

Estensioni principali:

- **autodoc** (import e estrazione automatica)
- **napoleon** (docstring Google)
- **sphinx_autodoc_typehints** (integrazione type hints)

### DocString in Stile Google (1 minuto e 30 secondi)

Scelto per equilibrio tra leggibilità e completezza. Docstring in italiano per coerenza e chiarezza di dominio.

Esempio sintetico:

```python
def usa_inventario_automatico(
    inventario: Inventario,
    pg: Personaggio,
    strategia: Strategia | None = None,
) -> tuple[int | None, str]:
    """
    Utilizza un oggetto dall'inventario in modo automatico.

    Args:
        inventario (Inventario): Fonte dell'oggetto.
        pg (Personaggio): Utilizzatore.
        strategia (Strategia, optional): Strategia da applicare.

    Returns:
        tuple[int | None, str]: Risultato e messaggio.
    """
```

Struttura essenziale: descrizione, Args, Returns, (Raises quando serve).

### Type Hints e Automazione (45 secondi)

I type hints permettono collegamenti automatici e coerenza. Processo in 4 passi: scansiona file, importa moduli, estrae docstring e type hints, genera HTML con ricerca.

### Benefici e Chiusura (45 secondi)

1. Zero manutenzione manuale
2. Standard professionale con ricerca
3. Collaborazione più semplice
4. Coerenza di formato

Conclusione: documentazione come "finestra vivente" che evolve con il progetto.

# 7. Raspberry