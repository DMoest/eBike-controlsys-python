from firebase_admin import db
from db.db import Firebase
import random
from app.bike import Bike

class Customer:
    """
    Represents a group of persons running individual bike objects.
    """

    routes_by_city = {}
    _id = None
    bikes = None

    def __init__(self, calculated_routes, id, bikes):
        self.routes_by_city = calculated_routes
        self._id = id
        self.bikes = bikes

    def reset_bike(self, bike):
        speed = random.randint(5, 20)
        should_reverse = random.randint(0, 1)
        route_idx = random.randint(0, len(self.routes_by_city["umea"]) - 1)
        points = self.routes_by_city["umea"][route_idx][speed]
        if should_reverse == 1:
            points.reverse()
        bike.reset_route(points)
            
    def run(self):
        """
        Runs specified number of bikes with random route and
        speed for every bike.
        """
        speed = random.randint(5, 20)
        should_reverse = random.randint(0, 1)
        route_idx = random.randint(0, len(self.routes_by_city["umea"]) - 1)
        self.route = self.routes_by_city["umea"][route_idx][speed]
        if should_reverse == 1:
            self.route.reverse()

        bike_idx = random.randint(0, len(self.bikes) - 1)
        bike = self.bikes[bike_idx]
        bike.start()

        self.start_bike(bike)

    def start_bike(self, bike):
        """
        Starts all bikes and bulk updates their position according
        to respective route every second.
        """

        bike.move_bike()
        #bike.check_in_parking_area(self.routes_by_city["parkings"])

    def update_db(self, bike_objects):
        ref = db.reference("/bikes/")
        ref.set(bike_objects)
