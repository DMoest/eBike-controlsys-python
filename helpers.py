from geographiclib.geodesic import Geodesic
import math
import json
import random
def calculate_route(route, speed):
    """
    Calculates intermedate points betwen the endpoints given
    in de supplied route.
    """
    # define the WGS84 ellipsoid
    geod = Geodesic.WGS84
    points = []

    interval = speed * 0.277777778 # Interval for coordinates along the line between endpoints in meters.
    trip = route["route"]
    idx = 1
    while idx <= len(trip) - 1:
        l = geod.InverseLine(trip[idx-1]["lat"], trip[idx-1]["long"], trip[idx]["lat"], trip[idx]["long"])
        step = int(math.ceil(l.s13 / interval)) # Step length is the total distance divided by the interval.
        for i in range(step + 1):
            s = min(interval * i, l.s13)
            points.append(l.Position(s, Geodesic.STANDARD | Geodesic.LONG_UNROLL))
        idx += 1
    
    return points

def loadJson():
    """
    Loads the predefined routes from routes.json.
    """
    cities_with_routes = {}

    with open('routes.json') as fh:
        data = json.load(fh)
        cities = data[0]["cities"]

        for key in cities.keys():
            cities_with_routes[key] = cities[key]

        return cities_with_routes

def calc_random_route_by_city(city, speed):
    """
    Gets a random route from the specified city and returns calculated
    intermediate points for the route.
    """
    speed = random.randint(5, 20)

    routes_by_city = loadJson()
    route_idx = random.randint(0, len(routes_by_city.get("umea")) - 1)
    route = routes_by_city.get(city)[route_idx]
    points = calculate_route(route, speed)
    return points
