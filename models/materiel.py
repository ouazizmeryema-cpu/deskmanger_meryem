class Materiel : 
    TYPE_VALIDES=[
        "Ordinateur portable",
        "Écran",
        "Téléphone professionnel",
        "Accessoire informatique",]

    def __init__(self, id:int, type:str, marque:str, modele:str, numero_serie:str):
        self.id=id
        self.type=type
        self.marque=marque
        self.modele=modele 
        self.numero_serie=numero_serie
        

    def get_designation(self)->str:
        return f"{self.marque} {self.type} {self.modele}"

    def __str__(self)->str:
        return (f"Matériel #{self.id}|"
                f"{self.get_designation}|"
                f"N/S : {self.mumero.derie}"
                )
    

    def __repr__(self):
        return(
            f"Materiel(id={self.id!r}, type={self.type!r},)"
            f"marque={self.marque!r}, modele={self.model!r},"
            f"numero_serie={self.numero_serie!r}"
        )
        