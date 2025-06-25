from . import characters_bp
from flask import render_template, request, redirect, url_for, session, abort
from gioco.personaggio import Personaggio
from gioco.oggetto import Oggetto
from gioco.inventario import Inventario
from utils.log import Log


@characters_bp.route('/create_char', methods=['GET', 'POST'])
def create_char():

    if request.method == 'GET':
        # Costruisce i dizionari con le classi disponibili
        classi_disponibili = {cls.__name__: cls for cls in Personaggio.__subclasses__()}
        oggetti_disponibili = {cls.__name__: cls for cls in Oggetto.__subclasses__()}

    if request.method == 'POST':
        # Riceve i dati dal form
        nome_personaggio = request.form['nome_personaggio'].strip()
        classe_personaggio = request.form['classe_personaggio']
        oggetto_iniziale = request.form['oggetto_iniziale']

        print("📥 Dati ricevuti dal form:")
        print("  → Nome:", nome_personaggio)
        print("  → Classe:", classe_personaggio)
        print("  → Oggetto:", oggetto_iniziale)

        # Crea il personaggio e l'inventario
        nuovo_pg = classi_disponibili[classe_personaggio](nome_personaggio)
        oggetto = oggetti_disponibili[oggetto_iniziale]()
        inventario_pg = Inventario(proprietario=nuovo_pg.id)
        inventario_pg.aggiungi_oggetto(oggetto)

        # Salva nella sessione
        elenco_pg = session.get('personaggi', [])
        elenco_inventari = session.get('inventari', [])

        elenco_pg.append(nuovo_pg.to_dict())
        elenco_inventari.append(inventario_pg.to_dict())

        session['personaggi'] = elenco_pg
        session['inventari'] = elenco_inventari

        Log.scrivi_log(f"Creato personaggio: {nuovo_pg.nome}, Classe: {classe_personaggio}, id: {nuovo_pg.id}, Oggetto iniziale: {oggetto_iniziale}")

        return redirect(url_for('gioco.index'))

    # Primo accesso: mostra il form
    return render_template(
        'create_char.html',
        classi=list(classi_disponibili.keys()),
        oggetti=list(oggetti_disponibili.keys())
    )


@characters_bp.route('/view_characters')
def view_characters():
    Log.scrivi_log("Visualizzazione pagina personaggi (view_characters)")
    return render_template('view_characters.html')


@characters_bp.route('/personaggi', methods=['GET', 'POST'])
def mostra_personaggi():
    lista_pers = session.get('personaggi', [])
    Log.scrivi_log(f"Richiesta lista personaggi. Numero personaggi: {len(lista_pers)}")
    return render_template('list_char.html', personaggi=lista_pers)


@characters_bp.route('/personaggi/<int:id>')
def dettaglio_personaggio(id):
    lista_pers = session.get('personaggi', [])
    try:
        pg = lista_pers[id]
        Log.scrivi_log(f"Visualizzazione dettagli personaggio con ID: {pg.get('id')}, Nome: {pg.get('nome', 'N/A')}")
    except IndexError:
        Log.scrivi_log(f"Tentativo di accesso a personaggio inesistente con ID: {pg.get('id')}")
        abort(404)
    return render_template('details_char.html', pg=pg, id=id)


@characters_bp.route('/personaggi/<int:id>', methods=['POST'])
def elimina_personaggio(id):
    lista_pers = session.get('personaggi', [])
    try:
        pg = lista_pers.pop(id)
        session['personaggi'] = lista_pers
        Log.scrivi_log(f"Eliminato personaggio con ID: {pg.get('id')}, Nome: {pg.get('nome', 'N/A')}")
    except IndexError:
        Log.scrivi_log(f"Errore durante eliminazione: ID inesistente {pg.get('id')}")
        abort(404)
    return redirect(url_for('characters.mostra_personaggi'))
