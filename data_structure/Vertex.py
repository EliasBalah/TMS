class Vertex:
    
    def __init__(self, ID) -> None:
        self.__ID = ID
        self.__neighbors = []

    def add_neighbor(self, neighbor, distance) -> int:
        for s_neighbor, _ in self.__neighbors:
            if s_neighbor.get_ID() == neighbor.get_ID(): return 0
        self.__neighbors.append((neighbor, distance))
        return 1
        
    def get_neighbors(self) -> list:
        return self.__neighbors
        
    def get_neighbor_distance(self, neighbor):
        for s_neighbor, s_distance in self.__neighbors:
            if s_neighbor.get_ID() == neighbor.get_ID(): return s_distance
        return 0

    def get_nearest_neighbor(self, exclude=[]):
        nearest_neighbors = []
        nearest_neighbors_distance = float("inf")
        for (s_neighbor, s_distance) in self.__neighbors:
            if s_neighbor in exclude: continue
            if s_distance < nearest_neighbors_distance:
                nearest_neighbors = [s_neighbor]
                nearest_neighbors_distance = s_distance
            elif s_distance == nearest_neighbors_distance:
                nearest_neighbors.append(s_neighbor)
        return (nearest_neighbors, nearest_neighbors_distance)

    def get_ID(self) -> int:
        return self.__ID
        
