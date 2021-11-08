import random
import json
from mosaik.util import connect_randomly, connect_many_to_one
import mosaik

SIM_CONFIG = {
    # 'CSV': {
    #     'python': 'mosaik_csv:CSV',
    # },
    # 'DB': {
    #     'cmd': 'mosaik-hdf5 %(addr)s',
    # },
    'HouseholdSim': {
        'python': 'householdsim.mosaik:HouseholdSim',
        # 'cmd': 'mosaik-householdsim %(addr)s',
    },
    'PyPower': {
        'python': 'mosaik_pypower.mosaik:PyPower',
        # 'cmd': 'mosaik-pypower %(addr)s',
    },
    'WebVis': {
        'cmd': 'mosaik-web -s 0.0.0.0:8000 %(addr)s',
    },
}

#START = '2014-01-01 00:00:00'
START = '2014-01-01 00:00'
END = 31 * 24 * 3600  # 1 day
# PV_DATA = 'data/pv_10kw.csv'
PROFILE_FILE = 'data/profiles.data.gz'
GRID_NAME = 'demo_lv_grid'
GRID_FILE = 'data/%s.json' % GRID_NAME
porta_agente = 20000


def load_nodes(file):
    """ Retorna uma lista com a identificação {name} de cada nó em um arquivo .json

    :param file: force.json
    :return: list: lista do número de nós da rede
    """
    with open(file, 'r') as f:
        data = json.load(f)

    acoms_id = list()
    for i in data['bus']:
        acoms_id.append(i[0])
        # print(i[0])

    return acoms_id[2:]

def create_scenario(sim_config, acom_sim_names):
    world = mosaik.World(sim_config)

    # Start simulators
    pypower = world.start('PyPower', step_size=15*60)
    hhsim = world.start('HouseholdSim')
    acom_sim_list = list()
    for i, name in acom_sim_names.items(): # Cria um simulador por Agente de Comunicação
        acom_sim = world.start(name, eid_prefix='AgCom_', start=START, step_size=1 * 60)  # Inicializa cada um dos simuladores
        acom_sim_list.append(acom_sim)
    # print(acom_sim_list)
    # pvsim = world.start('CSV', sim_start=START, datafile=PV_DATA)

    # Instantiate models
    grid = pypower.Grid(gridfile=GRID_FILE).children
    houses = hhsim.ResidentialLoads(sim_start=START,
                                    profile_file=PROFILE_FILE,
                                    grid_name=GRID_NAME).children
    acom_agents = [i.AgCom.create(1) for i in acom_sim_list]
    # pvs = pvsim.PV.create(20)

    # Connect entities
    connect_buildings_to_grid(world, houses, grid)
    nodes = [e for e in grid if e.type in ('RefBus, PQBus')]
    nodes = {str(n.eid): n for n in nodes}
    print(nodes)
    for acom_agent, node_id in zip(acom_agents, range(len(acom_agents))): # DÚVIDA: em start_mosaik_sim.py, config_dict.keys() = config_dict[node] == node_id???
        # print(acom_agent)
        # print(node_id)
        world.connect(acom_agent, nodes[node_id], 'v_out') # TODO: alterar nome da chave do dicionatio num for
        # print('>>> INFO: {} connected with {}.'.format(acom_agent.full_id, nodes[node_id].full_id)
        #connections.setdefault(prosumer.full_id, []).append(nodes[node_id].full_id)
    # connect_many_to_one(world, nodes, hdf5, 'P', 'Q', 'Vl', 'Vm', 'Va')
    # connect_randomly(world, pvs, [e for e in grid if 'node' in e.eid], 'P')

    # TODO: conectar an e adc na estrutura do acom

    # Database
    # db = world.start('DB', step_size=60, duration=END)
    # hdf5 = db.Database(filename='demo.hdf5')
    # connect_many_to_one(world, houses, hdf5, 'P_out')
    # connect_many_to_one(world, pvs, hdf5, 'P')  

    # branches = [e for e in grid if e.type in ('Transformer', 'Branch')]
    # connect_many_to_one(world, branches, hdf5,
                        # 'P_from', 'Q_from', 'P_to', 'P_from')

    # Web visualization
    webvis = world.start('WebVis', start_date=START, step_size=60)
    webvis.set_config(ignore_types=['Topology', 'ResidentialLoads', 'Grid',
                                    'Database'])
    vis_topo = webvis.Topology()

    connect_many_to_one(world, nodes, vis_topo, 'P', 'Vm')
    webvis.set_etypes({
        'RefBus': {
            'cls': 'refbus',
            'attr': 'P',
            'unit': 'P [W]',
            'default': 0,
            'min': 0,
            'max': 30000,
        },
        'PQBus': {
            'cls': 'pqbus',
            'attr': 'Vm',
            'unit': 'U [V]',
            'default': 230,
            'min': 0.99 * 230,
            'max': 1.01 * 230,
        },
    })

    connect_many_to_one(world, houses, vis_topo, 'P_out')
    webvis.set_etypes({
        'House': {
            'cls': 'load',
            'attr': 'P_out',
            'unit': 'P [W]',
            'default': 0,
            'min': 0,
            'max': 3000,
        },
    })

    # connect_many_to_one(world, pvs, vis_topo, 'P')
    # webvis.set_etypes({
    #     'PV': {
    #         'cls': 'gen',
    #         'attr': 'P',
    #         'unit': 'P [W]',
    #         'default': 0,
    #         'min': -10000,
    #         'max': 0,
    #     },
    # })

    world.run(until = END)
    return


def connect_buildings_to_grid(world, houses, grid):
    buses = filter(lambda e: e.type == 'PQBus', grid)
    buses = {b.eid.split('-')[1]: b for b in buses}
    house_data = world.get_data(houses, 'node_id')
    for house in houses:
        node_id = house_data[house]['node_id']
        world.connect(house, buses[node_id], ('P_out', 'P'))


if __name__ == '__main__':
    acoms_id = load_nodes(GRID_FILE) # Descobre ID de cada nó da rede
    
    acom_sim_names = dict()
    for i in acoms_id: # Conecta um Agente de Comunicação por nó da rede
        name = 'AgComSim_{}'.format(i)
        acom_sim_names[i] = name
        SIM_CONFIG[name] = {'connect': 'localhost:' + str(porta_agente)}
        porta_agente += 1000
    # print(SIM_CONFIG)
    # print(acom_sim_names)

    create_scenario(SIM_CONFIG, acom_sim_names)