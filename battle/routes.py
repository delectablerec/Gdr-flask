from flask import redirect, render_template, session, url_for, request, flash
from flask_login import login_required

import os
import random
from . import battle_bp
from gioco.missione import Missione
from gioco.strategy import Strategia
from gioco.inventario import Inventario
from gioco.personaggio import Personaggio
from gioco.oggetto import Oggetto  # , TipoOggetto
from gioco.schemas.missione import MissioniSchema
from gioco.schemas.inventario import InventarioSchema
from gioco.schemas.personaggio import PersonaggioSchema
from characters.routes import load_char, get_owned_chars
from utils.helper import get_all_subclasses
from utils.salvataggio import Json
from utils.log import get_logger
from config import DATA_DIR_SAVE, DATA_DIR_INV, DATA_DIR_PGS
from config import load_leaderboard, update_leaderboard

path_save = os.path.join(
    DATA_DIR_SAVE, "salvataggio.json"
)
path_inv = os.path.join(
    DATA_DIR_INV, "inventario.json"
)

classi = {cls.__name__: cls for cls in Personaggio.__subclasses__()}
schema = PersonaggioSchema()
schema_inv = InventarioSchema()

logger = get_logger(__name__)
punteggio_iniziale = 0
nome_classi = [classe.__name__ for classe in get_all_subclasses(Personaggio)]


@battle_bp.route('/select_char', methods=['GET', 'POST'])
@login_required
def select_char():
    """
    Seleziona i personaggi per la battaglia.
    Mostra una lista di personaggi disponibili e
    consente di selezionarli per la battaglia.
    Metodo GET: Mostra la lista dei personaggi disponibili.
    Metodo POST: salva i personaggi selezionati, la missione corrente sul file
        specifico e reindirizza alla battaglia automatica.

    Returns:
        Rendered template: 'select_char.html' con i personaggi disponibili
            e la missione corrente o redirect alla battaglia automatica.

    """
    # if request.method == 'POST':
    # prendo i dati da sessione:
    missione_corrente = Json.carica_dati(path_save)['missione']
    pg_id_list = load_char()
    pg_list = get_owned_chars(pg_id_list)
    if request.method == 'POST':
        # Request.form.getlist restituisce una lista di stringhe
        indici_selezionati = request.form.getlist('selected_chars')
        battle_mode = request.form.get('battle_mode', 'auto')

        personaggi_selezionati = []
        # se nel form passi l'indice allora dobbiamo ricreare il personaggio
        # per conservare i dati in sessione
        for idx in indici_selezionati:
            try:
                # creazione oggetti
                for pgs in pg_list:
                    if idx == pgs['id']:
                        pg = schema.dump(pgs)
                personaggi_selezionati.append(pg)
            except (ValueError, IndexError):
                continue

        data_load = Json.carica_dati(path_save)
        if isinstance(data_load, dict):
            data_load['personaggi_selezionati'] = personaggi_selezionati
        else:
            msg = 'Dati non in formato corretto'
            flash(msg, 'error')
        # reset dei dati della battaglia per testing
        if "messaggi_battaglia" in data_load:
            # rimuove la chiave
            del data_load["messaggi_battaglia"]
        if "ordine_turni" in data_load:
            del data_load["ordine_turni"]
        if "indice_turno_corrente" in data_load:
            data_load["indice_turno_corrente"] = 0
        if "turno" in data_load:
            data_load["turno"] = 0
        if "nemici_generati" not in data_load:
            data_load["nemici_generati"] = False
        Json.scrivi_dati(path_save, data_load)

        """
        # inserisco l'id nella sessione
        session['personaggi_selezionati'] = [
            pg['id'] for pg in personaggi_selezionati]
        print("Personaggi selezionati", session['personaggi_selezionati'])
        """

        # reindirizzo verso la pagina di destinazione in base alla modalità
        if battle_mode == 'interactive':
            return redirect(url_for('battle.full_battle'))
        else:
            return redirect(url_for('battle.auto_battle'))
    return render_template(
        'select_char.html',
        personaggi=pg_list,
        missione_corrente=missione_corrente
        )


