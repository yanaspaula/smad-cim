# start_mygrid_acom.py
import sys, os
import json
import mosaik
import mosaik.util
from mosaik_mygrid.mosaik import MyGrid

"""
    TODO:
    1. Conectar entidades:
    - Conexão: acom -> mygrid (valores aleatórios de tensão)
    - Conexão: mygrid -> db

    2. Consertar erro do Acom (dicionário do get_data() está errado).

    3. Consertar erro de database (HDF5).
    
"""
porta_agente = 20000

SIM_CONFIG = {
	'MyGrid': {
		'python': 'mosaik_mygrid.mosaik:MyGrid'
	},
	'HDF5':{
		'python': 'mosaik_hdf5:MosaikHdf5'
	},
    'Collector': {
        'cmd': 'python collector.py %(addr)s', # Has model to print data in terminal
    },
}

"""
	Determinações dos tempos de simulação no Mosaik:
"""
# QTD_HOURS = 1 * 23
START = '01/10/2019 - 00:00:00' 
END = 100 * 60	# X minutes
# END = int(QTD_HOURS * 60 * 60)

def load_nodes(file):
    """ Retorna uma lista com a identificação {name} de cada nó em um arquivo .json

    :param file: force.json
    :return: list: lista do número de nós da rede
    """
    with open(file, 'r') as f:
        data = json.load(f)

    acoms_id = list()
    for i in data['nodes']:
        acoms_id.append(i['name'])

    return acoms_id

def create_scenario(sim_config, acom_sim_names):
    # Inicializa configurações de simuladores para o cenário Mosaik
    world = mosaik.World(sim_config)

    # Inicializa simuladores
    mygrid_sim = world.start('MyGrid', eid_prefix = "MyGrid_", start = START, step_size = 1 * 60)
    # hdf5_sim = world.start('HDF5', step_size = 1*60, duration = END)
    collector = world.start('Collector', step_size=60) # Has model to print data in terminal

    acom_sim_list = list()
    for i, name in acom_sim_names.items(): # Cria um simulador por Agente de Comunicação
        acom_sim = world.start(name, eid_prefix='AgCom_', start=START, step_size=1 * 60)  # Inicializa cada um dos simuladores
        acom_sim_list.append(acom_sim)
    # print(acom_sim_list)

    # Cria instâncias de cada simulador
    # db = hdf5_sim.Database(filename='data.hdf5') # world database
    acom_agents = [i.AgCom.create(1) for i in acom_sim_list]
    # print(acom_agents)
    monitor = collector.Monitor() # Has model to print data in terminal

    with open('{}/mygrid_smad.json'.format(sys.path[0]), 'r') as f:
        _mygrid = mygrid_sim.Grid(gridfile = f).children

    # Conecta entidades
    for ag in acom_agents:
        # print(ag[0])
        world.connect(ag[0], monitor, 'v_out')

    # nodes = [e for e in _mygrid if e.type in ('RefBus', 'PQBus')]
    # nodes = {str(n.eid): n for n in nodes}
    # for node_id, acom_agent in zip(,acom_agents)
        # print('>>> INFO: {} connected with {}.'.format(nodes[str(node_id)].full_id, prosumer_agent[0].full_id))

    world.run(until = END)

    return

if __name__ == '__main__':
    acoms_id = load_nodes('mygrid_smad.json') # Descobre ID de cada nó da rede
    
    acom_sim_names = dict()
    for i in acoms_id: # Conecta um Agente de Comunicação por nó da rede
        name = 'AgComSim{}'.format(i)
        acom_sim_names[i] = name
        SIM_CONFIG[name] = {'connect': 'localhost:' + str(porta_agente)}
        porta_agente += 1000
    # print(SIM_CONFIG)
    # print(acom_sim_names)

    create_scenario(SIM_CONFIG, acom_sim_names)

