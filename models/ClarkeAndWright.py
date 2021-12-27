from data_structure import Graph
from utils.utils import identify_cycle


class ClarkeAndWright:

    def __init__(self) -> None:
        self.__data: Graph = None
        self.__saving = []

    def get_path_length(self, path):
        if len(path) < 2:
            return 0
        first_vertex = path[0]
        length = 0
        for vertex in path[1:]:
            length += self.__data.get_distance(first_vertex, vertex)
            first_vertex = vertex
        return length

    def get_saving(self, start_vertex=None):
        if not start_vertex:
            start_vertex = self.__data.get_vertices()[0]
        s = []
        for i, vertex_1 in enumerate(self.__data.get_vertices(), start=1):
            for vertex_2 in self.__data.get_vertices()[i:]:
                if vertex_1 != start_vertex and vertex_2 != start_vertex:
                    s.append([self.__data.get_distance(vertex_1, start_vertex) + self.__data.get_distance(
                        start_vertex, vertex_2) - self.__data.get_distance(vertex_1, vertex_2), (vertex_1, vertex_2)])
        s.sort(key=lambda x: x[0], reverse=True)
        return s

    def _get_optimal_path(self, start_vertex=None):
        if not start_vertex:
            start_vertex = self.__data.get_vertices()[0]
        saving = self.get_saving(start_vertex)
        li = [start_vertex, saving[0][1][0], saving[0][1][1], start_vertex]
        for _, pair in saving[1:]:
            if (pair[0] in li and pair[1] in li) or (pair[0] not in li and pair[1] not in li):
                continue
            if (pair[0] in li):
                if li[1] == pair[0]:
                    li.insert(1, pair[1])
                elif li[-2] == pair[0]:
                    li.insert(-2, pair[1])
            elif (pair[1] in li):
                if li[1] == pair[1]:
                    li.insert(1, pair[0])
                elif li[-2] == pair[1]:
                    li.insert(-2, pair[0])
        return li

    def _optimize(self):
        # optimal_path = []
        # optimal_path_length = float("inf")
        # for vertex in self.__data.get_vertices():
        #     path = self._get_optimal_path(vertex)
        #     path_length = self.get_path_length(path)
        #     if path_length < optimal_path_length:
        #         optimal_path = [path]
        #         optimal_path_length = path_length
        #     elif path_length == optimal_path_length:
        #         optimal_path.append(path)
        optimal_path = self._get_optimal_path()
        optimal_path_length = self.get_path_length(optimal_path)
        return (optimal_path, optimal_path_length)

    def fit(self, data) -> None:
        self.__data = data
