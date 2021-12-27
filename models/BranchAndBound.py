from data_structure import Graph


class BranchAndBound:
    # Data must be a graph (Graph object)
    def __init__(self) -> None:
        self.__data: Graph = None
        self._upper_bound = None
        self._lower_bound = None
        self._solution = []

    def _update_data(self, data) -> None:
        if not isinstance(data, Graph):
            raise TypeError(
                f"The model must be fitted with Graph object!")
        else:
            self.__data = data

    def _update_upper_bound(self, upper_bound) -> None:
        if upper_bound:
            self._upper_bound = upper_bound
        else:
            self._upper_bound = self.__data.vertices_count() * \
                self.__data.bounds()[1]

    def _update_lower_bound(self, lower_bound) -> None:
        if lower_bound:
            self._lower_bound = lower_bound
        else:
            self._lower_bound = self.__data.vertices_count() * \
                self.__data.bounds()[0]

    def _get_optimal_path(self, vertex, path_length, visited_vertices) -> None:

        if path_length > self._upper_bound:
            return
        if len(visited_vertices) == self.__data.vertices_count():
            cycle_length = path_length + \
                self.__data.get_distance(
                    visited_vertices[0], vertex) - self.__data.bounds()[0]
            if cycle_length == self._upper_bound:
                self._solution.append(visited_vertices + [visited_vertices[0]])
                return
            if cycle_length < self._upper_bound:
                self._solution = [visited_vertices + [visited_vertices[0]]]
                self._upper_bound = cycle_length
                return

        for neighbor, neighbor_distance in vertex.get_neighbors():
            if neighbor in visited_vertices:
                continue
            distance_minus_min = neighbor_distance - self.__data.bounds()[0]
            self._get_optimal_path(vertex=neighbor,  path_length=path_length +
                                   distance_minus_min, visited_vertices=visited_vertices + [neighbor])

        return

    def _optimize(self, start_vertex=None):
        if not start_vertex:
            start_vertex = self.__data.get_vertices()[0]
        self._get_optimal_path(
            vertex=start_vertex, path_length=self._lower_bound, visited_vertices=[start_vertex])
        return self._solution, self._upper_bound

    def fit(self, data, upper_bound=None, lower_bound=None) -> None:
        self._update_data(data)
        self._update_upper_bound(upper_bound)
        self._update_lower_bound(lower_bound)
