import os
from flask import Flask
from flask_session import Session
from gioco.routes import gioco

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

# Imposta una SECRET_KEY sicura (meglio via variabile d'ambiente)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia_questa_chiave_per_una_più_sicura')
app.config['SESSION_TYPE'] = 'filesystem'

# Inizializza il supporto alle sessioni sul filesystem
Session(app)

# Registra il blueprint che contiene tutte le route di gioco
app.register_blueprint(gioco)

if __name__ == '__main__':
    # Modalità di sviluppo con reload automatico
    app.run(host='0.0.0.0', port=5000, debug=True)