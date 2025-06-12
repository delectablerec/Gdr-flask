from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from gioco.menu_principale import MenuPrincipale
from gioco.missione import MissioneFactory
from gioco.ambiente import AmbienteFactory
from gioco.scontro import Scontro

gioco = Blueprint('gioco', __name__, template_folder='../templates')

# Home / menu principale
@gioco.route('/')
def index():
    return render_template('menu.html')


# Nuovo gioco: form per creare la compagnia (1-3 PG)
@gioco.route('/new-game', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':
        # raccogli i dati dal form: liste di nomi/tuple
        personaggi_info = []
        initial_gifts = []
        # supponiamo che nel form ci siano campi personaggio-1-nome, personaggio-1-classe, gift-1, ecc.
        for i in range(1, 4):
            nome = request.form.get(f'pg{i}_nome')
            cls  = request.form.get(f'pg{i}_classe')
            gift = request.form.get(f'gift_{i}')
            if nome and cls:
                personaggi_info.append({"nome": nome, "classe": cls})
                initial_gifts.append(gift)
        mp = MenuPrincipale()
        compagnia = mp.crea_compagnia(personaggi_info, initial_gifts)  # :contentReference[oaicite:5]{index=5}
        # qui scegliamo la missione e creiamo lo scontro
        missione = None
        session['compagnia'] = mp.to_dict()
        return redirect(url_for('gioco.select_mission'))

    # GET: mostra i form di creazione PG
    classi = list(MenuPrincipale._classe_map.keys())
    gifts  = list(MenuPrincipale._oggetto_map.keys())
    return render_template('create_char.html', classi=classi, gifts=gifts)


# Seleziona missione e avvia Scontro
@gioco.route('/select-mission', methods=['GET', 'POST'])
def select_mission():
    if 'compagnia' not in session:
        return redirect(url_for('gioco.new_game'))

    if request.method == 'POST':
        missione_id = request.form['missione_id']
        missione = MissioneFactory.seleziona_da_id(missione_id)      # :contentReference[oaicite:6]{index=6}
        compagnia = MenuPrincipale.from_dict(session['compagnia']).personaggi_inventari
        s = Scontro(missione, compagnia)                            # :contentReference[oaicite:7]{index=7}
        session['scontro'] = s.to_dict()
        return redirect(url_for('gioco.battle'))

    missioni = MissioneFactory.get_opzioni()
    return render_template('select_mission.html', missioni=missioni)