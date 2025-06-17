
class Messaggi:
    """
    Si occupa di accumulare i messaggi che devono essere mostrati all'utente
    """
    messaggi=""

    @staticmethod
    def add_to_messaggi(msg:str):
            """
            Aggiunge un nuovo msg a messaggi, mandando a capo ad ogni nuovo msg

            Args:
                msg (str): nuovo msg da concatenare
            """
            if Messaggi.messaggi == "" :
                Messaggi.messaggi = msg
            else:
                Messaggi.messaggi = f"{Messaggi.messaggi}\n{msg}"

    @staticmethod
    def get_messaggi():
        return Messaggi.messaggi

    @staticmethod
    def delete_messaggi():
        Messaggi.messaggi=""

