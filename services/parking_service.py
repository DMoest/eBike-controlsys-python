#!/usr/bin/env python3
import db.db
from app.parking import Parking

class ParkingService():
    parkings_umeå = []
    parkings_stockholm = []
    parkings_göteborg = []

    def __init__(self, api: db.db.Api):
        parkings_data = api.getAllParkings()["parking_zones"]
        print(parkings_data)
        self.init_parkings(parkings_data)

    def init_parkings(self, parkings_data):
        """
        Initializes user objects for each city.
        """
        for parking in parkings_data:
            if parking["city"] == "Umeå":
                self.parkings_umeå.append(Parking.create_from_json(parking))
            elif parking["city"] == "Stockholm":
                self.parkings_stockholm.append(Parking.create_from_json(parking))
            elif parking["city"] == "Göteborg":
                self.parkings_göteborg.append(Parking.create_from_json(parking))

    def get_parkings_for_city(self, city):
        if city == "Umeå":
            return self.parkings_umeå
        elif city == "Stockholm":
            return self.parkings_stockholm
        elif city == "Göteborg":
            return self.parkings_göteborg 

    