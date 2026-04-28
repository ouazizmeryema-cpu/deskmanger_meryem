# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox

class EmployeUI:
    """Fenêtre de gestion des employés."""

    def __init__(self, parent, db):
        self.db = db

        # Création de la fenêtre
        self.fenetre = tk.Toplevel(parent)
        self.fenetre.title("Gestion des employés")  # ❌ titke → title
        self.fenetre.geometry("600x400")

        # Construction de l'interface
        self._build_ui()
        self._charger_employes()

    def _build_ui(self):
        """Construit les éléments visuels."""

        # Formulaire
        frame_form = tk.LabelFrame(self.fenetre, text="Employé", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_form, text="Nom :").grid(row=0, column=0, sticky="w")
        self.entry_nom = tk.Entry(frame_form, width=30)
        self.entry_nom.grid(row=0, column=1, padx=5, pady=3)

        tk.Label(frame_form, text="Prénom :").grid(row=1, column=0, sticky="w")
        self.entry_prenom = tk.Entry(frame_form, width=30)
        self.entry_prenom.grid(row=1, column=1, padx=5, pady=3)

        tk.Label(frame_form, text="Service :").grid(row=2, column=0, sticky="w")
        self.entry_service = tk.Entry(frame_form, width=30)
        self.entry_service.grid(row=2, column=1, padx=5, pady=3)

        # Boutons
        frame_boutons = tk.Frame(self.fenetre)
        frame_boutons.pack(pady=5)

        tk.Button(frame_boutons, text="➕ Ajouter",   width=15, command=self._ajouter).pack(side="left", padx=5)
        tk.Button(frame_boutons, text="✏️ Modifier",  width=15, command=self._modifier).pack(side="left", padx=5)
        tk.Button(frame_boutons, text="🗑️ Supprimer", width=15, command=self._supprimer).pack(side="left", padx=5)

        # Tableau
        frame_tableau = tk.Frame(self.fenetre)
        frame_tableau.pack(fill="both", expand=True, padx=10, pady=5)

        colonnes = ("id", "nom", "prenom", "service")
        self.tableau = ttk.Treeview(frame_tableau, columns=colonnes, show="headings")

        self.tableau.heading("id",      text="ID")
        self.tableau.heading("nom",     text="Nom")
        self.tableau.heading("prenom",  text="Prénom")
        self.tableau.heading("service", text="Service")

        self.tableau.column("id",      width=40)
        self.tableau.column("nom",     width=150)
        self.tableau.column("prenom",  width=150)
        self.tableau.column("service", width=150)

        self.tableau.pack(fill="both", expand=True)
        self.tableau.bind("<<TreeviewSelect>>", self._selectionner)

    # ❌ ces méthodes étaient à l'intérieur de _build_ui → à mettre dehors !

    def _charger_employes(self):
        """Charge et affiche tous les employés."""
        for row in self.tableau.get_children():
            self.tableau.delete(row)
        for emp in self.db.get_all_employes():
            self.tableau.insert("", "end", values=(emp["id"], emp["nom"], emp["prenom"], emp["service"]))

    def _selectionner(self, event):
        """Remplit le formulaire avec l'employé sélectionné."""
        selection = self.tableau.selection()
        if selection:
            valeurs = self.tableau.item(selection[0])["values"]
            self.selected_id = valeurs[0]
            self.entry_nom.delete(0, tk.END)
            self.entry_nom.insert(0, valeurs[1])
            self.entry_prenom.delete(0, tk.END)
            self.entry_prenom.insert(0, valeurs[2])
            self.entry_service.delete(0, tk.END)
            self.entry_service.insert(0, valeurs[3])

    def _ajouter(self):
        """Ajoute un nouvel employé."""
        nom     = self.entry_nom.get().strip()
        prenom  = self.entry_prenom.get().strip()
        service = self.entry_service.get().strip()

        if not nom or not prenom or not service:
            messagebox.showwarning("Attention", "Tous les champs sont obligatoires !")
            return

        self.db.ajouter_employe(nom, prenom, service)
        self._charger_employes()
        self._vider_formulaire()
        messagebox.showinfo("Succès", "Employé ajouté avec succès !")

    def _modifier(self):
        """Modifie l'employé sélectionné."""
        if not hasattr(self, "selected_id"):
            messagebox.showwarning("Attention", "Sélectionnez un employé !")
            return

        nom     = self.entry_nom.get().strip()
        prenom  = self.entry_prenom.get().strip()
        service = self.entry_service.get().strip()

        self.db.modifier_employe(self.selected_id, nom, prenom, service)
        self._charger_employes()
        self._vider_formulaire()
        messagebox.showinfo("Succès", "Employé modifié avec succès !")

    def _supprimer(self):
        """Supprime l'employé sélectionné."""
        if not hasattr(self, "selected_id"):
            messagebox.showwarning("Attention", "Sélectionnez un employé !")
            return

        self.db.supprimer_employe(self.selected_id)
        self._charger_employes()
        self._vider_formulaire()
        messagebox.showinfo("Succès", "Employé supprimé avec succès !")

    def _vider_formulaire(self):
        """Vide les champs du formulaire."""
        self.entry_nom.delete(0, tk.END)      # ❌ entry_nom_delete → entry_nom.delete
        self.entry_prenom.delete(0, tk.END)
        self.entry_service.delete(0, tk.END)
        if hasattr(self, "selected_id"):
            del self.selected_id