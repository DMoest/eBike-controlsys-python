#!/usr/bin/env python3

import sys
import random
from collections import defaultdict
import db.db
from app.bike import Bike
from services.parking_service import ParkingService

class BikeService():
    bikes = []
    bikes_in_city = defaultdict(dict)
    parkings = None

    def __init__(self, api: db.db.Api, parkings: ParkingService):
        bikes_data = api.getAllBikes()["bikes"]
        NUM_USERS = int(sys.argv[1])
        self.parkings = parkings.parkings_umeå
        print(bikes_data)
        self.init_bikes(bikes_data)

    def init_bike(self, bike):
        """
        Initializes new Bike object.
        """
        park = self.parkings
        return Bike.create_from_json(bike, park)

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
        
        if "Umeå" in self.bikes_in_city:
            for item in self.bikes_in_city["Umeå"]["Umeå"]:
                bike = self.init_bike(item)
                self.bikes.append(bike)

        if "Stockholm" in self.bikes_in_city:
            for item in self.bikes_in_city["Stockholm"]["Stockholm"]:
                bike = self.init_bike(item)
                self.bikes.append(bike)
        
        if "Göteborg" in self.bikes_in_city:
            for item in self.bikes_in_city["Göteborg"]["Göteborg"]:
                bike = self.init_bike(item)
                self.bikes.append(bike)

    def get_random_bike(self):
        random_bike_idx = random.randint(0, len(self.bikes) - 1)
        bike = self.bikes.pop(random_bike_idx)
        return bike

    def get_bikes_count(self):
        return len(self.bikes)
