from utils.utils import visualize_cycle
from data_structure import Graph
from models import BranchAndBound, NearestNeighbors, ClarkeAndWright
from utils.utils import identify_cycles, unique_cycles

import sys


def test(model_methode, data_folder="C:\\Personal-Workspace\\Jupyter_Notebook\\TMS_0\\TMS\\data\\", sep=';'):

    data_file = data_folder + 'coordinates_data.csv'
    output_file = data_folder + f'output_{model_methode}.html'

    Network = Graph()

    with open(data_file, 'r') as data_file:
        lines = list(map(lambda x: x[:], data_file.readlines()))
        for line in lines:
            lat, lon, dem = map(float, line.split(sep))
            coordinates = lat, lon
            Network.add_vertex_if_not_exist(coordinates, dem)
        Network.add_neighbors()

    if model_methode == 'BranchAndBound':
        model = BranchAndBound()
    elif model_methode == 'NearestNeighbors':
        model = NearestNeighbors()
    elif model_methode == 'ClarkeAndWright':
        model = ClarkeAndWright()

    model.fit(Network)
    cycles, length = model._optimize()
    # cycles = unique_cycles(identify_cycles(cycles))
    # cycles = unique_cycles(cycles)
    print(cycles, ":", length)
    if isinstance(cycles[0], list):
        _map = visualize_cycle(cycles[0])
    else:
        _map = visualize_cycle(cycles)
    with open(output_file, 'wb') as op_file:
        _map.save(op_file)


def main():
    models = ['BranchAndBound', 'NearestNeighbors', 'ClarkeAndWright']
    model = 'BranchAndBound' if sys.argv[1] not in models else sys.argv[1]
    test(model)


if __name__ == '__main__':
    main()