@battle_bp.route('/auto_battle', methods=['GET'])
@login_required
def auto_battle():
    if os.path.exists(path_save):
        # --- SETUP DATI ---
        setup = setup_battle()
        missione_obj = setup[0]
        ambiente_obj = missione_obj.ambiente
        nemici_obj = missione_obj.nemici

        personaggi_selezionati_obj = setup[1]

        tutti_personaggi = personaggi_selezionati_obj + nemici_obj

        inventari = []
        inventari_pg = setup[2]
        inventari += inventari_pg
        inventari += missione_obj.inventari_nemici

        leaderboard_data = setup[3]
        save_data = Json.carica_dati(path_save)
        punteggio = punteggio_iniziale
        partite_giocate = leaderboard_data.get("partite_giocate", 0)
        partite_vinte = leaderboard_data.get("partite_vinte", 0)

        # Inizializza messaggi e ordine turni se non presenti
        if 'ordine_turni' not in save_data:
            ordine_turni = ordine_iniziativa(tutti_personaggi)
            save_data['ordine_turni'] = ordine_turni
            # Incrementa solo all'inizio di una nuova battaglia
            partite_giocate += 1
        if 'turno' not in save_data:
            save_data['turno'] = 0
        if 'indice_turno_corrente' not in save_data:
            save_data['indice_turno_corrente'] = 0

        if 'messaggi_battaglia' not in save_data:
            save_data['messaggi_battaglia'] = []

        ordine_turni = save_data['ordine_turni']
        indice_turno = save_data['indice_turno_corrente']

        battaglia_finita = False
        vittoria = False

        if not battaglia_finita:

            save_data['ordine_turni'] = ordine_turni

            if indice_turno >= len(ordine_turni):
                indice_turno = 0

            save_data['indice_turno_corrente'] = indice_turno
            personaggio_turno_corrente = None
            for p in tutti_personaggi:
                if str(p.id) == ordine_turni[indice_turno]:
                    if not p.sconfitto():
                        personaggio_turno_corrente = p
                        save_data['turno'] += 1
                        # ----- SEPARATORE DI TURNO -----
                        save_data['messaggi_battaglia'].append(
                            f"<hr><div class='text-center text-primary "
                            f"fw-bold my-2'>------- TURNO {save_data['turno']}"
                            f" -------</div>"
                        )
                        break

            if not personaggio_turno_corrente:
                # Nessun personaggio disponibile, skip turno
                save_data['indice_turno_corrente'] = (
                    (indice_turno + 1) % len(ordine_turni)
                )
                Json.scrivi_dati(path_save, save_data)
                return redirect(url_for('battle.auto_battle'))

            save_data['messaggi_battaglia'].append(
                f"È il turno di {bold(personaggio_turno_corrente.nome)}"
            )

            # Uso dell'inventario in maniera automatica
            inventario = None
            for inv in inventari:
                if (
                    isinstance(inv, Inventario)
                    and inv.id_proprietario == personaggio_turno_corrente.id
                ):
                    inventario = inv
                    break

            result = usa_inventario_automatico(
                inventario,
                personaggio_turno_corrente,
                missione_obj,
                (nemici_obj + personaggi_selezionati_obj)
            )
            txt = result[1]
            if txt:
                save_data['messaggi_battaglia'].append(txt)

            if personaggio_turno_corrente.npc:
                bersagli_validi = [
                    p for p in personaggi_selezionati_obj if not p.sconfitto()
                ]
            else:
                bersagli_validi = [n for n in nemici_obj if not n.sconfitto()]

            if bersagli_validi:
                bersaglio = random.choice(bersagli_validi)
                danno, msg = personaggio_turno_corrente.attacca(
                    ambiente_obj.mod_attacco
                )
                if danno > 0:
                    msg = (
                        f"{bold(personaggio_turno_corrente.nome)} attacca "
                        f"{bold(bersaglio.nome)} per "
                        f"<span class='text-danger fw-bold'>{danno}</span> "
                        f"danni!"
                    )
                elif danno == 0:
                    msg = (
                        f"{bold(personaggio_turno_corrente.nome)} attacca "
                        f"{bold(bersaglio.nome)} ma non infligge danni!"
                    )
                else:
                    msg = (
                        f"{bold(personaggio_turno_corrente.nome)} "
                        f"tenta di attaccare "
                        f"{bold(bersaglio.nome)} ma fallisce!"
                    )

                bersaglio.subisci_danno(danno)
                save_data['messaggi_battaglia'].append(msg)

                if bersaglio.sconfitto():
                    punteggio += calcola_punteggio(bersaglio)
                    ordine_turni.remove(str(bersaglio.id))
                    save_data['messaggi_battaglia'].append(
                        f"{bold(bersaglio.nome)} è stato <span "
                        f"class='text-danger fw-bold'>sconfitto!</span>"
                    )

            save_data['personaggi_selezionati'] = PersonaggioSchema(
                many=True
            ).dump(personaggi_selezionati_obj)
            missione_obj.nemici = nemici_obj
            save_data['missione'] = MissioniSchema().dump(missione_obj)

            save_data['indice_turno_corrente'] = (
                (indice_turno + 1) % len(ordine_turni)
            )
            Json.scrivi_dati(path_save, save_data)
            pc_vivi = [
                p for p in personaggi_selezionati_obj if not p.sconfitto()
            ]
            npc_vivi = [p for p in nemici_obj if not p.sconfitto()]
            if not pc_vivi:
                battaglia_finita = True
                vittoria = False
                punteggio -= 5 * len(npc_vivi)
                partite_giocate += 1
                save_data['messaggi_battaglia'].append(
                    "<span class='text-danger fw-bold'>Tutti i personaggi "
                    "sono stati sconfitti!</span>"
                )
            elif not npc_vivi:
                battaglia_finita = True
                vittoria = True
                punteggio += 10 * len(pc_vivi)  # Bonus per vittoria
                partite_vinte += 1
                partite_giocate += 1
                assegna_premi(
                    missione_obj,
                    save_data['messaggi_battaglia'],
                    personaggi_selezionati_obj,
                    inventari_pg
                )
                for char in pc_vivi:
                    mod_ambiente = ambiente_obj.modifica_cura(
                        char, nome_soggetto=char
                    )
                    char.recupera_salute(mod_ambiente)
                save_data['messaggi_battaglia'].append(
                    "<span class='text-success fw-bold'>Tutti i nemici sono "
                    "stati sconfitti! Vittoria!</span>"
                )

        # update dei valori della leaderboard
        leaderboard_data["partite_giocate"] = partite_giocate
        leaderboard_data["partite_vinte"] = partite_vinte
        leaderboard_data["punteggio"] += punteggio
        user_id = str(session.get('_user_id', ''))
        update_leaderboard(user_id, leaderboard_data)

        # Salva stato, aggiorna file
        for pg in personaggi_selezionati_obj:
            file_name = f"{pg.id}.json"
            pg_path = os.path.join(DATA_DIR_PGS, file_name)
            inv_path = os.path.join(DATA_DIR_INV, file_name)
            if pg.sconfitto():
                if os.path.exists(pg_path):
                    os.remove(pg_path)
                if os.path.exists(inv_path):
                    os.remove(inv_path)
            else:
                Json.scrivi_dati(pg_path, PersonaggioSchema().dump(pg))
                for inv in inventari_pg:
                    if isinstance(inv, Inventario):
                        if inv.id_proprietario == pg.id:
                            inventario = inv
                            Json.scrivi_dati(
                                inv_path, InventarioSchema().dump(inventario)
                            )

        save_data['missione'] = MissioniSchema().dump(missione_obj)
        Json.scrivi_dati(path_save, save_data)

        if battaglia_finita is True:
            os.remove(path_save)

        return render_template(
            'auto_battle.html',
            battaglia_finita=battaglia_finita,
            vittoria=vittoria,
            messaggi=save_data['messaggi_battaglia'],
            personaggi=personaggi_selezionati_obj,
            nemici=nemici_obj,
            missione=missione_obj,
            pc_vivi=pc_vivi,
            npc_vivi=npc_vivi
        )
    else:
        flash('Non esiste il file di salvataggio', 'danger')
        return redirect(url_for('mission.select_mission'))


