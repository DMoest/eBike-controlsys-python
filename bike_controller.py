from asyncio.tasks import sleep
import time
import random
from bike import Bike
from db import Firebase
import helpers

db = Firebase()

class BikeController:
    """
    Represents a group of persons running individual bike objects.
    """

    routes_by_city = {}

    def __init__(self, calculated_routes):
        self.routes_by_city = calculated_routes

    def reset_bike(self, bike):
        speed = random.randint(5, 20)
        route_idx = random.randint(0, len(self.routes_by_city["umea"]) - 1)
        points = self.routes_by_city["umea"][route_idx][speed]
        bike.reset_route(points)

    def run(self, num_bikes):
        """
        Runs specified number of bikes with random route and
        speed for every bike.
        """
        bikes = []
        
        for i in range(num_bikes):
            speed = random.randint(5, 20)
            route_idx = random.randint(0, len(self.routes_by_city["umea"]) - 1)
            points = self.routes_by_city["umea"][route_idx][speed]
            bike = Bike(i, speed, points, db)
            bike.start()
            bikes.append(bike)

        self.start_bike(bikes) 

    def start_bike(self, bikes):
        """
        Starts all bikes and bulk updates their position according
        to respective route every second.
        """
        route_list = []
        for bike in bikes:
            route_list.append(bike.get_route())

        longest_idx = max(route_list,key=len)

        for i in range(len(longest_idx)):
            bike.start
            for bike in bikes:
                bike.move_bike()
            time.sleep(1)           
