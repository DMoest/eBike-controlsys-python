#!/usr/bin/env python3

import random
import time
import os

class Customer:
    """
    Represents a group of persons running individual bike objects.
    """

    routes_by_city = {}
    _id = None
    _pid = None
    bike = None
    user = None
    route = None
    route_idx = 0

    def __init__(self, calculated_routes, id, bike, user):
        self.routes_by_city = calculated_routes
        self._id = id
        self._pid = os.getpid()
        self.bike = bike
        self.user = user
        speed = random.randint(5, 20)
        should_reverse = random.randint(0, 1)
        self.route_idx = random.randint(0, len(self.routes_by_city[self.user.city]) - 2)
        self.route = self.routes_by_city[self.user.city][self.route_idx][speed]
        if should_reverse == 1:
            self.route.reverse()

    def get_pid(self):
        return self._pid

    def get_user(self):
        return self.user

    def get_bike(self):
        return self.bike
            
    def run(self):
        """
        Runs specified bike along route.
        """
        delay = random.randint(0, 300)
        time.sleep(delay)
        self.bike.move_bike(self.route[0])
        self.bike.start(self.user)

        self.start_bike(self.bike)

    def start_bike(self, bike):
        """
        Starts the bike and updates its position according
        to route every 10 seconds.
        """

        for location in self.route:
            if bike._active:
                bike.move_bike(location)
                time.sleep(10)
        
        bike.stop()
