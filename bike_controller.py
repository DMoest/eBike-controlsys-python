from bike import Bike
from geographiclib.geodesic import Geodesic
import time
import math
import threading
import json

class BikeController:
    routes = []
    umeaBasePosition = (63.831550, 20.235777)
    

    def __init__(self):
        self.loadJson()

    def run(self):
        for route in self.routes:
            bike1 = Bike(1, 30)
            # self.start_bike(self.bike1)
            points = self.calculate_route(self.routes[0], bike1)
            self.start_bike(bike1, points)

    def calculate_route(self, route, bike):
        # define the WGS84 ellipsoid
        geod = Geodesic.WGS84
        points = []

        speed = bike.getSpeed()

        interval = speed * 0.277777778 # Interval for coordinates along the line between endpoints in meters.
        trip = route["route"]
        idx = 1
        print(len(trip))
        while idx <= len(trip) - 1:
            l = geod.InverseLine(trip[idx-1]["lat"], trip[idx-1]["long"], trip[idx]["lat"], trip[idx]["long"])
            step = int(math.ceil(l.s13 / interval)) # Step length is the total distance divided by the interval.
            print("init: " + str(trip[idx-1]) + " target: " + str(trip[idx]))
            for i in range(step + 1):
                s = min(interval * i, l.s13)
                points.append(l.Position(s, Geodesic.STANDARD | Geodesic.LONG_UNROLL))
            idx += 1
        
        return points

    def start_bike(self, bike, route):
        bike.start()
        for loc in route:
            self.moveBike(bike, loc)
            

    def moveBike(self, bike, loc):
        bike.set_position(loc)
        bike.printLocation()
        if not bike.isMoving:
            bike.stop()
            time.sleep(5)
            bike.start()
        time.sleep(1)        
        
    def loadJson(self):
        with open('routes.json') as fh:
            data = json.load(fh)
            for route in data:
                self.routes.append(route)


if __name__ == "__main__":
    contoller = BikeController()
    contoller.run()
