class Employe : 
    def __init__(self , id:int, nom:str, prenom:str, service:str):
        self.id=id 
        self.nom=nom 
        self.prenom=prenom 
        self.service=service 

        
    def get_nom_complet (self)->str:
        return f"{self.prenom} {self.nom.upper}"

    def __str__(self):
        return(
            f"Employé #{self.id}|"
            f"{self.get_nom_complet()}|"
            f"service:{self.service}"

        )
    
    def __repr__(self) -> str:
        return (
            f"Employe(id={self.id!r}, nom={self.nom!r}, "  
            f"prenom={self.prenom!r}, service={self.service!r})"
        )
        
    

