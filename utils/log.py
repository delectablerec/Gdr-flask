# importo di datetime per la registrazione degli eventi
from datetime import datetime
import os
class Log:
    """Classe per la registrazione degli eventi del gioco."""
    @staticmethod
    def scrivi_log(messaggio: str) -> None:
        """
        Registra un messaggio con timestamp direttamente nel file log.txt.

        Args:
            messaggio (str): Messaggio da registrare.

        Return:
            None
        """
        # creo cartella data se non esiste
        
        if not os.path.exists("data"):
            os.makedirs("data")
        
        with open("data/log.txt", "a", encoding="utf-8") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {messaggio}\n")
        
        

    @staticmethod
    def mostra_log() -> None:
        """
        Legge il file e stampa tutto quello che è successo nella partita

        Args:
            None

        Return:
            None
        """
        
        with open("data/log.txt", "r", encoding="utf-8") as file:
            print(file.read())
        