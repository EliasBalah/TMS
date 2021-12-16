def unique_cycles(cycles):
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


def identify_cycle(cycle):
    cycle = list(map(lambda x: x.get_ID(), cycle))
    return cycle


def identify_cycles(cycles):
    cycles = list(map(lambda x: identify_cycle(x), cycles))
    return cycles
