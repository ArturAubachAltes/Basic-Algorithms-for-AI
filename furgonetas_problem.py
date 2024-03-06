from typing import Generator
from aima.search import Problem
from StateRepresentation import StateRepresentation
from operators import furgo_operators

		
class BiciProblem(Problem):
	def __init__(self, initial_state,hueristico=True, useoneaction=False):
		self.num_steps = 0
		self.useoneaction=useoneaction
		self.hueristico = hueristico
		super().__init__(initial_state)

	def actions(self, state: StateRepresentation):
		if self.useoneaction:
			self.num_steps +=1
			return state.generate_one_action()
		else:
			self.num_steps +=1
			return state.generate_actions()


	def result(self, state: StateRepresentation, action: furgo_operators) -> StateRepresentation:
		return state.apply_action(action)

	def value(self, state: StateRepresentation) -> float:
		if self.hueristico:
			return state.ganancias_mov()


		else:
			return state.heuristico_beneficio()

	