def _inizializza_dati_battaglia(save_data, tutti_personaggi, leaderboard_data):
    """
    Inizializza i dati della battaglia se non presenti.

    Args:
        save_data: Dati salvati della battaglia
        tutti_personaggi: Lista di tutti i personaggi
        leaderboard_data: Dati della leaderboard

    Returns:
        tuple: (ordine_turni, indice_turno, partite_giocate)
    """
    partite_giocate = leaderboard_data.get("partite_giocate", 0)

    if 'ordine_turni' not in save_data:
        ordine_turni = ordine_iniziativa(tutti_personaggi)
        save_data['ordine_turni'] = ordine_turni
        partite_giocate += 1
    if 'turno' not in save_data:
        save_data['turno'] = 0
    if 'indice_turno_corrente' not in save_data:
        save_data['indice_turno_corrente'] = 0
    if 'messaggi_battaglia' not in save_data:
        save_data['messaggi_battaglia'] = []

    ordine_turni = save_data['ordine_turni']
    indice_turno = save_data['indice_turno_corrente']

    return ordine_turni, indice_turno, partite_giocate


def _trova_personaggio_turno_corrente(
    tutti_personaggi, ordine_turni, indice_turno
):
    """
    Trova il personaggio del turno corrente.

    Args:
        tutti_personaggi: Lista di tutti i personaggi
        ordine_turni: Ordine dei turni
        indice_turno: Indice del turno corrente

    Returns:
        Personaggio o None
    """
    if indice_turno >= len(ordine_turni):
        indice_turno = 0

    for p in tutti_personaggi:
        if str(p.id) == ordine_turni[indice_turno]:
            if not p.sconfitto():
                return p
    return None


def _trova_inventario_corrente(inventari, personaggio_turno_corrente):
    """
    Trova l'inventario del personaggio corrente.

    Args:
        inventari: Lista degli inventari
        personaggio_turno_corrente: Personaggio del turno corrente

    Returns:
        Inventario o None
    """
    if not personaggio_turno_corrente:
        return None

    for inv in inventari:
        if (isinstance(inv, Inventario) and
                inv.id_proprietario == personaggio_turno_corrente.id):
            return inv
    return None


def _gestisci_azione_form(
    action, personaggio_turno_corrente, inventario_corrente, request
):
    """
    Gestisce le azioni dei form (show_attack, show_items, select_item).

    Returns:
        dict: Dizionario con le variabili di stato del form
    """
    form_state = {
        'show_attack_form': False,
        'show_item_selection': False,
        'show_item_target': False,
        'selected_item': None,
        'item_needs_target': False,
        'aspetta_azione_giocatore': False
    }

    if action == 'show_attack':
        if not personaggio_turno_corrente.npc:
            form_state['show_attack_form'] = True
            form_state['aspetta_azione_giocatore'] = True

    elif action == 'show_items':
        if not personaggio_turno_corrente.npc:
            form_state['show_item_selection'] = True
            form_state['aspetta_azione_giocatore'] = True

    elif action == 'select_item':
        item_id = request.form.get('item_id')
        if item_id and inventario_corrente:
            for oggetto in inventario_corrente.oggetti:
                if str(oggetto.id) == item_id:
                    form_state['selected_item'] = oggetto
                    form_state['show_item_target'] = True
                    form_state['aspetta_azione_giocatore'] = True
                    # Verifica se l'oggetto ha bisogno di un bersaglio
                    if (hasattr(oggetto, 'tipo_oggetto') and
                            'OFFENSIVO' in str(oggetto.tipo_oggetto)):
                        form_state['item_needs_target'] = True
                    break

    return form_state


