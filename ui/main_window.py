# Fenetre principale de l'app 
#affiche le menu principal de donne accès aux fonctionnalites 



import tkinter as tk  
from tkinter import ttk 

class MainWindow : 
    """ Fenetre principal de DeskManger."""
    
    def __init__(self,db):
        #recupération de la base de donnée passé par main.py
        self.db = db

        #creation de la fenetre principal 
        self.root = tk.Tk()
        self.root.title("DeskManger - Gestion de matériel")
        self.root.geometry("400x300")
        self.root.resizable(True, True)

        #construction de l interface 
        self._build_ui()

    
    def _build_ui(self):
        """Construit les éléments visuels de la fenêtre."""
                # Titre
        tk.Label(
            self.root,
            text="DeskManager",
            font=("Helvetica", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="Gestion de matériel informatique",
            font=("Helvetica", 10)
        ).pack()

        # Boutons
        tk.Button(
            self.root,
            text="👤 Gérer les employés",
            width=30,
            command=self.ouvrir_employes
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="💻 Gérer le matériel",
            width=30,
            command=self.ouvrir_materiels
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="📋 Gérer les attributions",
            width=30,
            command=self.ouvrir_attributions
        ).pack(pady=5)

    def ouvrir_employes (self):
        """ouvre la fenetre de gestion des employés."""
        from ui.employe_ui import EmployeUI
        EmployeUI(self.root, self.db)

    def ouvrir_materiels(self):
        """Ouvre la fenêtre de gestion du matériel."""
        from ui.materiel_ui import MaterielUI
        MaterielUI(self.root, self.db)

    def ouvrir_attributions(self):
        """Ouvre la fenêtre de gestion des attributions."""
        from ui.attribution_ui import AttributionUI
        AttributionUI(self.root, self.db)

    def lancer(self):
        """Lance la boucle principale Tkinter."""
        self.root.mainloop()
