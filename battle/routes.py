from flask import redirect, render_template, session, url_for, request
from requests import request
from . import battle_bp
from gioco.personaggio import Personaggio
from gioco.inventario import Inventario
from gioco.ambiente import Ambiente, Foresta
from gioco.missione import Missione, GestoreMissioni
@battle_bp.route('/select_char', methods=['GET', 'POST'] )
def select_char():
    #if request.method == 'POST':

    #prendo i dati da sessione :
    personaggi=[]
    inventari=[]
    ambiente = Foresta()
    gestore_missioni = GestoreMissioni()
    missione_corrente = gestore_missioni.sorteggia()
    if 'ambiente' in session :
        #Recupero l'oggetto ambiente dalla sessione deserializzandolo
        ambiente = Ambiente.from_dict(session['ambiente'])
    if 'personaggi' in session and 'inventari' in session:
        pg_list = session.get('personaggi', [])
        inv_list = session.get('inventari',  [])
        #Deserializzo gli elementi delle liste
        print(pg_list)
        print(inv_list)
        """
        for serialized in  pg_list :
            personaggi.append(Personaggio.from_dict(serialized))
        for serialized in inv_list:
            inventari.append(Inventario.from_dict(serialized))
        #Ora le liste personaggi e  inventari contengono i dati deserializzati
        """
    # elementi_selezionati = request.form.getlist('personaggio_id')
    # if elementi_selezionati:
    #     for pg in pg_list:
    #         if pg['id'] in elementi_selezionati:
    #             personaggi.append(Personaggio.from_dict(pg))
    #             for inv in inv_list:
    #                 if pg == inv.proprietario:
    #                     inventari.append(Inventario.from_dict(inv))
    #                 break

    if request.method == 'POST':
        # Request.form.getlist restituisce una lista di stringhe
        indici_selezionati = request.form.getlist('selected_chars')
        personaggi_selezionati = []
        inventari_selezionati = []
        # se nel form passi l'indice iallora dobbiamo ricreare il personaggio per conservare i dati in sessione
        for idx in indici_selezionati:
            try:
                indice = int(idx)
                # creazione oggetti
                pg = Personaggio.from_dict(pg_list[indice])
                inv = Inventario.from_dict(inv_list[indice])
                # aggingiamo i personaggi alle liste
                personaggi_selezionati.append(pg)
                inventari_selezionati.append(inv)
            except (ValueError, IndexError):
                continue
        # serializzo le liste nella sessione
        session['personaggi_selezionati'] = [pg.to_dict() for pg in personaggi_selezionati]
        session['inventari_selezionati'] = [inv.to_dict() for inv in inventari_selezionati]
        # reindirizzo verso la pagina di destinazione
        return redirect(url_for(battle_bp.battle))
    # eventualmente carico la selezione precedente per avere dei vaolri di default
    selezionati_pg = []
    selezionati_inv = []
    if 'personaggi_selezionati' in session:
        for sec in session['personaggi_selezionati']:
            selezionati_pg.append(Personaggio.from_dict(sec))
        for sec in session.get('inventari_selezionati', []):
            selezionati_inv.append(Inventario.from_dict(sec))


    return render_template(
        'select_char.html',
        personaggi=pg_list,
        inventari=inv_list,
        ambiente_corrente = ambiente,
        missione_corrente = missione_corrente,
        selezionati_pg = selezionati_pg,
        selezionati_inv = selezionati_inv
    )