def _gestisci_attacco_giocatore(
    request, personaggio_turno_corrente, nemici_obj, ambiente_obj, save_data,
    ordine_turni, indice_turno
):
    """
    Gestisce l'attacco del giocatore.

    Returns:
        tuple: (success, punteggio_aggiunto)
    """
    target_id = request.form.get('target_id')
    punteggio_aggiunto = 0

    if target_id and not personaggio_turno_corrente.npc:
        bersaglio = None
        for nemico in nemici_obj:
            if (str(nemico.id) == target_id and not nemico.sconfitto()):
                bersaglio = nemico
                break

        if bersaglio:
            save_data['turno'] += 1
            save_data['messaggi_battaglia'].append(
                f"<hr><div class='text-center text-primary "
                f"fw-bold my-2'>------- TURNO {save_data['turno']}"
                f" -------</div>"
            )
            save_data['messaggi_battaglia'].append(
                f"È il turno di {bold(personaggio_turno_corrente.nome)}"
            )

            danno, _ = personaggio_turno_corrente.attacca(
                ambiente_obj.mod_attacco
            )

            if danno > 0:
                msg = (
                    f"{bold(personaggio_turno_corrente.nome)} attacca "
                    f"{bold(bersaglio.nome)} per "
                    f"<span class='text-danger fw-bold'>{danno}</span> danni!"
                )
            elif danno == 0:
                msg = (
                    f"{bold(personaggio_turno_corrente.nome)} attacca "
                    f"{bold(bersaglio.nome)} ma non infligge danni!"
                )
            else:
                msg = (
                    f"{bold(personaggio_turno_corrente.nome)} "
                    f"tenta di attaccare {bold(bersaglio.nome)} ma fallisce!"
                )

            bersaglio.subisci_danno(danno)
            save_data['messaggi_battaglia'].append(msg)

            if bersaglio.sconfitto():
                punteggio_aggiunto = calcola_punteggio(bersaglio)
                ordine_turni.remove(str(bersaglio.id))
                save_data['messaggi_battaglia'].append(
                    f"{bold(bersaglio.nome)} è stato "
                    f"<span class='text-danger fw-bold'>sconfitto!</span>"
                )

            # Prossimo turno
            save_data['indice_turno_corrente'] = (
                (indice_turno + 1) % len(ordine_turni)
            )
            save_data['ordine_turni'] = ordine_turni
            return True, punteggio_aggiunto

    return False, punteggio_aggiunto


def _gestisci_uso_oggetto(
    request, personaggio_turno_corrente, inventario_corrente, nemici_obj,
    ambiente_obj, save_data, ordine_turni, indice_turno
):
    """
    Gestisce l'uso degli oggetti da parte del giocatore.

    Returns:
        tuple: (success, punteggio_aggiunto)
    """
    item_id = request.form.get('item_id')
    use_target_id = request.form.get('use_target_id')
    punteggio_aggiunto = 0

    if item_id and inventario_corrente:
        oggetto_da_usare = None
        for oggetto in inventario_corrente.oggetti:
            if str(oggetto.id) == item_id:
                oggetto_da_usare = oggetto
                break

        if oggetto_da_usare:
            save_data['turno'] += 1
            save_data['messaggi_battaglia'].append(
                f"<hr><div class='text-center text-primary "
                f"fw-bold my-2'>------- TURNO {save_data['turno']}"
                f" -------</div>"
            )
            save_data['messaggi_battaglia'].append(
                f"È il turno di {bold(personaggio_turno_corrente.nome)}"
            )

            result = inventario_corrente.usa_oggetto(
                oggetto_da_usare, ambiente_obj
            )
            if result:
                value = result[0]

                if ('BUFF' in str(oggetto_da_usare.tipo_oggetto)):
                    txt = (
                        f"{bold(personaggio_turno_corrente.nome)} usa "
                        f"{bold(oggetto_da_usare.nome)} su se stesso"
                    )
                    personaggio_turno_corrente.attacco_max += value
                elif (
                    'OFFENSIVO' in str(oggetto_da_usare.tipo_oggetto)
                    and use_target_id
                ):
                    bersaglio = None
                    for nemico in nemici_obj:
                        if str(nemico.id) == use_target_id:
                            bersaglio = nemico
                            break
                    if bersaglio:
                        txt = (
                            f"{bold(personaggio_turno_corrente.nome)} "
                            f"usa {bold(oggetto_da_usare.nome)} su "
                            f"{bold(bersaglio.nome)} infliggendo "
                            f"{bold(-value)} HP di danno"
                        )
                        bersaglio.salute += value
                        if bersaglio.sconfitto():
                            punteggio_aggiunto = calcola_punteggio(bersaglio)
                            ordine_turni.remove(str(bersaglio.id))
                            save_data['messaggi_battaglia'].append(
                                f"{bold(bersaglio.nome)} è stato "
                                f"<span class='text-danger fw-bold'>"
                                f"sconfitto!</span>"
                            )
                elif ('RISTORATIVO' in str(oggetto_da_usare.tipo_oggetto)):
                    txt = (
                        f"{bold(personaggio_turno_corrente.nome)} usa "
                        f"{bold(oggetto_da_usare.nome)} su se stesso"
                    )
                    personaggio_turno_corrente.salute += value
                    if (personaggio_turno_corrente.salute >=
                            personaggio_turno_corrente.salute_max):
                        personaggio_turno_corrente.salute = (
                            personaggio_turno_corrente.salute_max
                        )
                        txt += ", che torna al massimo della salute."
                    else:
                        txt += (
                            f", recuperando <span class='text-success "
                            f"fw-bold'> {bold(value)}</span> HP."
                        )

                save_data['messaggi_battaglia'].append(txt)

            # Prossimo turno
            save_data['indice_turno_corrente'] = (
                (indice_turno + 1) % len(ordine_turni)
            )
            return True, punteggio_aggiunto

    return False, punteggio_aggiunto


