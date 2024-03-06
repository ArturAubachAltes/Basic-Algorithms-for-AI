from __future__ import annotations
from abia_bicing import furgonetas
from operators import crea_furgo,asignar_dest2,borrar_furgo,furgo_move_origin,furgo_move_dest,incrementar_num_bici,reduir_num_bici
from typing import List, Set, Generator
import random
from problem_parameters import ProblemParameters
import copy

class StateRepresentation(object):
    """
    Doy por hecho de que tenemos dos listas, una de est y otra de furgos pero creo que podríamos hacer una
    lista de tuplas, con una estación y furgo si hay o None si no hay o algo así(haciendo esto, sin embargo,
    estaríamos obligados a mantener la cuenta de furgos asignadas/creadas de alguna manera(un contador externo en una clase 
    por ejemplo)).
    """
    def __init__(self, params: ProblemParameters, list_est,list_furgos):
        """
        list_est una lista de instancias de estacio y list_furgos una lista de instancias de furgo
        """
        self.params = params
        self.list_est = list_est
        self.list_furgos=list_furgos
        #Si hacemos la inicialización puede ser que hagamos que se pnga como zero después de calcularlo

    def e_copy(self) -> StateRepresentation:
        """
        El copy original el que feia era a més fer deep copies dels sets de la llista de contenidors,
        ara com només tenim instàncies a dins no cal.
        Si anessim a utilitzar una única llista amb tuples, però, potser si que hauriem de utilitzar-ne el copy:
        list_est_copy = [set_i.copy() for set_i in self.list_est]
        list_furgo_copy = [set_i.copy() for set_i in self.list_furgos]
        """
        # Afegim el copy per cada set!
        list_furgo_copy = [copy.deepcopy(instancia) for instancia in self.list_furgos]
        #list_estaciones=[copy.deepcopy(estaciones) for estaciones in self.list_est]
        return StateRepresentation(self.params, self.list_est,list_furgo_copy)

    def __repr__(self):
        return f"Trasllats:{([str(i) for i in self.list_furgos])}, beneficio_total: {self.beneficio_total}"


    # Utilitzarem aquesta funció auxiliar per trobar el contenidor
    # que conté un paquet determinat


    def to_list(self):
        return ["self.num_steps", self.beneficio_total]


    def generate_actions(self):
        """
        També hem de fer un generador d'un únic estat
        Aquí haurem de mirar si ens queden per assignar furgos mirant la quantitat que tenim assignada i
        la quantitat total(als parametres del problema) y després un loop per mirar si movem l'estació d'origen
        d'una furgo a un  millor origen i un altra loop que miri si en movem els/el destí a un de millor
        """


        # Crear furgonetas si aún no se han asignado todas
        if len(self.list_furgos) <= self.params.f_max:  # Verifica si el número de furgonetas existentes es menor o igual al máximo permitido
            for est_origen in self.list_est:  # Itera sobre todas las estaciones de origen posibles
                if not est_origen.hayfurgos:  
                    for est_dest in self.list_est:  # Itera sobre todas las estaciones de destino posibles
                        if est_origen != est_dest:  # Asegura que la estación de destino no es la misma que la de origen
                            if self.params.TIPOS_operador ==1:
                                yield crea_furgo(est_origen, 1, est_dest)  # Crea una nueva furgoneta con la estación de origen y destino especificadas
                            else:
                                for i in range(1, 31):
                                    yield crea_furgo(est_origen, i, est_dest)

                                
        if len(self.list_furgos)>0:
            # Operaciones con furgonetas existentes
            for furgo in self.list_furgos:
                # Borrar furgoneta
                yield borrar_furgo(furgo)

                # Mover origen de la furgoneta
                for origen_new in self.list_est:
                    if  not origen_new.hayfurgos and furgo.origen != origen_new and origen_new != furgo.dest1: #si en el origen no hay una furgo y no es el mismo origen de antes
                        if furgo.dest2:
                            if origen_new != furgo.dest2:
                                yield furgo_move_origin(furgo, origen_new)
                        else:
                            yield furgo_move_origin(furgo, origen_new)

                # Mover destino de la furgoneta
                for dest_new in self.list_est:
                    if furgo.dest1 != dest_new and furgo.origen != dest_new:
                        if furgo.dest2:
                            if furgo.dest2 != dest_new:
                                yield furgo_move_dest(furgo, dest_new)

                        else:
                            yield furgo_move_dest(furgo, dest_new)

                # Incrementar parada si la furgoneta aún no tiene una segunda parada
                if furgo.dest2 is None:
                    for dest2 in self.list_est:
                        if dest2 != furgo.origen and dest2 != furgo.dest1 and furgo.total_bicis() < 30:#esto también me permitiría mover la segunda parada
                            yield asignar_dest2(furgo, 1, dest2)                  
                else:
                    for dest2 in self.list_est:
                        if dest2 != furgo.origen and dest2 != furgo.dest1 and dest2 != furgo.dest2:
                            yield asignar_dest2(furgo, furgo.cant_bicis2, dest2)

                    # Incrementar número de bicicletas
                    if self.params.TIPOS_operador !=3:
                        if furgo.total_bicis() < 30:
                            if furgo.dest2:
                                yield incrementar_num_bici(furgo, furgo.cant_bicis2 + 1,True) #incremento las bicis en uno

                            yield incrementar_num_bici(furgo, furgo.cant_bicis1 + 1) #incremento las bicis en uno


                        # Reducir número de bicicletas
                        if furgo.cant_bicis1 > 1: #reduzco las bicis
                            if furgo.dest2:
                                yield reduir_num_bici(furgo, furgo.cant_bicis2 - 1,True) #incremento las bicis en uno

                            yield reduir_num_bici(furgo, furgo.cant_bicis1 - 1) #incremento las bicis en uno       
    
    
    def generate_one_action(self):
        # Crear listas para almacenar posibles acciones
        lista_crear_furgo = []
        lista_asignar_dest2 = []
        lista_borrar_furgo = []
        lista_furgo_move_origin = []
        lista_furgo_move_dest = []
        lista_incrementar_num_bici = []
        lista_reduir_num_bici = []

        # Crear furgonetas si aún no se han asignado todas
        if len(self.list_furgos) <= self.params.f_max:  # Verifica si el número de furgonetas existentes es menor o igual al máximo permitido
            for est_origen in self.list_est:  # Itera sobre todas las estaciones de origen posibles
                if not est_origen.hayfurgos:  
                    for est_dest in self.list_est:  # Itera sobre todas las estaciones de destino posibles
                        if est_origen != est_dest:  # Asegura que la estación de destino no es la misma que la de origen
                            lista_crear_furgo.append((est_origen, 1, est_dest))  # Crea una nueva furgoneta con la estación de origen y destino especificadas

        if len(self.list_furgos)>0:
            # Operaciones con furgonetas existentes
            for furgo in self.list_furgos:
                # Borrar furgoneta
                lista_borrar_furgo.append(furgo)

                # Mover origen de la furgoneta
                for origen_new in self.list_est:
                    if  not origen_new.hayfurgos and furgo.origen != origen_new and origen_new != furgo.dest1: #si en el origen no hay una furgo y no es el mismo origen de antes
                        if furgo.dest2:
                            if origen_new != furgo.dest2:
                                lista_furgo_move_origin.append((furgo, origen_new))

                        else:
                            lista_furgo_move_origin.append((furgo, origen_new))

                # Mover destino de la furgoneta
                for dest_new in self.list_est:
                    if furgo.dest1 != dest_new and furgo.origen != dest_new:
                        if furgo.dest2:
                            if furgo.dest2 != dest_new:
                                lista_furgo_move_dest.append((furgo, dest_new))

                        else:
                            lista_furgo_move_dest.append((furgo, dest_new))

                # Incrementar parada si la furgoneta aún no tiene una segunda parada
                if furgo.dest2 is None:
                    for dest2 in self.list_est:
                        if dest2 != furgo.origen and dest2 != furgo.dest1 and furgo.total_bicis() < 30:#esto también me permitiría mover la segunda parada
                            lista_asignar_dest2.append((furgo, 1, dest2))
              
                else:
                    for dest2 in self.list_est:
                        if dest2 != furgo.origen and dest2 != furgo.dest1 and dest2 != furgo.dest2:
                            lista_asignar_dest2.append((furgo, furgo.cant_bicis2, dest2))

                    # Incrementar número de bicicletas
                    if furgo.total_bicis() < 30:
                        if furgo.dest2:
                            lista_incrementar_num_bici.append((furgo, furgo.cant_bicis1 + 1,True)) #incremento las bicis en uno

                        lista_incrementar_num_bici.append((furgo, furgo.cant_bicis1 + 1,False)) #incremento las bicis en uno


                    # Reducir número de bicicletas
                    if furgo.cant_bicis1 > 1: #reduzco las bicis
                        if furgo.dest2:
                            lista_reduir_num_bici.append((furgo, furgo.cant_bicis1 - 1,True)) #incremento las bicis en uno

                        lista_reduir_num_bici.append((furgo, furgo.cant_bicis1 - 1,False)) #incremento las bicis en uno

        # Calcular las longitudes de las listas de acciones
        n = len(lista_crear_furgo)
        m = len(lista_borrar_furgo)
        o = len(lista_furgo_move_origin)
        p = len(lista_furgo_move_dest)
        q = len(lista_asignar_dest2)
        r = len(lista_incrementar_num_bici)
        s = len(lista_reduir_num_bici)

        # Seleccionar una acción aleatoria basada en las proporciones de las acciones disponibles
        random_value = random.random()
        total_sum = n + m + o + p + q + r + s
        if random_value < (n / total_sum):
            combination = random.choice(lista_crear_furgo)
            yield crea_furgo(combination[0],combination[1],combination[2])#¿Qué es esto?
        elif random_value < ((n + m) / total_sum):
            furgo = random.choice(lista_borrar_furgo)
            yield borrar_furgo(furgo)
        elif random_value < ((n + m + o) / total_sum):
            combination = random.choice(lista_furgo_move_origin)
            yield furgo_move_origin(combination[0],combination[1])
        elif random_value < ((n + m + o + p) / total_sum):
            combination = random.choice(lista_furgo_move_dest)
            yield furgo_move_dest(combination[0],combination[1])
        elif random_value < ((n + m + o + p + q) / total_sum):
            combination = random.choice(lista_asignar_dest2)
            yield asignar_dest2(combination[0],combination[1],combination[2])
        elif random_value < ((n + m + o + p + q + r) / total_sum):
            combination = random.choice(lista_incrementar_num_bici)
            yield incrementar_num_bici(combination[0],combination[1],combination[2])
        else:
            combination = random.choice(lista_reduir_num_bici)
            yield reduir_num_bici(combination[0],combination[1],combination[2])        

    def findfurgo(self,new_lista_furgo,inst_furgo):
        for i in new_lista_furgo: #Busco en el nuevo estado la furgo correspondiente
            if i == inst_furgo:   
                return i         
    def apply_action(self, action) -> StateRepresentation:
        """
        Apliquem l'acció, no deu ser molt dificil
        """
        new_lista_furgo = self.e_copy()
        #new_lista_furgo.num_steps += 1


        if isinstance(action, crea_furgo):
            origin = action.origin
            dest1 = action.dest1
            bikes1 = action.bikes1
            furg = furgonetas(origin, dest1, bikes1)
            new_lista_furgo.list_furgos.append(furg)
            dest1.bicicletas_trasladadas += bikes1
            furg.origen.hayfurgos = True  # Marcar que la nueva estación origen tiene furgo

        elif isinstance(action, borrar_furgo):
            action.furgo.dest1.bicicletas_trasladadas -= action.furgo.cant_bicis1
            if action.furgo.dest2:
                action.furgo.dest2.bicicletas_trasladadas -= action.furgo.cant_bicis2
            new_lista_furgo.list_furgos = [furgo for furgo in new_lista_furgo.list_furgos if furgo != action.furgo]#No podríamos hacer pop y ya?
            # Aquí puedes agregar la lógica para sumar las bicis de la furgo al origen si es necesario

        elif isinstance(action, furgo_move_origin):
            furgo = self.findfurgo(new_lista_furgo.list_furgos, action.furgo)
            furgo.origen.hayfurgos = False  # Marcar que la estación origen ya no tiene furgo
            furgo.origen = action.originnew
            furgo.origen.hayfurgos = True  # Marcar que la nueva estación origen tiene furgo
        elif isinstance(action, furgo_move_dest):
            furgo = self.findfurgo(new_lista_furgo.list_furgos, action.furgo)
            furgo.dest1.bicicletas_trasladadas -= furgo.cant_bicis1 #Las bicis que llevaba al antiguo destino pasan a ser 0
            furgo.dest1 = action.destnew #cambio de destino
            furgo.dest1.bicicletas_trasladadas += furgo.cant_bicis1 #al nuevo destino llevo las bicis del viejo destino
        elif isinstance(action, asignar_dest2):
            furgo = self.findfurgo(new_lista_furgo.list_furgos, action.furgo)
            if furgo.dest2:
                furgo.dest2.bicicletas_trasladadas -= furgo.cant_bicis2 #Las bicis que llevaba al antiguo destino pasan a ser 0
            furgo.bikes2 = action.bikes2
            furgo.dest2 = action.dest2
            furgo.dest2.bicicletas_trasladadas += furgo.bikes2 #Las bicis que llevaba al antiguo destino pasan a ser 0

        elif isinstance(action, incrementar_num_bici):
            furgo = self.findfurgo(new_lista_furgo.list_furgos, action.furgo)
            if action.dest2:
                furgo.cant_bicis2 = action.bibic_nou1
                furgo.dest2.bicicletas_trasladadas += 1 
            else:
                furgo.cant_bicis1 = action.bibic_nou1
                furgo.dest1.bicicletas_trasladadas += 1 


        elif isinstance(action, reduir_num_bici):
            
            furgo = self.findfurgo(new_lista_furgo.list_furgos, action.furgo)
            if action.dest2:
                furgo.cant_bicis2 = action.bibic_nou1
                furgo.dest2.bicicletas_trasladadas -= 1 

            else:
                furgo.cant_bicis1 = action.bibic_nou1
                furgo.dest1.bicicletas_trasladadas -= 1 
                
        return new_lista_furgo


    def distancia_manhattan(self, estacion1, estacion2):
        return abs(estacion1.coordX - estacion2.coordX) + abs(estacion1.coordY - estacion2.coordY)


    def ganancias_mov(self) -> float:
        perdidas=0
        ingresos=0
        self.recorrido=0
        for furgo in self.list_furgos:
            self.recorrido+=self.distancia_manhattan(furgo.origen,furgo.dest1)
            if furgo.dest2:
                self.recorrido+=self.distancia_manhattan(furgo.dest1,furgo.dest2)
            margen_inicio = (furgo.origen.num_bicicletas_no_usadas+furgo.origen.num_bicicletas_next)-furgo.origen.demanda

            bici1,bici2=furgo.dame_bicis(True)

            if (margen_inicio)<=0:
                perdidas+=(bici1+bici2)
            elif margen_inicio-(bici1+bici2)<=0:
                perdidas+=abs(margen_inicio-(bici1+bici2))

            # Actualizar el registro de bicicletas movidas

            if furgo.dest2:

                bicis_ya_en_estacion1= (furgo.dest1.bicicletas_trasladadas-furgo.cant_bicis1)
                bicis_ya_en_estacion2= (furgo.dest2.bicicletas_trasladadas-furgo.cant_bicis2)
                ingresos_ant=(furgo.cant_bicis1+furgo.dest1.num_bicicletas_next+furgo.dest1.num_bicicletas_no_usadas+bicis_ya_en_estacion1+furgo.cant_bicis1+furgo.dest2.num_bicicletas_next+furgo.dest2.num_bicicletas_no_usadas+bicis_ya_en_estacion2)-(furgo.dest1.demanda+furgo.dest2.demanda)
                if ingresos_ant<=0:
                    ingresos+=(bici1+bici2)-perdidas
                else:
                    margen_bicis_llevar=(furgo.dest1.demanda+furgo.dest2.demanda)-(furgo.dest1.num_bicicletas_next+furgo.dest1.num_bicicletas_no_usadas+bicis_ya_en_estacion1+furgo.dest2.num_bicicletas_next+furgo.dest2.num_bicicletas_no_usadas+bicis_ya_en_estacion2)
                    if margen_bicis_llevar<=0:
                        ingresos+= (-bici1-bici2)-perdidas
                    else:
                        if margen_bicis_llevar-(bici1+bici2)>=0:
                            ingresos += (bici1+bici2)
                        else: 
                            ingresos+=margen_bicis_llevar

            else:
                bicis_ya_en_estacion1= (furgo.dest1.bicicletas_trasladadas-furgo.cant_bicis1)
                ingresos_ant= (furgo.cant_bicis1+furgo.dest1.num_bicicletas_next+furgo.dest1.num_bicicletas_no_usadas+bicis_ya_en_estacion1)-furgo.dest1.demanda
                if ingresos_ant<=0:
                    ingresos+=(bici1+bici2)-perdidas
                else:
                    margen_bicis_llevar=(furgo.dest1.demanda)-(furgo.dest1.num_bicicletas_next+furgo.dest1.num_bicicletas_no_usadas+bicis_ya_en_estacion1)
                    if margen_bicis_llevar<=0:
                        ingresos+= (-bici1-bici2)-perdidas
                    else:
                        if margen_bicis_llevar-(bici1+bici2)>0:
                            ingresos += (bici1+bici2)-perdidas
                        else:
                            ingresos+=margen_bicis_llevar-perdidas

           
        if self.params.params:
            self.beneficio_total=-ingresos
            return -ingresos
        
        else:
            self.beneficio_total=ingresos
            return ingresos




    def heuristico_costes(self) -> float:
        coste_estado = 0
        km_recor=0
        for furgo in self.list_furgos:
            # Calculando el coste de kilómetros
            km_recor += self.distancia_manhattan(furgo.origen, furgo.dest1)
            if furgo.dest2 is not None:
                km_recor += self.distancia_manhattan(furgo.dest1, furgo.dest2)
            
            nb = furgo.total_bicis()  # Total de bicicletas transportadas por la furgoneta
            coste_estado += (((nb + 9) // 10) * (km_recor/1000))  # Ajusta esta fórmula según tus necesidades
        return -coste_estado  # Retornamos el coste como un valor negativo para indicar pérdida



    def heuristico_beneficio(self):
        self.beneficio_total= self.ganancias_mov()+self.heuristico_costes()
        return self.beneficio_total 