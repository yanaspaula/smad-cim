# start_mosaik_acom.py
import mosaik
import mosaik.util
import random_simulator


porta_agente = 20000

SIM_CONFIG = {
	'AgCom':{
		'connect': 'localhost:' + str(porta_agente),
	},
	'RandomSim': {
		'python': 'random_simulator:RandomSim'
	},
	'Collector': {
		'cmd': 'python collector.py %(addr)s', # Simulador de Monitor
	},
}


"""
	Determinações dos tempos de simulação no Mosaik:
"""
# QTD_HOURS = 1 * 23
START = '01/10/2019 - 00:00:00' 
END = 10 * 60	# X minutes
# END = int(QTD_HOURS * 60 * 60)


"""
	Inicialização do mundo no Mosaik
"""
# Initiates world and gets Simulators configuration
world = mosaik.World(SIM_CONFIG)

# Starts simulators
rand_sim = world.start('RandomSim', eid_prefix = "IED_read")
# collector = world.start('Collector', step_size = 60)
acom_sim = world.start('AgCom', eid_prefix = 'AgenteCom_', start = START, step_size = 1 * 60)
# acom = world.start('AgCom', eid_prefix = 'AgenteCom_', step_size = 1 * 60)


# Creates instances
ieds = rand_sim.RandomModel()
acom = acom_sim.AgCom()
# monitor = collector.Monitor()

# Connects entities
#world.connect(ieds, monitor, 'val')
print(ieds)
print(acom)
world.connect(ieds, acom, ['val', 'acom_attr'])

world.run(until = END)