def _gestisci_turno_npc(
    personaggio_turno_corrente, inventario_corrente,
    missione_obj, nemici_obj, personaggi_selezionati_obj,
    ambiente_obj, save_data, ordine_turni, indice_turno
):
    """
    Gestisce il turno automatico degli NPC.

    Returns:
        int: punteggio aggiunto
    """
    punteggio_aggiunto = 0

    save_data['turno'] += 1
    save_data['messaggi_battaglia'].append(
        f"<hr><div class='text-center text-primary "
        f"fw-bold my-2'>------- TURNO {save_data['turno']}"
        f" -------</div>"
    )
    save_data['messaggi_battaglia'].append(
        f"È il turno di {bold(personaggio_turno_corrente.nome)}"
    )

    # Uso automatico dell'inventario per NPC
    result = usa_inventario_automatico(
        inventario_corrente,
        personaggio_turno_corrente,
        missione_obj,
        (nemici_obj + personaggi_selezionati_obj)
    )
    txt = result[1]
    if txt:
        save_data['messaggi_battaglia'].append(txt)

    # Attacco automatico per NPC
    bersagli_validi = [
        p for p in personaggi_selezionati_obj if not p.sconfitto()
    ]
    if bersagli_validi:
        bersaglio = random.choice(bersagli_validi)
        danno, msg = personaggio_turno_corrente.attacca(
            ambiente_obj.mod_attacco
        )

        if danno > 0:
            msg = (
                f"{bold(personaggio_turno_corrente.nome)} attacca "
                f"{bold(bersaglio.nome)} per "
                f"<span class='text-danger fw-bold'>{danno}</span> danni!"
            )
        elif danno == 0:
            msg = (
                f"{bold(personaggio_turno_corrente.nome)} attacca "
                f"{bold(bersaglio.nome)} ma non infligge danni!"
            )
        else:
            msg = (
                f"{bold(personaggio_turno_corrente.nome)} tenta di "
                f"attaccare {bold(bersaglio.nome)} ma fallisce!"
            )

        bersaglio.subisci_danno(danno)
        save_data['messaggi_battaglia'].append(msg)

        if bersaglio.sconfitto():
            punteggio_aggiunto = calcola_punteggio(bersaglio)
            ordine_turni.remove(str(bersaglio.id))
            save_data['messaggi_battaglia'].append(
                f"{bold(bersaglio.nome)} è stato <span "
                f"class='text-danger fw-bold'>sconfitto!</span>"
            )

    # Prossimo turno
    save_data['indice_turno_corrente'] = (
        (indice_turno + 1) % len(ordine_turni)
    )

    return punteggio_aggiunto


def _verifica_fine_battaglia(
    personaggi_selezionati_obj, nemici_obj, save_data,
    ambiente_obj, missione_obj, inventari_pg
):
    """
    Verifica le condizioni di fine battaglia.

    Returns:
        tuple: (battaglia_finita, vittoria, pc_vivi, npc_vivi,
                punteggio_aggiunto, partite_vinte_aggiuntive)
    """
    pc_vivi = [p for p in personaggi_selezionati_obj if not p.sconfitto()]
    npc_vivi = [p for p in nemici_obj if not p.sconfitto()]
    punteggio_aggiunto = 0
    partite_vinte_aggiuntive = 0

    if not pc_vivi:
        battaglia_finita = True
        vittoria = False
        punteggio_aggiunto = -5 * len(npc_vivi)
        save_data['messaggi_battaglia'].append(
            "<span class='text-danger fw-bold'>Tutti i personaggi sono "
            "stati sconfitti!</span>"
        )
    elif not npc_vivi:
        battaglia_finita = True
        vittoria = True
        punteggio_aggiunto = 10 * len(pc_vivi)
        partite_vinte_aggiuntive = 1
        assegna_premi(
            missione_obj,
            save_data['messaggi_battaglia'],
            personaggi_selezionati_obj,
            inventari_pg
        )
        for char in pc_vivi:
            mod_ambiente = ambiente_obj.modifica_cura(char, nome_soggetto=char)
            char.recupera_salute(mod_ambiente)
        save_data['messaggi_battaglia'].append(
            "<span class='text-success fw-bold'>Tutti i nemici sono stati "
            "sconfitti! Vittoria!</span>"
        )
    else:
        battaglia_finita = False
        vittoria = False

    return (battaglia_finita, vittoria, pc_vivi, npc_vivi,
            punteggio_aggiunto, partite_vinte_aggiuntive)


def _salva_dati_battaglia(
    personaggi_selezionati_obj, inventari_pg,
    missione_obj, nemici_obj, save_data, battaglia_finita
):
    """
    Salva i dati della battaglia su file.
    """
    # Salva files
    for pg in personaggi_selezionati_obj:
        file_name = f"{pg.id}.json"
        pg_path = os.path.join(DATA_DIR_PGS, file_name)
        inv_path = os.path.join(DATA_DIR_INV, file_name)
        if pg.sconfitto():
            if os.path.exists(pg_path):
                os.remove(pg_path)
            if os.path.exists(inv_path):
                os.remove(inv_path)
        else:
            Json.scrivi_dati(pg_path, PersonaggioSchema().dump(pg))
            for inv in inventari_pg:
                if (isinstance(inv, Inventario) and
                        inv.id_proprietario == pg.id):
                    Json.scrivi_dati(inv_path, InventarioSchema().dump(inv))

    save_data['personaggi_selezionati'] = PersonaggioSchema(
        many=True
    ).dump(personaggi_selezionati_obj)
    missione_obj.nemici = nemici_obj
    save_data['missione'] = MissioniSchema().dump(missione_obj)
    Json.scrivi_dati(path_save, save_data)

    if battaglia_finita:
        os.remove(path_save)


