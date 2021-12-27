from utils.utils import get_route_length


class Vertex:

    def __init__(self, latitude, longitude, value) -> None:
        self.__latitude = latitude
        self.__longitude = longitude
        self.__value = value
        self.__neighbors = []

    def get_coordinates(self):
        return self.__latitude, self.__longitude

    def get_value(self):
        return self.__value

    def update_value(self, new_value):
        self.__value = new_value

    def get_neighbors(self):
        return self.__neighbors

    def get_last_neighbor_added(self):
        if self.__neighbors:
            return self.__neighbors[-1]

    def add_neighbor(self, neighbor):
        distance = get_route_length(
            origin=self, destination=neighbor, distance='graph_hopper')
        self.__neighbors.append((neighbor, distance))

    def get_nearest_neighbor(self, exclude=[]):
        nearest_neighbors = []
        nearest_neighbors_distance = float("inf")
        for (s_neighbor, s_distance) in self.__neighbors:
            if s_neighbor in exclude:
                continue
            if s_distance < nearest_neighbors_distance:
                nearest_neighbors = [s_neighbor]
                nearest_neighbors_distance = s_distance
            elif s_distance == nearest_neighbors_distance:
                nearest_neighbors.append(s_neighbor)
        return (nearest_neighbors, nearest_neighbors_distance)
