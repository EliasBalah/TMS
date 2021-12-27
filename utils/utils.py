import math
import requests
import folium


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
    pass
    # cycle = list(map(lambda x: x.get_ID(), cycle))
    # return cycle


def identify_cycles(cycles):
    pass
    # cycles = list(map(lambda x: identify_cycle(x), cycles))
    # return cycles


def get_route_length(origin, destination, distance='euclidean'):
    if distance == 'euclidean':
        return get_air_distance(origin, destination)
    elif distance == 'google_map':
        return None
    elif distance == 'graph_hopper':
        return get_graphhopper_distance(origin, destination)
    return None


def get_air_distance(origin, destination):
    earth_radius = 6371000
    phi_1, lambda_1 = map(lambda x: x*math.pi/180,
                          origin.get_coordinates())
    phi_2, lambda_2 = map(lambda x: x*math.pi/180,
                          destination.get_coordinates())
    distance_cart = (2 - math.cos(phi_1 + phi_2)*(math.cos(lambda_1 - lambda_2) - 1) -
                     math.cos(phi_1 - phi_2)*(math.cos(lambda_1 - lambda_2) + 1))**(1/2)
    distance = 2*earth_radius*math.asin(distance_cart/2)
    return distance


def get_graphhopper_distance(origin, destination):
    api_key = '6ae3932f-cd53-48dc-bb67-4f1fc7ec11c3'
    origins_string = ','.join(map(lambda x: str(x), origin.get_coordinates()))
    destinations_string = ','.join(
        map(lambda x: str(x), destination.get_coordinates()))
    url = f"https://graphhopper.com/api/1/route?point={origins_string}&point={destinations_string}&profile=car&locale=de&calc_points=false&key={api_key}"
    payload = {}
    headers = {}
    response = requests.request(
        "GET", url, headers=headers, data=payload).json()
    return response['paths'][0]['distance']


def visualize_cycle(cycle: list):

    cycle = list(map(lambda x: x.get_coordinates(), cycle))
    print(cycle)

    midpoint = sum(list(map(lambda x: x[0], cycle)))/len(
        cycle), sum(list(map(lambda x: x[1], cycle)))/len(cycle)

    _map = folium.Map(location=midpoint, zoom_start=4)
    depot_node = cycle[0]
    depot_icon = folium.Icon(color='red')
    folium.Marker(
        depot_node, popup=f"Depot: ({depot_node[0]}, {depot_node[1]})", icon=depot_icon).add_to(_map)
    for order, customer_node in enumerate(cycle[1:-1], start=1):
        folium.Marker(
            customer_node, popup=f"Customer {order}: ({customer_node[0]}, {customer_node[1]})").add_to(_map)
    folium.PolyLine(cycle).add_to(_map)
    return _map
