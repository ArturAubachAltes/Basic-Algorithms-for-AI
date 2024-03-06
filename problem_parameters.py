from typing import List

class ProblemParameters(object):
    def __init__(self, f_max: int, est_max: List[int], bic_tot: int,semilla,TIPOS_operador:int, params:bool):
        self.f_max=f_max
        self.est_max=est_max
        self.bic_tot=bic_tot
        self.semilla=semilla
        self.TIPOS_operador = TIPOS_operador #1,2,3
        self.params=params
    def __repr__(self):
        return f"Params(F_max={self.f_max}, Nombre_estacions={self.est_max},semilla={self.semilla})"
    
