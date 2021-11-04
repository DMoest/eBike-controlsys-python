from asyncio.tasks import sleep
from bike import Bike
from geographiclib.geodesic import Geodesic
import time
import math
import json
import random

class BikeController:
    routes = []

    def __init__(self):
        self.loadJson()

    def run(self, num_bikes):
        bikes = []
        print("Calculating routes...")
        
        for i in range(num_bikes):
            speed = random.randint(5, 20)
            route_idx = random.randint(0, len(self.routes[0]["cities"]["umea"]) - 1)
            route = self.routes[0]["cities"]["umea"][route_idx]
            points = self.calculate_route(route, speed)
            bike = Bike(i, speed, points)
            bike.start()
            bikes.append(bike)

        self.start_bike(bikes) 

    def calculate_route(self, route, speed):
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

    def start_bike(self, bikes):
        route_list = []
        for bike in bikes:
            route_list.append(bike.get_route())

        longest_idx = max(route_list,key=len)

        for i in range(len(longest_idx)):
            bike.start
            for bike in bikes:
                route = bike.get_route()
                if route[i]:
                    self.moveBike(bike, route[i])
            time.sleep(1)
            

    def moveBike(self, bike, loc):
        bike.set_position(loc)
        bike.printLocation()
        if not bike.isMoving:
            bike.stop()
            time.sleep(5)
            bike.start()
        
    def loadJson(self):
        with open('routes.json') as fh:
            data = json.load(fh)
            for route in data:
                self.routes.append(route)
