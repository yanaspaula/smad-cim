# random_simulator.py

import random
import mosaik_api

# Meta-data dictionary configuration for Mosaik
META = {
	'models': {
		'RandomModel': { # our Model in simulation.py and all its read/write attributes
			'public': True,
			'params': [],
			'attrs': ['val'],
		}
	}
}

"""
	A model that generates a random value to be read by acom.
"""
class Model:
	def __init__(self):
		self.val = random.random()
	# 	self.val = val
	
	# def step(self):
	# 	self.val += random.random()

"""
	Creates and stores models. 
	Collects some important data needed for Mosaik.
"""
class Simulator(object):
	def __init__(self):
		self.models = []


		self.data = []

	def add_model(self):
		model = Model()
		self.models.append(model)
		self.data.append([])

	def step(self): 
		for i, model in enumerate(self.models):
			# model.step()
			self.data[i].append(model.val) # adds a *model* *val* to in the ``Simulator`` object *data* instance

"""
	Integrates our created simulator with Mosaik via the Mosaik API
"""
class RandomSim(mosaik_api.Simulator):
	def __init__(self): # Initializes our created model
		super().__init__(META)
		self.simulator = Simulator() # Imports our model __init__() into Mosaik's simulation
		self.eid_prefix = 'RanModel'
		self.entities = {}

	def init(self, sid, eid_prefix = None): # Initialization sent to Mosaik
		if eid_prefix is not None:
			self.eid_prefix = eid_prefix
		return self.meta

	def create(self, num, model): # Initializes *num* instances of a *model* type for Mosaik's API
		next_eid = len(self.entities)
		entities = []

		for i in range(next_eid, next_eid + num):
			eid = "%s%d" % (self.eid_prefix, i)
			self.simulator.add_model()
			self.entities[eid] = i
			entities.append({"eid": eid, "type": model})
		return entities

	def step(self, time, inputs): # Gets data for Mosaik
		for eid, attrs in inputs.items():
			for attr, values in attrs.items():
				model_idx = self.entities[eid]

		self.simulator.step()
		return time + 60 # Step size is one minute

	def get_data(self, outputs): # Allows other simulators to get our ``Model`` information
		models = self.simulator.models
		data = {}
		for eid, attrs in outputs.items():
			model_idx = self.entities[eid]
			data[eid] = {}
			for attr in attrs:
				if attr not in self.meta['models']['RandomModel']['attrs']:
					raise ValueError("Unknown output attribute: %s" % attr)

				data[eid][attr] = getattr(models[model_idx], attr)
		return data

"""
	Example of an execution.
"""
# if __name__ == '__main__':
	
# 	sim = Simulator()

# 	# Adds *2* models in the simulator
# 	for i in range(2):
# 		sim.add_model()
	
# 	sim.add_model()
# 	sim.step()

# 	print("Random values in Model:")
# 	for i, inst in enumerate(sim.data):
# 		print("%d: %s" % (i, inst))