@battle_bp.route('/full_battle', methods=['GET', 'POST'])
@login_required
def full_battle():
    """
    Gestisce una battaglia completa tra i personaggi e i nemici in cui l'utente
    può interagire con il combattimento scegliendo chi colpire e cosa usare
    di quanto presente nell'inventario mantenendo il controllo su ogni azione.
    Per gli NPC, l'azione viene gestita automaticamente come in auto_battle.
    """
    if not os.path.exists(path_save):
        flash('Non esiste il file di salvataggio', 'danger')
        return redirect(url_for('mission.select_mission'))

    # --- SETUP DATI ---
    setup = setup_battle()
    missione_obj = setup[0]
    ambiente_obj = missione_obj.ambiente
    nemici_obj = missione_obj.nemici
    personaggi_selezionati_obj = setup[1]
    inventari_pg = setup[2]
    leaderboard_data = setup[3]

    tutti_personaggi = personaggi_selezionati_obj + nemici_obj
    inventari = inventari_pg + missione_obj.inventari_nemici

    save_data = Json.carica_dati(path_save)
    punteggio = punteggio_iniziale
    partite_vinte = leaderboard_data.get("partite_vinte", 0)

    # Inizializza dati battaglia
    ordine_turni, indice_turno, partite_giocate = _inizializza_dati_battaglia(
        save_data, tutti_personaggi, leaderboard_data
    )

    # Variabili per controllare quale form mostrare
    show_attack_form = False
    show_item_selection = False
    show_item_target = False
    selected_item = None
    item_needs_target = False
    aspetta_azione_giocatore = False

    # Trova personaggio e inventario del turno corrente
    personaggio_turno_corrente = _trova_personaggio_turno_corrente(
        tutti_personaggi, ordine_turni, indice_turno
    )

    if not personaggio_turno_corrente:
        save_data['indice_turno_corrente'] = (
            (indice_turno + 1) % len(ordine_turni)
        )
        Json.scrivi_dati(path_save, save_data)
        return redirect(url_for('battle.full_battle'))

    inventario_corrente = _trova_inventario_corrente(
        inventari, personaggio_turno_corrente
    )

    # Gestione POST - azioni del giocatore
    if request.method == 'POST':
        action = request.form.get('action')

        # Gestione azioni form (show_attack, show_items, select_item)
        form_state = _gestisci_azione_form(
            action, personaggio_turno_corrente, inventario_corrente, request
        )
        show_attack_form = form_state['show_attack_form']
        show_item_selection = form_state['show_item_selection']
        show_item_target = form_state['show_item_target']
        selected_item = form_state['selected_item']
        item_needs_target = form_state['item_needs_target']
        aspetta_azione_giocatore = form_state['aspetta_azione_giocatore']

        # Gestione attacco giocatore
        if action == 'attack':
            success, punteggio_aggiunto = _gestisci_attacco_giocatore(
                request, personaggio_turno_corrente,
                nemici_obj, ambiente_obj, save_data,
                ordine_turni, indice_turno
            )
            if success:
                punteggio += punteggio_aggiunto
                Json.scrivi_dati(path_save, save_data)
                return redirect(url_for('battle.full_battle'))

        # Gestione uso oggetto
        elif action == 'use_item':
            success, punteggio_aggiunto = _gestisci_uso_oggetto(
                request, personaggio_turno_corrente, inventario_corrente,
                nemici_obj, ambiente_obj, save_data, ordine_turni, indice_turno
            )
            if success:
                punteggio += punteggio_aggiunto
                Json.scrivi_dati(path_save, save_data)
                return redirect(url_for('battle.full_battle'))

    # Gestione turno NPC
    if (personaggio_turno_corrente and personaggio_turno_corrente.npc and
            request.method == 'GET'):
        punteggio_aggiunto = _gestisci_turno_npc(
            personaggio_turno_corrente, inventario_corrente, missione_obj,
            nemici_obj, personaggi_selezionati_obj, ambiente_obj,
            save_data, ordine_turni, indice_turno
        )
        punteggio += punteggio_aggiunto

    # Gestione turno giocatore
    elif (personaggio_turno_corrente and not personaggio_turno_corrente.npc
            and request.method == 'GET'):
        aspetta_azione_giocatore = True

    # Verifica condizioni di fine battaglia
    result = _verifica_fine_battaglia(
        personaggi_selezionati_obj, nemici_obj, save_data,
        ambiente_obj, missione_obj, inventari_pg
    )
    battaglia_finita = result[0]
    vittoria = result[1]
    pc_vivi = result[2]
    npc_vivi = result[3]
    punteggio_aggiunto = result[4]
    partite_vinte_aggiuntive = result[5]
    punteggio += punteggio_aggiunto
    partite_vinte += partite_vinte_aggiuntive

    # Aggiorna leaderboard
    leaderboard_data["partite_giocate"] = partite_giocate
    leaderboard_data["partite_vinte"] = partite_vinte
    leaderboard_data["punteggio"] += punteggio
    user_id = str(session.get('_user_id', ''))
    update_leaderboard(user_id, leaderboard_data)

    # Salva dati battaglia
    _salva_dati_battaglia(
        personaggi_selezionati_obj, inventari_pg, missione_obj,
        nemici_obj, save_data, battaglia_finita
    )

    return render_template(
        'full_battle.html',
        battaglia_finita=battaglia_finita,
        vittoria=vittoria,
        messaggi=save_data['messaggi_battaglia'],
        personaggi=personaggi_selezionati_obj,
        nemici=nemici_obj,
        missione=missione_obj,
        pc_vivi=pc_vivi,
        npc_vivi=npc_vivi,
        aspetta_azione_giocatore=aspetta_azione_giocatore,
        personaggio_turno_corrente=personaggio_turno_corrente,
        inventario_corrente=inventario_corrente,
        show_attack_form=show_attack_form,
        show_item_selection=show_item_selection,
        show_item_target=show_item_target,
        selected_item=selected_item,
        item_needs_target=item_needs_target
    )


