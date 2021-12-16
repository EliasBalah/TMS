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

    # Methodes for Nearest Neighbor Algorithm ============================================================================================================

    def get_NearestNeighborPath(self, start_vertex, vertex, visited_vertices=[]):
        nearest_neighbors, nearest_neighbor_distance = vertex.get_nearest_neighbor(
            exclude=visited_vertices)
        if not nearest_neighbors:
            return [start_vertex, vertex], self.get_distance(start_vertex, vertex)
        optimal_path, optimal_path_length = [], float("inf")
        for nearest_neighbor in nearest_neighbors:
            path, path_length = self.get_NearestNeighborPath(
                start_vertex, nearest_neighbor, visited_vertices=visited_vertices + [vertex])
            if path_length < optimal_path_length:
                optimal_path, optimal_path_length = path, path_length
        optimal_path.append(vertex)
        optimal_path_length += nearest_neighbor_distance
        return optimal_path, optimal_path_length

    def get_Optimal_NearestNeighborPath(self):
        optimal_path = []
        optimal_path_length = float("inf")
        for vertex in self.__vertices:
            path, path_length = self.get_NearestNeighborPath(vertex, vertex)
            print(f"Nearest Neighbor Cycle ({vertex.get_ID()} as depot):", self.get_path_with_IDs(
                path), "->", path_length)
            if path_length < optimal_path_length:
                optimal_path = [path]
                optimal_path_length = path_length
            elif path_length == optimal_path_length:
                optimal_path.append(path)
        return (optimal_path, optimal_path_length)

    # Methodes for Clarke and Wright Algorithm ============================================================================================================

    def get_path_length(self, path):
        if len(path) < 2:
            return 0
        first_vertex = path[0]
        length = 0
        for vertex in path[1:]:
            length += self.get_distance(first_vertex, vertex)
            first_vertex = vertex
        return length

    def get_graph_saving(self, start_vertex=None):
        if not start_vertex:
            start_vertex = self.__vertices[0]
        s = []
        for i, vertex_1 in enumerate(self.__vertices, start=1):
            for vertex_2 in self.__vertices[i:]:
                if vertex_1 != start_vertex and vertex_2 != start_vertex:
                    s.append([self.get_distance(vertex_1, start_vertex) + self.get_distance(
                        start_vertex, vertex_2) - self.get_distance(vertex_1, vertex_2), (vertex_1, vertex_2)])
        s.sort(key=lambda x: x[0], reverse=True)
        return s

    def get_ClarkeWrightPath(self, start_vertex):
        saving = self.get_graph_saving(start_vertex)
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

    def get_Optimal_ClarkeWrightPath(self):
        optimal_path = []
        optimal_path_length = float("inf")
        for vertex in self.__vertices:
            path = self.get_ClarkeWrightPath(vertex)
            path_length = self.get_path_length(path)
            print(f"Clarke & Wright Cycle ({vertex.get_ID()} as depot):", self.get_path_with_IDs(
                path), "->", path_length)
            if path_length < optimal_path_length:
                optimal_path = [path]
                optimal_path_length = path_length
            elif path_length == optimal_path_length:
                optimal_path.append(path)
        return (optimal_path, optimal_path_length)

    # =====================================================================================================================================================

    def unique_cycles(self, cycles):
        def isIncluded(cy, cys):
            res = 0
            for cy_ in cys:
                for e, e_ in zip(cy, cy_):
                    if e != e_:
                        res += 1
                        break
            if res == len(cys):
                return False
            return True
        unique_cycles = []
        for cycle in cycles:
            if cycle[0] == 0:
                cycle = cycle[:-1]
                if not isIncluded(cycle, unique_cycles):
                    unique_cycles.append(cycle)
            else:
                _0_index = cycle.index(0)
                cycle = cycle[_0_index:-1] + cycle[:_0_index]
                if not isIncluded(cycle, unique_cycles):
                    unique_cycles.append(cycle)
        return unique_cycles

    def get_path_with_IDs(self, path):
        path = list(map(lambda x: x.get_ID(), path))
        return path

    def get_Optimal_Path_with_IDs(self, method='ClarkeWright'):
        if method == 'ClarkeWright':
            paths, length = self.get_Optimal_ClarkeWrightPath()
        elif method == 'NearestNeighbor':
            paths, length = self.get_Optimal_NearestNeighborPath()
        paths = list(map(self.get_path_with_IDs, paths))
        return self.unique_cycles(paths), length

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
