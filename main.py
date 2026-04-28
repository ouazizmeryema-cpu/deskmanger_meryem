# -*- coding: utf-8 -*-

# point d'entrée de l'application Deskmanger
# Lance la base de donnée et l'interface graphique


import os
import sys
from database.database_manager import DatabaseManager
from ui.main_window import MainWindow

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def main():
    base = get_base_path()
    data_dir = os.path.join(base, "data")
    os.makedirs(data_dir, exist_ok=True)
    db = DatabaseManager(os.path.join(data_dir, "deskmanger"))
    app = MainWindow(db)
    app.lancer()
    db.fermer()

if __name__ == "__main__":
    main()