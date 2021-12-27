from data_structure.Vertex import Vertex
from data_structure import Graph
from utils.utils import identify_cycle


class NearestNeighbors:

    def __init__(self) -> None:
        self.__data: Graph = None

    def _get_optimal_path(self, vertex: Vertex, visited_vertices=[]):
        nearest_neighbors, nearest_neighbor_distance = vertex.get_nearest_neighbor(
            exclude=visited_vertices)
        if not nearest_neighbors:
            return [visited_vertices[0], vertex], self.__data.get_distance(visited_vertices[0], vertex)
        optimal_path, optimal_path_length = [], float("inf")
        for nearest_neighbor in nearest_neighbors:
            path, path_length = self._get_optimal_path(
                nearest_neighbor, visited_vertices=visited_vertices + [vertex])
            if path_length < optimal_path_length:
                optimal_path, optimal_path_length = path, path_length
        optimal_path.append(vertex)
        optimal_path_length += nearest_neighbor_distance
        return optimal_path, optimal_path_length

    def _optimize(self):
        optimal_path = []
        optimal_path_length = float("inf")
        for vertex in self.__data.get_vertices():
            path, path_length = self._get_optimal_path(vertex)
            print(f"Nearest Neighbor Cycle ({vertex} as depot):", path_length)
            if path_length < optimal_path_length:
                optimal_path = [path]
                optimal_path_length = path_length
            elif path_length == optimal_path_length:
                optimal_path.append(path)
        return (optimal_path, optimal_path_length)

    def fit(self, data):
        self.__data = data
