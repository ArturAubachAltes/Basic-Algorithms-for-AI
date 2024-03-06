
from aima.search import hill_climbing,simulated_annealing,exp_schedule
import time
from abia_bicing import Estaciones
from furgonetas_problem import BiciProblem
from problem_parameters import ProblemParameters
from StateRepresentation import StateRepresentation
from solucions_inicialss import Solucio_greedy3, Solucio_greedy2
import math
import random
import time


class Main:
    def __init__(self, model, maxim_furgonetas: int, numero_estaciones: int, numero_bicis: int, semilla: int = 1235, initial_state: int = 2, operadors: int = 3, heuristic:bool = True, k:int=1,lam:int=0.01,limit:int=20000): #heuristic= True: heuristico_beneficio, operador: qionss operadors utilitzar
        inicio = time.time()

        # Initialize estaciones
        self.estaciones = Estaciones(numero_estaciones, numero_bicis, semilla)

        if initial_state == 1:
            self.initial_state = []

        elif initial_state == 2:
            self.initial_state = Solucio_greedy2(self.estaciones, maxim_furgonetas, numero_bicis)
        elif initial_state == 3:
            self.initial_state = Solucio_greedy3(self.estaciones, maxim_furgonetas, numero_bicis)  # GREEADY


        # Set up other parameters
        self.params = ProblemParameters(maxim_furgonetas, numero_estaciones, numero_bicis, semilla, operadors,heuristic)
        self.initial_state = StateRepresentation(self.params, self.estaciones.lista_estaciones, self.initial_state)
        #print(self.initial_state)

        if model == "hill_climbing" :

            #self.results = hill_climbing(BiciProblem(self.initial_state, heuristic, False))
            
            self.a=BiciProblem(self.initial_state, heuristic, False)
            self.results = hill_climbing(self.a)
            
        
        elif model == "simulated_annealing":
            self.a=BiciProblem(self.initial_state, heuristic, True)
            self.results = simulated_annealing(self.a, exp_schedule(k, lam, limit))

        # Marcar el tiempo de finalización
        fin = time.time()

        # Calcular la duración
        self.duracion = fin - inicio

    # Methods to get the values
    def get_estaciones(self):
        return self.estaciones

    def get_initial_state(self):
        return self.initial_state

    def get_params(self):
        return self.params

    def get_results(self):
        return self.results

    def get_num_steps(self):
        return self.a.num_steps
    
    def get_time(self):
        return self.duracion

    def get_beneficio_total(self):
        return self.results.beneficio_total


