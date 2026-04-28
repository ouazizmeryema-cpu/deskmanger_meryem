#base de donnée

import sqlite3

class DatabaseManager:

    def __init__(self,db_path : str ="data/deskmanger.db"):
        self.db_path= db_path 
        self.connexion = sqlite3.connect(self.db_path)
        self.connexion.row_factory = sqlite3.Row
        self.curseur = self.connexion.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.curseur.executescript("""
            CREATE TABLE IF NOT EXISTS employes (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                nom     TEXT    NOT NULL,
                prenom  TEXT    NOT NULL,
                service TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS materiels (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                type         TEXT    NOT NULL,
                marque       TEXT    NOT NULL,
                modele       TEXT    NOT NULL,
                numero_serie TEXT    NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS attributions (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                employe_id       INTEGER NOT NULL,
                materiel_id      INTEGER NOT NULL,
                date_attribution TEXT    NOT NULL,
                FOREIGN KEY (employe_id)  REFERENCES employes(id),
                FOREIGN KEY (materiel_id) REFERENCES materiels(id)
            );
        """)
        self.connexion.commit()

        #méthode CRU : create , read , update

        #______employé_______

    def ajouter_employe(self, nom:str, prenom:str ,service:str) ->int:
        """Ajouter un nouvel employe a la base donnée"""
        self.curseur.execute(
            "INSERT INTO employes (nom, prenom ,service) VALUES(?,?,?)",(nom, prenom, service)
        )
        self.connexion.commit()
        return self.curseur.lastrowid
    
    def modifier_employe(self,id:int, nom:str, prenom:str, service:str):
         """Modifier un employe"""
         self.curseur.execute(
             "UPDATE employes SET nom=?, prenom=?, service=? WHERE id=?",
             (nom, prenom, service, id)
        
        )
         self.connexion.commit()


    def supprimer_employe(self, id:int ) ->None:
        """Supprimer un employe"""
        self.curseur.execute("DELETE FROM attributions WHERE employe_id=?", (id,))
        self.curseur.execute("DELETE FROM employes WHERE id=?",(id,))
        self.connexion.commit()

    

    def get_all_employes(self) ->list: 
        self.curseur.execute("SELECT * FROM employes ORDER BY nom, prenom")
        return self.curseur.fetchall()
    
    #______materiel_____
    
    def ajouter_materiel(self, type: str , marque: str, modele: str, numero_serie: str) ->int:
        """ajouter un nouveau materiel"""
        self.curseur.execute(
            "INSERT INTO materiels (type , marque, modele, numero_serie) VALUES(?,?,?,?)",(type, marque, modele, numero_serie)
        )
        self.connexion.commit()
        # récupère l'id généré automatiquement par SQLite après l'insertion
        return self.curseur.lastrowid
    
    def modifier_materiel(self, id: int, type: str, marque: str, modele: str, numero_serie: str) -> None:
        """Modifie un matériel existant."""
        self.curseur.execute(
            "UPDATE materiels SET type=?, marque=?, modele=?, numero_serie=? WHERE id=?",
        (type, marque, modele, numero_serie, id)
        )
        self.connexion.commit()

    def supprimer_materiel(self, id: int) ->None:
        """Supprime un matériel et ses attributions"""
        self.curseur.execute("DELETE FROM attributions WHERE materiel_id=?", (id,))
        self.curseur.execute("DELETE FROM materiels WHERE id=?",(id,))
        self.connexion.commit()

    def get_all_materiels(self) ->list:
        """Retourne tous les matériels"""
        self.curseur.execute("SELECT * FROM materiels ORDER BY type, marque")
        return self.curseur.fetchall()
  
    
    def get_materiels_disponibles(self) ->list:
        """retourne les materiels non attribués"""
        self.curseur.execute("""
            SELECT * FROM materiels
            WHERE id NOT IN(SELECT materiel_id FROM attributions)
            ORDER BY type,marque
            
        """)
        return self.curseur.fetchall()
    

    #________attributions________


    def ajouter_attribution(self, employe_id: int, materiel_id: int, date_attribution: str)-> int:
        """Attribue un matériel à un employé."""
        self.curseur.execute(
            "INSERT INTO attributions (employe_id, materiel_id, date_attribution) VALUES(?,?,?)",
            (employe_id, materiel_id, date_attribution) 
        )
        self.connexion.commit()
        return self.curseur.lastrowid

    def get_all_attributions(self,)->list:
        """ retourn tous les attribution"""
        self.curseur.execute( """
            SELECT
            a.id,
            e.nom || ' ' || e.prenom AS employe,
            m.marque || ' ' || m.modele AS materiel,
            a.date_attribution
        FROM attributions a
        JOIN employes  e ON a.employe_id  = e.id
        JOIN materiels m ON a.materiel_id = m.id
        ORDER BY a.date_attribution DESC
    """

        )

        return self.curseur.fetchall()

    def supprimer_attribution(self, id:int) ->None:
        """Supprimer une attribution"""
        self.curseur.execute("DELETE FROM attributions WHERE id=?",(id,))
        self.connexion.commit()
    
    
    def fermer(self) -> None:
        """Fermer la connexion à la base de donnée"""
        self.connexion.close()

                             
        
    
    