from . import inventory_bp
from flask import render_template, request, session, redirect, url_for, flash
from gioco.oggetto import BombaAcida, Medaglione, Oggetto, PozioneCura
from gioco.personaggio import Personaggio
from gioco.classi import Ladro, Mago, Guerriero
from gioco.inventario import Inventario
from utils.messaggi import Messaggi
from utils.log import Log

@inventory_bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    personaggi = session.get('personaggi', [])
    inventari = session.get('inventari', [])

    nome_per_id = {p['id']: p['nome'] for p in personaggi}

    id_selezionato = None
    inventario_selezionato = None

    if request.method == 'POST':
        id_selezionato = request.form.get('personaggio_id')
        # Cerca l'inventario del personaggio selezionato
        for inv in inventari:
            if inv['proprietario'] == id_selezionato:
                inventario_selezionato = inv
                Log.scrivi_log(f"Inventario di {nome_per_id[id_selezionato]} selezionato.")

                break

    return render_template(
        'inventory.html',
        personaggi=personaggi,
        nome_per_id=nome_per_id,
        id_selezionato=id_selezionato,
        inventario=inventario_selezionato
    )

"""
@inventory_bp.route('/test-inventory', methods=['GET', 'POST'])
def test_inventory():
    # 1. Ottieni i dati dalla sessione
    personaggi_data = session.get('personaggi', [])
    inventari_data = session.get('inventari', [])

    if not personaggi_data or not inventari_data:
        return "Sessione non valida o incompleta", 400

    # 2. Crea il personaggio principale dinamicamente
    main_pg_data = personaggi_data[0]
    classe_pg = main_pg_data['classe']
    pg_classi = {'Mago': Mago, 'Guerriero': Guerriero, 'Ladro': Ladro}
    pg_test = pg_classi[classe_pg](main_pg_data['nome'])
    pg_test.__dict__.update(main_pg_data)  # importa attributi come salute, livello ecc.

    # 3. Crea inventario del personaggio
    inventario_pg_data = next((inv for inv in inventari_data if inv['proprietario'] == pg_test.id), None)
    inventario_pg = Inventario(pg_test)
    inventario_pg.oggetti = []
    for oggetto_data in inventario_pg_data['oggetti']:
        classe_oggetto = globals().get(oggetto_data['classe'])
        if classe_oggetto:
            oggetto = classe_oggetto()
            oggetto.__dict__.update(oggetto_data)
            inventario_pg.oggetti.append(oggetto)

    # 4. Crea bersagli (tutti i personaggi della sessione)
    bersagli = []
    bersagli_dict = {}
    for p_data in personaggi_data:
        cls = pg_classi.get(p_data['classe'])
        if cls:
            p = cls(p_data['nome'])
            p.__dict__.update(p_data)
            bersagli.append(p)
            bersagli_dict[p.id] = p

    # 5. Gestione POST
    oggetto_selezionato = request.form.get('oggetto')
    bersaglio_id = request.form.get('bersaglio')
    messaggio = None

    if request.method == 'POST':
        if 'action' in request.form and request.form['action'] == 'close':
            return redirect(url_for('gioco.index'))

        if oggetto_selezionato and bersaglio_id:
            oggetto = next((o for o in inventario_pg.oggetti if o.nome == oggetto_selezionato), None)
            bersaglio = bersagli_dict.get(bersaglio_id)
            if oggetto and bersaglio:
                inventario_pg.usa_oggetto(oggetto, utilizzatore=pg_test, bersaglio=bersaglio)
                messaggio = Messaggi.get_messaggi()
                Messaggi.delete_messaggi()
            else:
                messaggio = "Oggetto o bersaglio non trovato!"

    # 6. Prepara i dati per il template
    oggetti = [{"nome": o.nome} for o in inventario_pg.oggetti]
    bersagli_view = [
        {
            "id": b.id,
            "nome": b.nome,
            "salute": b.salute,
            "salute_max": getattr(b, "salute_max", 100),
            "classe": b.__class__.__name__,
            "tipologia": "Sè stesso" if b.id == pg_test.id else "Alleato"
        }
        for b in bersagli
    ]

    return render_template(
        'inventory.html',
        pg_nome=pg_test.nome,
        oggetti=oggetti,
        oggetto_selezionato=oggetto_selezionato,
        bersagli=bersagli_view if oggetto_selezionato else [],
        messaggio=messaggio
    )
    """