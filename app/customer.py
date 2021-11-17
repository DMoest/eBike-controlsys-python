#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time

class Customer:
    """
    Represents a group of persons running individual bike objects.
    """

    routes_by_city = {}
    _id = None
    bike = None
    user = None
    route = None
    route_idx = 0

    def __init__(self, calculated_routes, id, bike, user):
        self.routes_by_city = calculated_routes
        self._id = id
        self.bike = bike
        self.user = user
        speed = random.randint(5, 20)
        should_reverse = random.randint(0, 1)
        self.route_idx = random.randint(0, len(self.routes_by_city[self.user.city]) - 2)
        self.route = self.routes_by_city[self.user.city][self.route_idx][speed]
        if should_reverse == 1:
            self.route.reverse()
            
    def run(self):
        """
        Runs specified number of bikes with random route and
        speed for every bike.
        """
        self.bike.start()

        self.start_bike(self.bike)

    def start_bike(self, bike):
        """
        Starts all bikes and bulk updates their position according
        to respective route every second.
        """

        parkings = self.routes_by_city[self.user.city]["parkings"]

        for location in self.route:
            if bike._is_parking:
                if bike.check_in_parking_area(parkings):
                    bike.stop()
                    if bike._power_level <= 25:
                        print("Charging")
                        bike.charge_bike()
                        time.sleep(20)
                        bike._power_level = 100
                    break
            bike.move_bike(location)
            time.sleep(10)
        #bike.check_in_parking_area(self.routes_by_city["parkings"])
