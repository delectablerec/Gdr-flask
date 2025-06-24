from . import characters_bp
from flask import render_template, request, redirect, url_for, session, abort
from gioco.personaggio import Personaggio
from gioco.oggetto import Oggetto
from gioco.inventario import Inventario
from utils.log import Log

@characters_bp.route('/create_char', methods=['GET', 'POST'])
def create_char():

    classi = {cls.__name__: cls for cls in Personaggio.__subclasses__()}
    oggetti = {cls.__name__: cls for cls in Oggetto.__subclasses__()}

    if request.method == 'POST':
        nome = request.form['nome'].strip()
        classe_sel = request.form['classe']
        oggetto_sel = request.form['oggetto']

        pg = classi[classe_sel](nome)
        ogg = oggetti[oggetto_sel]()
        inv = Inventario(proprietario=pg.id)
        inv.aggiungi_oggetto(ogg)

        pg_list = session.get('personaggi', [])
        inv_list = session.get('inventari', [])

        pg_list.append(pg.to_dict())
        inv_list.append(inv.to_dict())

        session['personaggi'] = pg_list
        session['inventari'] = inv_list

        Log.scrivi_log(f"Creato personaggio: {pg.nome}, Classe: {classe_sel}, id: {pg.id}, Oggetto iniziale: {oggetto_sel}")

        return redirect(url_for('gioco.index'))

    return render_template(
        'create_char.html',
        classi=list(classi.keys()),
        oggetti=list(oggetti.keys())
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
