# Gioco di Ruolo - Web App Flask

## Obiettivo
Migrare ad una versione web del gioco di ruolo, utilizzando Flask per creare un'applicazione web che gestisca le funzionalità del gioco.

creazione ambiente virtuale
```bash
python -m venv venv
source venv/bin/activate # su Linux/Mac
venv\Scripts\activate # su Windows
```
## Installazione Flask
```bash
pip install Flask
pip install Flask-SQLAlchemy
pip install Flask-Login
pip install Flask-Session
```
## Aggiungere la folder static e templates
```bash
mkdir static templates
```
## Blueprint

In Flask un Blueprint è un modo per suddividere la tua applicazione in componenti riutilizzabili e indipendenti, ognuno con le proprie route, template e file statici.
In pratica il blueprint è uno “spazio dei nomi” e un “contenitore di route” che ti aiuta a mantenere il progetto modulare, organizzato e scalabile

Ti permette di:

**Organizzare il codice**
- Raggruppi insieme tutte le view (i “route”), i template e gli asset (CSS/JS) che riguardano un’area funzionale dell’app (es. autenticazione, API, pannello admin, parte di gioco), senza dover tenere tutto nel singolo file app.py.

**Riutilizzare e incapsulare**
- Puoi definire un blueprint in un package separato, testarlo o riutilizzarlo poi in altri progetti semplicemente importandolo e registrandolo, senza “sporcare” il namespace principale.

**Evitare import circolari**
- Suddividendo logica e route in moduli distinti, riduci la probabilità di dover importare app dentro moduli che a loro volta importano app, e via dicendo.

## Come si usa
```python
# gioco/routes.py
from flask import Blueprint, render_template

gioco = Blueprint('gioco', __name__, template_folder='../templates')

@gioco.route('/')
def index():
    return render_template('menu.html')
```
Blueprint('gioco', __name__) crea un nuovo “oggetto app” virtuale chiamato gioco.

Definisci con @gioco.route() tutte le view relative a quella parte dell’app.

Poi, nel file principale:

```python
# app.py
from flask import Flask
from gioco.routes import gioco  # import del blueprint

app = Flask(__name__)
app.register_blueprint(gioco)   # lo “attacchi” all’app principale
```
Da questo momento tutte le route definite in gioco (es. /, /battle, ecc.) diventano parte dell’applicazione vera e propria

## App.py
```python
from flask import Flask
from flask_session import Session
from gioco.routes import gioco

app = Flask(__name__)
app.config['SECRET_KEY'] = '...'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.register_blueprint(gioco)
```
## routes.py
In gioco/routes.py crea le viste Flask per:

- / (homepage / menu principale)
- /new-game (form per creare personaggi)
- /load-game (caricamento da sessione o file)
- /select-mission (scegli missione)
- /battle (gestione turni di combattimento)
- /inventory (visualizza e usa oggetti)

## templates
In templates/ crea:

- layout.html (base con navbar, footer)
- menu.html (bottoni per Nuovo Gioco / Carica Partita)
- create_char.html (form con nome e classe)
- select_mission.html (lista missioni disponibili)
- battle.html (mostra stato dei personaggi, inventario, pulsanti Azione / Usa Oggetto)

## Passaggi successivi
Ora che abbiamo impostato le basi dell'applicazione Flask:
- app.py per la configurazione principale
- routes.py per le route del gioco
- templates per i file HTML

Ecco i prossimi step prima di scendere nel dettaglio dei singoli file:

**Serializzazione degli oggetti di dominio**
– Aggiungere a tutte le classi principali (Personaggio, Missione, Ambiente, Oggetto, Inventario, ecc.) i metodi to_dict() e from_dict() (o from_json()) che trasformano lo stato interno in un dizionario serializzabile e ricreano l’istanza a partire da quel dizionario.
– Questo ci permetterà di salvare e ripristinare lo stato di gioco tramite la session di Flask o file JSON.

**Factory e liste di opzioni**
– Creare (o completare) i moduli PersonaggioFactory, MissioneFactory, AmbienteFactory che espongono:
- Un metodo per recuperare la lista delle opzioni disponibili (classe, missione, ambiente) sotto forma di {id: oggetto} o lista di tuple,
- Un metodo per “costruire” un’istanza dato l’id scelto dal form.

In questo modo le view Flask possono semplicemente fare factory.get_opzioni() per popolare il <select>, e poi factory.seleziona_da_id(id) per istanziare l’oggetto.

**Gestione dello stato di gioco in sessione**
– Decidere quali dati tenere in session: normalmente il personaggio e la missione corrente (o anche l’intero “gioco”).
– Alla ricezione di un POST in /battle, si ricostruisce lo stato da session, si esegue il turno, si rialimenta la pagina e si salva di nuovo in session.

**Integrazione del salvataggio/caricamento su file**
– Aggiungere in load_game e possibilmente in una route /save-game la logica di scrittura/lettura di un file JSON (o Pickle), per poter mantenere partite oltre la sessione.
– Usare un semplice form di upload/download o slot predefiniti.

**Static files e asset**
– Mettere in static/ eventuali CSS, immagini e script JS (ad es. per aggiornare dinamicamente il log di battaglia).
– Verificare che il template base (layout.html) punti correttamente a /static/....