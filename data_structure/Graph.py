from . import Vertex


class Graph:

    def __init__(self) -> None:
        self.__vertices = []
        self.__metadata = {
            'vertices_count': 0,
            'min_distance': float('inf'),
            'max_distance': 0
        }

    def __add_vertex(self, ID) -> Vertex:
        vertex = Vertex(ID)
        self.__vertices.append(vertex)
        self.__metadata['vertices_count'] += 1
        return vertex

    def add_vertex_if_not_exist(self, ID) -> Vertex:
        for vertex in self.__vertices:
            if vertex.get_ID() == ID:
                return vertex
        vertex = self.__add_vertex(ID)
        return vertex

    def update_endpoints(self, endpoint_1, endpoint_2, distance):
        endpoint_1.add_neighbor(endpoint_2, distance)
        endpoint_2.add_neighbor(endpoint_1, distance)
        if distance > self.longest_distance():
            self.__update_longest_distance(distance)
        if distance < self.shortest_distance():
            self.__update_shortest_distance(distance)

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
            return vertex_1.get_neighbor_distance(vertex_2)

    def vertices_count(self):
        return self.__metadata.get('vertices_count')

    def __update_longest_distance(self, distance):
        self.__metadata['max_distance'] = distance

    def __update_shortest_distance(self, distance):
        self.__metadata['min_distance'] = distance

    def longest_distance(self):
        return self.__metadata.get('max_distance')

    def shortest_distance(self):
        return self.__metadata.get('min_distance')

    def get_metadata(self):
        return self.vertices_count(), self.longest_distance(), self.shortest_distance()

    def read_data(file="D:\\AMOA\\INE3\\P2\\Transport Operations Management\\TP_Probleme_tournee_vehicule\\data.txt"):
        with open(file, 'rb') as data_file:
            lines = list(map(lambda x: x[:-2], data_file.readlines()))
            data = Graph()
            for line in lines:
                ID_1, ID_2, distance = map(int, line.split())
                endpoint_1 = data.add_vertex_if_not_exist(ID_1)
                endpoint_2 = data.add_vertex_if_not_exist(ID_2)
                data.update_endpoints(endpoint_1, endpoint_2, distance)

        return data
