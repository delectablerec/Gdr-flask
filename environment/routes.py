from flask import request, render_template, redirect, url_for, flash, session
from . import environment_bp
from gioco.ambiente import AmbienteFactory, Ambiente
from utils.log import Log


@environment_bp.route('/select-environment', methods=['GET', 'POST'])
def select_environment():
    if request.method == 'POST':
        ambiente_id = request.form.get('ambiente_id')
        ambiente = AmbienteFactory.seleziona_da_id(ambiente_id)
        session['ambiente'] = ambiente.to_dict()  # Salva l'ambiente in sessione
        msg = f"Ambiente selezionato: {ambiente.nome} (id: {ambiente_id})"
        flash(msg, 'success')
        Log.scrivi_log(msg)
        return redirect(url_for('environment.show_environment'))

    ambienti = AmbienteFactory.get_opzioni()
    return render_template('select_environment.html', ambienti=ambienti)


@environment_bp.route('/show-environment')
def show_environment():
    ambiente_data = session.get('ambiente')
    if not ambiente_data:
        msg = 'Nessun ambiente selezionato.'
        flash(msg, 'error')
        Log.scrivi_log(msg)
        return redirect(url_for('environment.select_environment'))

    ambiente = Ambiente.from_dict(ambiente_data)
    msg = f"Ambiente mostrato: {ambiente.nome}"
    flash(msg, 'info')
    Log.scrivi_log(msg)
    return render_template('show_environment.html', ambiente=ambiente)