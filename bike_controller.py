from asyncio.tasks import sleep
from bike import Bike
import helpers
import time
import random

class BikeController:
    """
    Represents a group of persons running individual bike objects.
    """

    routes_by_city = {}

    def __init__(self):
        # Load all predefined routes by city from JSON.
        helpers.loadJson()

    def reset_bike(self, bike):
        speed = random.randint(5, 20)
        bike.reset_route(helpers.calc_random_route_by_city("umea"), speed)

    def run(self, num_bikes):
        """
        Runs specified number of bikes with random route and
        speed for every bike.
        """
        bikes = []
        print("Calculating routes...")
        
        for i in range(num_bikes):
            speed = random.randint(5, 20)
            points = helpers.calc_random_route_by_city("umea", speed)
            bike = Bike(i, speed, points)
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
