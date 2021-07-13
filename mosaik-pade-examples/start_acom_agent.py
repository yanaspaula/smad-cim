import sys
sys.path.insert(1, '/home/nana/Documents/Estágio UFC/Codes/SMAD CIM/smad-cim/core')
from sys import argv
from acom import *
from pade.misc.utility import display_message, start_loop

'''
	DÚVIDAS

1. Criei __init__.py em pastas, mas não consegui importar classes - Apenas com sys
'''

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