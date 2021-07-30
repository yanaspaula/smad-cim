from sys import argv
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'core')) # imports path for acom
from acom import *
from pade.misc.utility import display_message, start_loop

if __name__ == '__main__':
	# Inicialização
	c = 0
	agents = list()	
	port = int(argv[1]) + c

	# Instancia IED do AgCom
	ied = FileIED('CH13', ('localhost', 50013), 'IED_test.txt')
	ieds = [ied]

	# Instancia AgCom
	agent_name = 'ACom_SMAD_{}@localhost:{}'.format(port, port)
	ag_com = AgenteCom(
		AID(name = agent_name), 
		'sub_teste', 
		ieds)

	# Inicializa PADE
	agents.append(ag_com)
	c += 1000
	start_loop(agents)