def setup_battle() -> tuple[Missione, list[Personaggio], list[Inventario]]:
    """
    Crea il setup dei dati prendendoli dai file json
    data/( save, inventari, personaggi)
    Deserializza i dati dai json e ritorna gli oggetti

    Returns:
        tuple:
            Missione: La missione deserializzata con dentro i suoi campi
                la lista dei nemici, l'ambiente, la lista degli inventari dei
                nemici e la lista dei premi.

            List[Personaggio]: La lista dei personaggi selezionati dei
                giocatori.

            List[Inventario]: La lista degli inventari dei giocatori.
    """
    # --- SETUP DATI ---
    save_data = Json.carica_dati(path_save)
    missione = save_data['missione']

    # print(f"MISSIONE DICT :{missione}")
    personaggi_selezionati = Json.carica_dati(path_save)[
        'personaggi_selezionati'
    ]
    # print(f"PERSONAGGI SELEZIONATI DICT :{personaggi_selezionati}")

    # Deserializzazione oggetti
    missione_obj = MissioniSchema().load(missione)
    personaggio_schema = PersonaggioSchema(many=True)
    personaggi_selezionati_obj = personaggio_schema.load(
        personaggi_selezionati
    )
    # print(f"PERSONAGGI_OBJ : {personaggi_selezionati_obj}")

    # Carico gli inventari dei personaggi:
    inventari_pg_obj = []
    inventario_schema = InventarioSchema()
    for pg in personaggi_selezionati_obj:
        if not pg.sconfitto():
            pg_inv_path = os.path.join(DATA_DIR_INV, f"{str(pg.id)}.json")
            inventario_pg = Json.carica_dati(pg_inv_path)
            inventario_pg_obj = inventario_schema.load(inventario_pg)
            inventari_pg_obj.append(inventario_pg_obj)

    # caricamento dati leaderboard user corrente
    user_id = str(session.get('_user_id', ''))
    user_leaderboard = load_leaderboard(user_id)

    if save_data["nemici_generati"] is False:
        nemici_casuali = generate_random_enemy(len(personaggi_selezionati))
        missione_obj.nemici = nemici_casuali[0]
        print("NEMICI CASUALI", missione_obj.nemici)
        missione_obj.inventari_nemici = nemici_casuali[1]
        print("INVENTARI NEMICI", missione_obj.inventari_nemici)
        save_data["nemici_generati"] = True

    Json.scrivi_dati(path_save, save_data)

    return (
        missione_obj,
        personaggi_selezionati_obj,
        inventari_pg_obj,
        user_leaderboard
    )


