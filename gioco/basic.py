import uuid

class Basic():
    def __init__(self) -> None:
        """
        Classe base per gli oggetti di gioco.
        """
        self.id = uuid.uuid4()

    def to_dict(self) -> dict:
        """
        Serializza l'oggetto in un dizionario.

        Returns:
            dict: Rappresentazione dell'oggetto come dizionario.
        """
        return {
            'id': str(self.id),
            'classe': self.__class__.__name__
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Basic':
        """
        Deserializza un dizionario in un oggetto basic.

        Args:
            data (dict): Il dizionario da deserializzare.

        Returns:
            basic: L'oggetto basic deserializzato.
        """
        obj = cls()
        obj.id = uuid.UUID(data['id'])
        return obj
