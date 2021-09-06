from sys import argv
import json
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'core')) # imports path for acom
from acom import *
from pade.misc.utility import display_message, start_loop

def count_nodes(file):
    """ Conta números de nós existentes em um arquivo .json

    :param file: force.json
    :return: int: número de nós da rede
    """
    with open(file, 'r') as f:
        data = json.load(f)

    return len(data['nodes'])

if __name__ == '__main__':
	# Inicialização
	c = 0
	agents = list()	
	port = int(argv[1]) + c

	# Instancia IED do AgCom
	ied = FileIED('CH13', ('localhost', 50013), 'IED_test.txt')
	ieds = [ied]

	# Instancia AgComs
	for i in range(count_nodes('mygrid_smad.json')): # Inicializa Agentes de acordo com número de nós
		agent_name = 'AgCom_{}@localhost:{}'.format(i, port + c)
		agents.append(AgenteCom(AID(name = agent_name), 'sub_teste', ieds)) # Inicializa PADE
		c += 1000	

	start_loop(agents)