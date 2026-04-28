# -*- coding: utf-8 -*-
# ============================================================
# materiel_ui.py – Interface de gestion du matériel
# Permet d'ajouter, modifier, supprimer et afficher le matériel
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox

class MaterielUI:
    """Fenêtre de gestion du matériel."""

    def __init__(self, parent, db):
        self.db = db

        # Création de la fenêtre
        self.fenetre = tk.Toplevel(parent)
        self.fenetre.title("Gestion du matériel")
        self.fenetre.geometry("700x400")

        # Construction de l'interface
        self._build_ui()
        self._charger_materiels()

    def _build_ui(self):
        """Construit les éléments visuels."""

        # ── Formulaire ──────────────────────────────
        frame_form = tk.LabelFrame(self.fenetre, text="Matériel", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=10)

        # Type
        tk.Label(frame_form, text="Type :").grid(row=0, column=0, sticky="w")
        self.combo_type = ttk.Combobox(frame_form, width=28, state="readonly")
        self.combo_type["values"] = [
            "Ordinateur portable",
            "Écran",
            "Téléphone professionnel",
            "Accessoire informatique"
        ]
        self.combo_type.grid(row=0, column=1, padx=5, pady=3)

        # Marque
        tk.Label(frame_form, text="Marque :").grid(row=1, column=0, sticky="w")
        self.entry_marque = tk.Entry(frame_form, width=30)
        self.entry_marque.grid(row=1, column=1, padx=5, pady=3)

        # Modèle
        tk.Label(frame_form, text="Modèle :").grid(row=2, column=0, sticky="w")
        self.entry_modele = tk.Entry(frame_form, width=30)
        self.entry_modele.grid(row=2, column=1, padx=5, pady=3)

        # Numéro de série
        tk.Label(frame_form, text="N° de série :").grid(row=3, column=0, sticky="w")
        self.entry_numero_serie = tk.Entry(frame_form, width=30)
        self.entry_numero_serie.grid(row=3, column=1, padx=5, pady=3)

        # ── Boutons ──────────────────────────────────
        frame_boutons = tk.Frame(self.fenetre)
        frame_boutons.pack(pady=5)

        tk.Button(frame_boutons, text="➕ Ajouter",   width=15, command=self._ajouter).pack(side="left", padx=5)
        tk.Button(frame_boutons, text="✏️ Modifier",  width=15, command=self._modifier).pack(side="left", padx=5)
        tk.Button(frame_boutons, text="🗑️ Supprimer", width=15, command=self._supprimer).pack(side="left", padx=5)

        # ── Tableau ──────────────────────────────────
        frame_tableau = tk.Frame(self.fenetre)
        frame_tableau.pack(fill="both", expand=True, padx=10, pady=5)

        colonnes = ("id", "type", "marque", "modele", "numero_serie")
        self.tableau = ttk.Treeview(frame_tableau, columns=colonnes, show="headings")

        self.tableau.heading("id",           text="ID")
        self.tableau.heading("type",         text="Type")
        self.tableau.heading("marque",       text="Marque")
        self.tableau.heading("modele",       text="Modèle")
        self.tableau.heading("numero_serie", text="N° de série")

        self.tableau.column("id",           width=40)
        self.tableau.column("type",         width=150)
        self.tableau.column("marque",       width=100)
        self.tableau.column("modele",       width=100)
        self.tableau.column("numero_serie", width=120)

        self.tableau.pack(fill="both", expand=True)

        # Clic sur une ligne → remplit le formulaire
        self.tableau.bind("<<TreeviewSelect>>", self._selectionner)

    def _charger_materiels(self):
        """Charge et affiche tous les matériels dans le tableau."""
        for row in self.tableau.get_children():
            self.tableau.delete(row)

        for mat in self.db.get_all_materiels():
            self.tableau.insert("", "end", values=(
                mat["id"], mat["type"], mat["marque"],
                mat["modele"], mat["numero_serie"]
            ))

    def _selectionner(self, event):
        """Remplit le formulaire avec le matériel sélectionné."""
        selection = self.tableau.selection()
        if selection:
            valeurs = self.tableau.item(selection[0])["values"]
            self.selected_id = valeurs[0]
            self.combo_type.set(valeurs[1])
            self.entry_marque.delete(0, tk.END)
            self.entry_marque.insert(0, valeurs[2])
            self.entry_modele.delete(0, tk.END)
            self.entry_modele.insert(0, valeurs[3])
            self.entry_numero_serie.delete(0, tk.END)
            self.entry_numero_serie.insert(0, valeurs[4])

    def _ajouter(self):
        """Ajoute un nouveau matériel."""
        type_mat     = self.combo_type.get()
        marque       = self.entry_marque.get().strip()
        modele       = self.entry_modele.get().strip()
        numero_serie = self.entry_numero_serie.get().strip()

        if not type_mat or not marque or not modele or not numero_serie:
            messagebox.showwarning("Attention", "Tous les champs sont obligatoires !")
            return

        self.db.ajouter_materiel(type_mat, marque, modele, numero_serie)
        self._charger_materiels()
        self._vider_formulaire()
        messagebox.showinfo("Succès", "Matériel ajouté avec succès !")

    def _modifier(self):
        """Modifie le matériel sélectionné."""
        if not hasattr(self, "selected_id"):
            messagebox.showwarning("Attention", "Sélectionnez un matériel !")
            return

        type_mat     = self.combo_type.get()
        marque       = self.entry_marque.get().strip()
        modele       = self.entry_modele.get().strip()
        numero_serie = self.entry_numero_serie.get().strip()

        self.db.modifier_materiel(self.selected_id, type_mat, marque, modele, numero_serie)
        self._charger_materiels()
        self._vider_formulaire()
        messagebox.showinfo("Succès", "Matériel modifié avec succès !")

    def _supprimer(self):
        """Supprime le matériel sélectionné."""
        if not hasattr(self, "selected_id"):
            messagebox.showwarning("Attention", "Sélectionnez un matériel !")
            return

        self.db.supprimer_materiel(self.selected_id)
        self._charger_materiels()
        self._vider_formulaire()
        messagebox.showinfo("Succès", "Matériel supprimé avec succès !")

    def _vider_formulaire(self):
        """Vide les champs du formulaire."""
        self.combo_type.set("")
        self.entry_marque.delete(0, tk.END)
        self.entry_modele.delete(0, tk.END)
        self.entry_numero_serie.delete(0, tk.END)
        if hasattr(self, "selected_id"):
            del self.selected_id