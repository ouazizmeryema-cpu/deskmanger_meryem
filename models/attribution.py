# attribution.py – Modèle d'une attribution
# Représente le lien entre un employé et un matériel


class Attribution : 

 def __init__(self,id : int, employe,materiel, date_attribution:str):
    self.id = id
    self.employe = employe 
    self.materiel = materiel
    self.date_attribution = date_attribution 

 def __str__(self) -> str:
    return (
        f"attribution #{self.id}|"
        f"{self.employe.get_nom_complet()}|"
        f"{self.materiel.get_designation()}|"
        f"Date: {self.date_attribution}"


    )

 def __repr__(self)-> str : 
    return (
        #r affiche les guillemets pour les str exp="toto"
        f"Attribution("
        f"id={self.id!r}, "
        f"employe={self.employe!r}, "    # !r pour voir exactement le type de la valeur
        f"materiel={self.materiel!r}, " 
        f"date_attribution={self.date_attribution!r})"

    )
    