def calcola_punteggio(pg: Personaggio) -> int:
    """
    Calcola il punteggio ottenuto o perso per la sconfitta del personaggio.
    Args:
        pg (Personaggio): Il personaggio sconfitto.
    Returns:
        int: Il punteggio ottenuto o perso per la sconfitta del pg.
    """
    punti = punteggio_iniziale
    classe = type(pg).__name__
    if classe in nome_classi:
        if classe == 'Guerriero':
            punti += 10
        elif classe == 'Ladro':
            punti += 8
        elif classe == 'Mago':
            punti += 5
        else:
            punti += 2
    if not pg.npc:
        punteggio_negativo = - punti
        punti = punteggio_negativo
    return punti


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
        ambiente (Ambiente): L'ambiente in cui si trova il personaggio.
        bersagli (list[Personaggio]): I bersagli dell'effetto dell'oggetto.

    Returns:
        tuple[int | None, str]:
        Il risultato dell'uso dell'oggetto e un messaggio descrittivo.
    """
    ambiente = missione.ambiente
    result = None
    value = None
    check = True

    if strategia is None:
        strategia = missione.strategia_nemici

    bersagli = [
        bersaglio for bersaglio in bersagli
        if bersaglio.salute > 0
        and bersaglio != pg
        and bersaglio.npc != pg.npc
    ]

    if inventario is None:
        txt = f"{bold(pg.nome)} non ha un inventario! Errore!!!!."
        check = False
    elif inventario.oggetti is None:
        txt = f"{bold(pg.nome)} non ha più oggetti nell'inventario."
        check = False
    txt = ""
    if check:
        result = strategia.uso_inventario_npc(pg.salute, inventario, ambiente)

        if result is not None:
            # print(f"Result: {result}")
            value = result[0]
            oggetto = result[1]
            print("OGGETTO USATO :", oggetto, type(oggetto))
            if oggetto.tipo_oggetto == "TipoOggetto.BUFF":
                bersaglio = None
                txt = (
                    f"{bold(pg.nome)} usa {bold(oggetto.nome)} su se stesso, "
                )
                pg.attacco_max += value
            elif oggetto.tipo_oggetto == "TipoOggetto.OFFENSIVO":
                bersaglio = random.choice(bersagli)

                txt = (
                    f"{bold(pg.nome)} usa {bold(oggetto.nome)} su "
                    f"{bold(bersaglio.nome)} "
                    f"infliggendo {bold(-value)} HP di danno"
                )

                bersaglio.salute += value
            elif oggetto.tipo_oggetto == "TipoOggetto.RISTORATIVO":
                bersaglio = None
                txt = (
                    f"{bold(pg.nome)} usa {bold(oggetto.nome)} su se stesso"
                )
                pg.salute += value
                if pg.salute >= pg.salute_max:
                    pg.salute = pg.salute_max
                    txt += ", che torna al massimo della salute."
                else:
                    txt += (
                        f", recuperando <span class='text-success fw-bold'>"
                        f" {bold(value)}</span> HP."
                    )
        else:
            txt = f"{bold(pg.nome)} non utilizza oggetti in questo turno"
        logger.info(str(txt))
    return value, txt


def generate_random_enemy(
    number: int = 1
) -> list[tuple[Personaggio, Inventario]]:
    """
    Genera randomicamente dei nemici e il loro inventario sulla base della
    quantità richiesta.
    Utilizza le classi derivate da Personaggio e Oggetto per creare
    istanze di nemici e oggetti casuali.

    Args:
        number (int): Numero di nemici da generare, default è 1.

    Returns:
        list[tuple[Personaggio, Inventario]]:
            Una lista di tuple contenenti i nemici e i loro inventari.
    """
    nemici = []
    inventari_nemici = []
    for i in range(number):
        tipi_di_classi = list(get_all_subclasses(Personaggio))
        tipi_di_oggetti = list(get_all_subclasses(Oggetto))
        classe_sel = random.choice(tipi_di_classi)
        oggetto_sel = random.choice(tipi_di_oggetti)
        oggetto_obj = oggetto_sel()
        nemico_obj = classe_sel(nome=f"Nemico {i}")
        inventario_obj = Inventario(id_proprietario=nemico_obj.id)
        inventario_obj.aggiungi_oggetto(oggetto_obj)
        inventari_nemici.append(inventario_obj)
        nemici.append(nemico_obj)
    return nemici, inventari_nemici


# in ingresso lista di tutti i personaggi, e  sommo iniziativa + d20, ordino
# in base a qst, mettendo gli id
def ordine_iniziativa(tutti_personaggi):
    """
    Calcola l'iniziativa per ogni personaggio sommando il valore di iniziativa
    al tiro di un d20.
    Ritorna una lista ordinata di ID in base all'iniziativa decrescente.

    Args:
        personaggi (list): Lista di oggetti `Personaggio`.

    Returns:
        list: Lista ordinata di ID in base al punteggio iniziativa.
    """
    iniziativa = []
    for pg in tutti_personaggi:
        tiro = random.randint(1, 20)
        iniziativa.append((pg.id, pg.iniziativa + tiro))
    # Ordino per l'elemento 1 della tupla decrescente
    iniziativa.sort(key=lambda tuple: tuple[1], reverse=True)

    lista_ordinata_id = []
    for tupla in iniziativa:
        id = tupla[0]
        lista_ordinata_id.append(str(id))
    return lista_ordinata_id


def assegna_premi(
    missione: Missione,
    messaggi_battaglia: list[str],
    personaggi_selezionati: list[Personaggio],
    inventari: list[Inventario]
):
    """
    Da chiamare a fine scontro in caso di vittoria per assegnare
    i premi della missione agli inventari dei personaggi

    Args:
        missione (Missione): La missione corrente
        messaggi_battaglia (list[str]): Lista dei messaggi della battaglia
        personaggi_selezionati (list[Personaggio]): Personaggi selezionati dai
            giocatori
        inventari (list[Inventario]): Inventari dei personaggi giocanti

    Returns:
        None
    """
    for inventario in inventari:
        for pg in personaggi_selezionati:
            if inventario.id_proprietario == pg.id:
                for premio in missione.premi:
                    # QUESTA è una PORCATA , cè da rimettere mano nella lista
                    # premi di ogni missione
                    oggetti_map = {
                        subcls.__name__: subcls
                        for subcls in get_all_subclasses(Oggetto)
                    }
                    oggetto_cls = oggetti_map[premio.classe]
                    nuova_istanza = oggetto_cls()
                    messaggi_battaglia.append(
                        f"{bold(pg.nome)} ha ricevuto in premio "
                        f"{bold(nuova_istanza.nome)}"
                        )
                    inventario.aggiungi_oggetto(nuova_istanza)


def bold(txt):
    """
    Rende il testo in ingresso in grassetto nella pagina html.

    Args:
        txt (str): Il testo da rendere in grassetto.

    Returns:
        str: Il testo formattato in grassetto.
    """
    return f"<b>{txt}</b>"
