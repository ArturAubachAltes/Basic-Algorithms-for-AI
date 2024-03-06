class furgo_operators(object):
	pass


class crea_furgo(furgo_operators):
    """
    Crear furgo
    """
    def __init__(self,origin,bikes1,dest1,bikes2=0,dest2=None) -> None:
        self.origin=origin
        self.dest1=dest1
        self.bikes1=bikes1


class asignar_dest2(furgo_operators):
    """
    Crear furgo
    """
    def __init__(self,furgo,bikes2,dest2) -> None:
        self.furgo=furgo
        self.dest2=dest2
        self.bikes2=bikes2

class borrar_furgo(furgo_operators):
    """
    Borrar furgo
    """
    def __init__(self,furgo):
        self.furgo=furgo

#Aquí ya damos por hecho que estan todas las furgos asignadas y vamos cambiandolas de sitio
class furgo_move_origin(furgo_operators):
    """
    Modifica el origen
    """
    def __init__(self,furgo,originnew):
        self.furgo = furgo
        self.originnew = originnew #estacion inicial que es una clase

#para calculo, en la futura clase state_representation podemos tener un método que lo calcule
class furgo_move_dest(furgo_operators):
    """
    """
    def __init__(self,furgo,destnew):
        self.furgo=furgo
        self.destnew = destnew        
#de la manera imprementada podemos convertirlo en un operador, pero bueno no cambiaría demasiado


class incrementar_num_bici(furgo_operators):
    def __init__(self,furgo,bibic_nou1,dest2=False):
        self.furgo = furgo
        self.bibic_nou1 = bibic_nou1
        self.dest2 = dest2


class reduir_num_bici(furgo_operators):
    def __init__(self,furgo,bibic_nou1,dest2=False):
        self.furgo = furgo
        self.bibic_nou1 = bibic_nou1
        self.dest2 = dest2





