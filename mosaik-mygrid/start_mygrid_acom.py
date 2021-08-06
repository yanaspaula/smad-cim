# start_mygrid_acom.py
import sys, os
import json
import mosaik
import mosaik.util
from mosaik_mygrid.mosaik import MyGrid

"""
	Dúvidas:

	1. A importação da classe está correta, considerando a pasta?
"""

porta_agente = 20000

SIM_CONFIG = {
	'AgCom':{
		'connect': 'localhost:' + str(porta_agente),
	},
	'MyGrid': {
		'python': 'mosaik_mygrid.mosaik:MyGrid' # Dúvida 1
	}
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
mygrid_sim = world.start('MyGrid', eid_prefix = "IED-read_", start = START, step_size = 1 * 60)
acom_sim = world.start('AgCom', eid_prefix = 'AgenteCom_', start = START, step_size = 1 * 60)

# Creates instances
with open('{}/mygrid_smad.json'.format(sys.path[0]), 'r') as f:
  file = json.load(f)
  ieds = mygrid_sim.Grid(file)
acom = acom_sim.AgCom()

# Connects entities
world.connect(ieds, acom, ['load_nodes', 'acom_attr'])

world.run(until = END)