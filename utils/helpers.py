#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geographiclib.geodesic import Geodesic
import math
import json

def calculate_route(route, speed):
    """
    Calculates intermedate points betwen the endpoints given
    in de supplied route.
    """
    # define the WGS84 ellipsoid
    geod = Geodesic.WGS84
    points = []

    interval = (speed * 0.277777778) * 10 # Interval for coordinates along the line between endpoints in meters.
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

    with open('routes.json', encoding='utf-8') as fh:
        data = json.load(fh)
        cities = data[0]["cities"]

        for key in cities.keys():
            cities_with_routes[key] = cities[key]

        return cities_with_routes

def calc_random_route_by_city(city):
    """
    Gets a random route from the specified city and returns calculated
    intermediate points for the route.
    """
    base_routes = loadJson()
    calculated_routes = {}

    for city in base_routes.keys():
        calculated_routes[city] = {}
        calculated_routes[city]["parkings"] = base_routes[city]["parkings"]
        for i, route in enumerate(base_routes[city]["routes"]):
            calculated_routes[city][i] = {}
            for speed in range(5, 25):
                calculated_routes[city][i][speed] = calculate_route(route, speed)
    
    return calculated_routes
