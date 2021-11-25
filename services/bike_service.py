#!/usr/bin/env python3

import sys
import random
from collections import defaultdict
import db.db
from app.bike import Bike

class BikeService():
    bikes = []
    bikes_in_city = defaultdict(dict)

    def __init__(self):
        bikes_data = db.db.getAllBikes()["bikes"]
        NUM_USERS = int(sys.argv[1])

        self.init_bikes(bikes_data)

    def init_bike(self, bike):
        """
        Initializes new Bike object.
        """  
        return Bike.create_from_json(bike)

    def init_bikes(self, bikes_data):
        """
        Initializes bike objects for each city.
        """
        for bike in bikes_data:
            if bike["city"] == "Umeå":
                self.bikes_in_city["Umeå"].setdefault("Umeå",[]).append(bike)
            elif bike["city"] == "Stockholm":
                self.bikes_in_city["Stockholm"].setdefault("Stockholm",[]).append(bike)
            elif bike["city"] == "Göteborg":
                self.bikes_in_city["Göteborg"].setdefault("Göteborg",[]).append(bike)

        for item in self.bikes_in_city["Umeå"]["Umeå"]:
            bike = self.init_bike(item)
            self.bikes.append(bike)

        for item in self.bikes_in_city["Stockholm"]["Stockholm"]:
            bike = self.init_bike(item)
            self.bikes.append(bike)

        for item in self.bikes_in_city["Göteborg"]["Göteborg"]:
            bike = self.init_bike(item)
            self.bikes.append(bike)

    def get_random_bike(self):
        random_bike_idx = random.randint(0, len(self.bikes) - 1)
        bike = self.bikes.pop(random_bike_idx)
        return bike

    def get_bikes_count(self):
        return len(self.bikes)
