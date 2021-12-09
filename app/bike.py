#!/usr/bin/env python3

import requests
import threading
import random

class Bike():
    """
    Represents an individual bike object.
    """
    _id = None
    _city = None
    _status = None
    _position = None #Current lat/long position.
    _speed = None #Current speed in km/h.
    _active = False #Is the bike currently moving?
    _parking_approved = False
    _power_level = 0
    _is_parking = False
    _is_charging = False
    _user = None
    _parkings = None

    def __init__(self, id, speed, city, status, active, position, power_level, parkings):
        self._id = id
        self._speed = speed
        self._city = city
        self._status = status
        self._active = active
        self._position = position
        self._power_level = power_level
        self._parkings = parkings

    def start(self, user):
        """
        Start the bike and update database.
        """
        self._active = True
        self._user = user
        self.start_trip()
        self.update_db()

    def stop(self):
        """
        Stop the bike and update database.
        """
        self._active = False
        self.update_db()
        self.end_trip()

    def check_in_parking_area(self):
        """
        Determine if the bike is within any of the approved parking
        areas supplied.
        """
        withinParking = False

        # 0 represents latitude and 1 longitude
        if self._parkings[0].sw[0] < self._position["lat2"] < self._parkings[0].ne[0] and\
            self._parkings[0].sw[1] < self._position["lon2"] < self._parkings[0].ne[1]:
            self._parking_approved = True
            withinParking = True
        return withinParking
        

    def move_bike(self, location):
        """
        Moves a bike object to a new location.
        """
        self._position = location
        self._power_level -= 0.5
        if self._power_level <= 0:
            self.stop()

        # Stop bike if powerlevel is low and within parking area.
        if self._power_level < 25:
            parking_idx = self.check_in_parking_area()
            if parking_idx:
                print("Stopping in parking area: " + str(parking_idx))
                self.stop()

    def charge_bike(self):
        self._is_charging = True

    def update_db(self):
        """
        Send request to api to update the bikes info.
        """
        requests.put('http://ebike_backend:8000/api/bike', data ={
            '_id': self._id,
            'city': self._city,
            'status': self._status,
            'active': self._active,
            'longitude': self._position["lon2"],
            'latitude': self._position["lat2"],
            'speed': self._speed,
            'battery': self._power_level
        })
        t = threading.Timer(35, self.update_db)
        t.start()

    def start_trip(self):
        requests.post('http://ebike_backend:8000/api/travel', data ={
            'city': self._city,
            'user_id': self._user._id,
            'bike_id': self._id,
            'status': self._status,
            'start_longitude': self._position["lon2"],
            'start_latitude': self._position["lat2"],
            'price': 0
        })

    def end_trip(self):
        requests.put('http://ebike_backend:8000/api/travel', data ={
            'city': self._city,
            'user_id': self._user._id,
            'bike_id': self._id,
            'status': self._status,
            'stop_longitude': self._position["lon2"],
            'stop_latitude': self._position["lat2"],
        })
        

    @classmethod
    def create_from_json(cls, json_data, parkings):
        """
        Factory method to create a bike object from JSON.
        """
        speed = random.randint(5, 20)
        power = random.randint(25, 100)

        return cls(
            json_data["_id"],
            speed,
            json_data["city"],
            json_data["status"],
            json_data["active"],
            {"lat2": json_data["latitude"], "lon2": json_data["longitude"]},
            power,
            parkings)
