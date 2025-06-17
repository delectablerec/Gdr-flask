# Task per i msg e il passaggio ai template

- Scegli una classe, comunicalo agli altri
- importa :

```python
    from utils.messaggi import Messaggi
```
- dentro ogni metodo della classe per concatenare i msg dentro all'oggetto Messaggi usa il metodo add_to_messaggi
```python
    Messaggi.add_to_messaggi(msg)
```
- vanno anche concatenati a messaggi tutti i messaggi che vengono sollevati dalle eccezioni e che siano pertinenti al giocatore
