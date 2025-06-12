"""
Modulo per creare la struttura di cartelle e file di un progetto.

La struttura è definita da un dizionario che associa nomi di cartelle a liste di file.
"""

import os

# Definizione delle cartelle e dei file
structure = {
    "torneo": ["__init__.py", "torneo.py", "turno.py"],
    "personaggi": ["__init__.py", "personaggio.py", "classi.py"],
    "inventario": ["__init__.py", "inventario.py"],
    "oggetti": ["__init__.py", "oggetto.py"],
    "utils": ["__init__.py", "utils.py"],
}

# Cartella principale
base_dir = "progetto"
os.makedirs(base_dir, exist_ok=True)

# Creazione delle cartelle e file
for folder, files in structure.items():
    folder_path = os.path.join(base_dir, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, "w", encoding="utf-8") as f:
            pass  # crea file vuoto

# Creazione del main.py nella root
main_file_path = os.path.join(base_dir, "main.py")
with open(main_file_path, "w", encoding="utf-8") as f:
    pass  # file vuoto

print("Struttura cartelle e file creata con successo!")