
# -*- coding: utf-8 -*-
# ============================================================
# attribution_ui.py – Interface de gestion des attributions
# Permet d'attribuer un matériel à un employé
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class AttributionUI:
    """Fenêtre de gestion des attributions."""

    def __init__(self, parent, db):
        self.db = db

        # Création de la fenêtre
        self.fenetre = tk.Toplevel(parent)
        self.fenetre.title("Gestion des attributions")
        self.fenetre.geometry("700x400")

        # Construction de l'interface
        self._build_ui()
        self._charger_attributions()

    def _build_ui(self):
        """Construit les éléments visuels."""

        # ── Formulaire ──────────────────────────────
        frame_form = tk.LabelFrame(self.fenetre, text="Attribution", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=10)

        # Employé
        tk.Label(frame_form, text="Employé :").grid(row=0, column=0, sticky="w")
        self.combo_employe = ttk.Combobox(frame_form, width=28, state="readonly")
        self.combo_employe.grid(row=0, column=1, padx=5, pady=3)

        # Matériel
        tk.Label(frame_form, text="Matériel :").grid(row=1, column=0, sticky="w")
        self.combo_materiel = ttk.Combobox(frame_form, width=28, state="readonly")
        self.combo_materiel.grid(row=1, column=1, padx=5, pady=3)

        # Date
        tk.Label(frame_form, text="Date :").grid(row=2, column=0, sticky="w")
        self.entry_date = tk.Entry(frame_form, width=30)
        self.entry_date.insert(0, date.today().strftime("%d/%m/%Y"))  # date du jour par défaut
        self.entry_date.grid(row=2, column=1, padx=5, pady=3)

        # Bouton charger les listes
        tk.Button(
            frame_form,
            text="🔄 Actualiser les listes",
            command=self._charger_listes
        ).grid(row=3, column=1, sticky="w", padx=5, pady=3)

        # ── Boutons ──────────────────────────────────
        frame_boutons = tk.Frame(self.fenetre)
        frame_boutons.pack(pady=5)

        tk.Button(frame_boutons, text="➕ Attribuer",  width=15, command=self._attribuer).pack(side="left", padx=5)
        tk.Button(frame_boutons, text="🗑️ Supprimer",  width=15, command=self._supprimer).pack(side="left", padx=5)

        # ── Tableau ──────────────────────────────────
        frame_tableau = tk.Frame(self.fenetre)
        frame_tableau.pack(fill="both", expand=True, padx=10, pady=5)

        colonnes = ("id", "employe", "materiel", "date_attribution")
        self.tableau = ttk.Treeview(frame_tableau, columns=colonnes, show="headings")

        self.tableau.heading("id",               text="ID")
        self.tableau.heading("employe",          text="Employé")
        self.tableau.heading("materiel",         text="Matériel")
        self.tableau.heading("date_attribution", text="Date")

        self.tableau.column("id",               width=40)
        self.tableau.column("employe",          width=180)
        self.tableau.column("materiel",         width=200)
        self.tableau.column("date_attribution", width=100)

        self.tableau.pack(fill="both", expand=True)

        # Clic sur une ligne → sélectionne
        self.tableau.bind("<<TreeviewSelect>>", self._selectionner)

        # Charger les listes au démarrage
        self._charger_listes()

    def _charger_listes(self):
        """Charge les employés et matériels disponibles dans les listes déroulantes."""
        # Employés
        self.employes = self.db.get_all_employes()
        self.combo_employe["values"] = [
            f"{e['id']} - {e['nom']} {e['prenom']}" for e in self.employes
        ]

        # Matériels disponibles (non attribués)
        self.materiels = self.db.get_materiels_disponibles()
        self.combo_materiel["values"] = [
            f"{m['id']} - {m['marque']} {m['modele']}" for m in self.materiels
        ]

    def _charger_attributions(self):
        """Charge et affiche toutes les attributions dans le tableau."""
        for row in self.tableau.get_children():
            self.tableau.delete(row)

        for attr in self.db.get_all_attributions():
            self.tableau.insert("", "end", values=(
                attr["id"], attr["employe"],
                attr["materiel"], attr["date_attribution"]
            ))

    def _selectionner(self, event):
        """Sélectionne une attribution."""
        selection = self.tableau.selection()
        if selection:
            valeurs = self.tableau.item(selection[0])["values"]
            self.selected_id = valeurs[0]

    def _attribuer(self):
        """Attribue un matériel à un employé."""
        employe_sel  = self.combo_employe.get()
        materiel_sel = self.combo_materiel.get()
        date_attr    = self.entry_date.get().strip()

        if not employe_sel or not materiel_sel or not date_attr:
            messagebox.showwarning("Attention", "Tous les champs sont obligatoires !")
            return

        # Récupérer les ids depuis la sélection "1 - Dupont Jean"
        employe_id  = int(employe_sel.split(" - ")[0])
        materiel_id = int(materiel_sel.split(" - ")[0])

        self.db.ajouter_attribution(employe_id, materiel_id, date_attr)
        self._charger_attributions()
        self._charger_listes()
        messagebox.showinfo("Succès", "Matériel attribué avec succès !")

    def _supprimer(self):
        """Supprime une attribution."""
        if not hasattr(self, "selected_id"):
            messagebox.showwarning("Attention", "Sélectionnez une attribution !")
            return

        self.db.supprimer_attribution(self.selected_id)
        self._charger_attributions()
        self._charger_listes()
        messagebox.showinfo("Succès", "Attribution supprimée avec succès !")