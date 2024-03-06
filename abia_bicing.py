from typing import Generator
import random


class Estacion(object):
    """
    Clase que representa una estación de Bicing
    """

    def __init__(self, x: int, y: int):
        """
        * coordX y coordY son atributos públicos que representan las
          coordenadas X e Y de la estación Bicing en metros
          bicicletas para la siguiente hora
        * num_bicicletas_next es un atributo público que guarda
          el número de bicicletas que habrá en la siguiente hora
          sin contar con los traslados
        * num_bicicletas_no_usadas es un atributo público que guarda
          el número de bicicletas que no se moverán en la hora actual  BICIS ACTUALS
        """
        self.coordX: int = x*100 #CANVIAT (ERA METRES I VOLEM KM)
        self.coordY: int = y*100 #CANVIAT
        self.hayfurgos = False
        self.num_bicicletas_no_usadas: int = 0
        self.num_bicicletas_next: int = 0
        self.bicicletas_trasladadas = 0
    def __eq__(self, __value: object) -> bool:
        return self.coordX== __value.coordX and self.coordY==__value.coordY and self.num_bicicletas_no_usadas==__value.num_bicicletas_no_usadas and self.num_bicicletas_next==__value.num_bicicletas_next

    def __str__(self) -> str:
        return f"({self.coordX}, {self.coordY})"

    
    def __hash__(self):
        return hash(self.coordX+self.coordY*100)


class Estaciones(object): #LST[estacion(coordX,coordY,num_bicicletas_no_usadas,num_bicicletas_next ),estacion(),...]
    """
    Clase que representa una lista ordenada de estaciones (instancias de Estacion)
    """

    def __init__(self, num_estaciones: int, num_bicicletas: int, semilla: int):
        """
        Constructora de Estaciones
        * num_estaciones: número de estaciones a generar
        * num_bicicletas: número de bicicletas a repartir
        * semilla: semilla del generador de números aleatorios
        """
        self.num_bicicletas: int = num_bicicletas
        self.rng: random.Random = random.Random(semilla)
        mitad_estaciones: int = int(num_estaciones / 2)
        self.lista_estaciones: list[Estacion] = []


        #  PERQUE MITAD ESTACIO?
        #"est" es una objecte stacio
        for _ in range(mitad_estaciones):
            est = Estacion(self.rng.randint(0, 99), self.rng.randint(0, 99))
            self.lista_estaciones.append(est)

        for _ in range(mitad_estaciones, num_estaciones):
            est = Estacion(self.rng.randint(0, 49) + 25, self.rng.randint(0, 49) + 25)
            self.lista_estaciones.append(est)

        self.__genera_estado_actual()
        self.__genera_estado_movimientos()
        self.__genera_proxima_demanda()

    def __genera_estado_actual(self):
        for est in self.lista_estaciones:
            est.num_bicicletas_no_usadas = 0

        i = self.num_bicicletas
        while i > 0:
            asignadas = self.rng.randint(0, 1)
            id_est = self.rng.randint(0, len(self.lista_estaciones) - 1)
            self.lista_estaciones[id_est].num_bicicletas_no_usadas = \
                self.lista_estaciones[id_est].num_bicicletas_no_usadas + asignadas
            i = i - asignadas

    def __genera_estado_movimientos(self):
        num_movimientos: int = int(float(self.num_bicicletas) * 0.8)

        for est in self.lista_estaciones:
            est.num_bicicletas_next = 0

        for id_est in range(num_movimientos):
            var3 = self.rng.randint(0, len(self.lista_estaciones) - 1)
            var2 = self.rng.randint(0, len(self.lista_estaciones) - 1)
            if self.lista_estaciones[var3].num_bicicletas_no_usadas > 0:
                self.lista_estaciones[var3].num_bicicletas_no_usadas = \
                    self.lista_estaciones[var3].num_bicicletas_no_usadas - 1
                self.lista_estaciones[var2].num_bicicletas_next = \
                    self.lista_estaciones[var2].num_bicicletas_next + 1

        for est in self.lista_estaciones:
            est.num_bicicletas_next = est.num_bicicletas_next + est.num_bicicletas_no_usadas

    def __genera_proxima_demanda(self):
        media_bicicletas: int = int(self.num_bicicletas / len(self.lista_estaciones))

        for est in self.lista_estaciones:
            if self.rng.random() > 0.5:
                factor = 1
            else:
                factor = -1
            est.demanda = media_bicicletas + factor * self.rng.randint(0, int(float(media_bicicletas) * 0.5) - 1)


class furgonetas(object):
    def __init__(self, origen: Estacion, dest1: Estacion, cant_bicis1: int, dest2=None, cant_bicis2=0) -> None:
        self.origen=origen
        self.dest1=dest1
        self.dest2=dest2
        self.cant_bicis1=cant_bicis1
        self.cant_bicis2=cant_bicis2
        self.origen.hayfurgos = True
    def __str__(self) -> str:
        if self.dest2:
            return f"Furgo sale de {self.origen} y va a {self.dest1} y {self.dest2} con {self.cant_bicis1} y {self.cant_bicis2}"
        else:
            return f"Furgo sale de {self.origen} y va a {self.dest1} con {self.cant_bicis1}"

    def __eq__(self, furgo2):
        if self.origen == furgo2.origen and self.dest1 == furgo2.dest1 and self.cant_bicis1 == furgo2.cant_bicis1:
            if self.dest2 is None and furgo2.dest2 is None:
                return True
            elif self.dest2 is not None and furgo2.dest2 is not None and self.dest2 == furgo2.dest2 and self.cant_bicis2 == furgo2.cant_bicis2:
                return True
        else:
            return False

    def total_bicis(self):
        return self.cant_bicis1 + (self.cant_bicis2 if self.cant_bicis2 else 0)
    
    def dame_bicis(self,lasdos=False):
        if lasdos:
            return self.cant_bicis1,self.cant_bicis2
        else:
            return self.cant_bicis1
