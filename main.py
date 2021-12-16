from data_structure import Graph
from models import BranchAndBound, NearestNeighbors, ClarkeAndWright
from utils.utils import identify_cycles, unique_cycles

import sys


def test(model_methode):
    if model_methode == 'BranchAndBound':
        model = BranchAndBound()
    elif model_methode == 'NearestNeighbors':
        model = NearestNeighbors()
    elif model_methode == 'ClarkeAndWright':
        model = ClarkeAndWright()

    data = Graph.read_data()
    model.fit(data)
    cycles, length = model._optimize()
    cycles = unique_cycles(identify_cycles(cycles))
    print(cycles, ":", length)


def main():
    models = ['BranchAndBound', 'NearestNeighbors', 'ClarkeAndWright']
    model = 'BranchAndBound' if sys.argv[1] not in models else sys.argv[1]
    test(model)


if __name__ == '__main__':
    main()
