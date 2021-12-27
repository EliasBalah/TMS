from utils.utils import get_route_length
from . import Vertex


class Graph:

    def __init__(self) -> None:
        self.__vertices = []
        self.__bounds = tuple()

    def add_vertex(self, coordinates, value):
        vertex = Vertex(coordinates[0], coordinates[1], value)
        self.__vertices.append(vertex)

    def add_vertex_if_not_exist(self, coordinates, value) -> None:
        # Verify if the vertex is already exist
        for self_vertex in self.__vertices:
            if self_vertex.get_coordinates() == coordinates:
                if self_vertex.get_value() != value:
                    self_vertex.update_value(value)
                return self_vertex
        # If not, add it to self.__vertices
        self.add_vertex(coordinates, value)

    def add_neighbors(self):
        min_distance = float("inf")
        max_distance = 0
        for startpoint in self.__vertices:
            for endpoint in self.__vertices:
                if startpoint == endpoint:
                    continue
                startpoint.add_neighbor(endpoint)
            if startpoint.get_last_neighbor_added()[1] < min_distance:
                min_distance = startpoint.get_last_neighbor_added()[1]
            if startpoint.get_last_neighbor_added()[1] > max_distance:
                max_distance = startpoint.get_last_neighbor_added()[1]
        self.__bounds = (min_distance, max_distance)

    def get_vertices(self, from_edges=False):
        if not from_edges:
            return self.__vertices
        vertices = []
        for edge in self.__edges:
            start_vertex, end_vertex = edge.get_endpoints()
            if start_vertex not in vertices:
                vertices.append(start_vertex)
            if end_vertex not in vertices:
                vertices.append(end_vertex)
        return vertices

    def get_distance(self, vertex_1, vertex_2):
        if vertex_1 in self.__vertices and vertex_2 in self.__vertices:
            return get_route_length(vertex_1, vertex_2, distance='graph_hopper')

    def vertices_count(self):
        return len(self.__vertices)

    def bounds(self):
        return self.__bounds
