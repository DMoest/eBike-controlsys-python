from asyncio.tasks import sleep
from firebase_admin import db
from db.db import Firebase
import time
import random
from app.bike import Bike

db_init = Firebase()

class BikeController:
    """
    Represents a group of persons running individual bike objects.
    """

    routes_by_city = {}

    def __init__(self, calculated_routes):
        self.routes_by_city = calculated_routes

    def reset_bike(self, bike):
        speed = random.randint(5, 20)
        should_reverse = random.randint(0, 1)
        route_idx = random.randint(0, len(self.routes_by_city["umea"]) - 1)
        points = self.routes_by_city["umea"][route_idx][speed]
        if should_reverse == 1:
            points.reverse()
        bike.reset_route(points)
            
    def run(self, num_bikes):
        """
        Runs specified number of bikes with random route and
        speed for every bike.
        """
        bikes = []
        
        for i in range(num_bikes):
            speed = random.randint(5, 20)
            should_reverse = random.randint(0, 1)
            route_idx = random.randint(0, len(self.routes_by_city["umea"]) - 1)
            points = self.routes_by_city["umea"][route_idx][speed]
            if should_reverse == 1:
                points.reverse()
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
        bike_objects = {}

        for bike in bikes:
            route_list.append(bike.get_route())

        longest_idx = max(route_list,key=len)

        for i in range(len(longest_idx)):
            bike.start
            for bike in bikes:
                pos = bike.get_position()
                id = bike.get_id()
                bike_objects["bike" + str(id)] = {
                    "id": id,
                    "lan": pos["lon2"],
                    "lat": pos["lat2"]
                }
                bike.move_bike()

            self.update_db(bike_objects)

            time.sleep(10)

    def update_db(self, bike_objects):
        ref = db.reference("/bikes/")
        ref.set(bike_objects)
