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

    def __init__(self, id, speed, city, status, active, position, power_level):
        self._id = id
        self._speed = speed
        self._city = city
        self._status = status
        self._active = active
        self._position = position
        self._power_level = power_level

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
        self.end_trip()
        self.update_db()

    def check_in_parking_area(self, parkings):
        """
        Determine if the bike is within any of the approved parking
        areas supplied.
        """
        self._parking_approved = False
        for parking in (parkings):
            if parking[1]["lat"] < self._position["lat2"] < parking[0]["lat"] and\
                parking[1]["long"] < self._position["lon2"] < parking[0]["long"]:
                self._parking_approved = True
                break

    def move_bike(self, location):
        """
        Moves a bike object to a new location.
        """
        self._position = location
        self._power_level -= 0.5
        if self._power_level <= 25:
            self._is_parking = True

        if self._power_level == 0:
            self.stop()

    def charge_bike(self):
        self._is_charging = True

    def update_db(self):
        """
        Send request to api to update the bikes info.
        """
        print(str(self._id) + " Powerlevel: " + str(self._power_level) + " Looking for parking: " + str(self._is_parking) + " Parked: " + str(self._parking_approved) + " Charging: " + str(self._is_charging))

        requests.put('http://ebike_backend:8000/api/bike', data ={
            '_id': self._id,
            'city': self._city,
            'status': self._status,
            'active': self._active,
            'longitude': self._position["lon2"],
            'latitude': self._position["lat2"]
        })
        t = threading.Timer(30, self.update_db)
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
    def create_from_json(cls, json_data):
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
            power)
