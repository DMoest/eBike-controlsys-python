import threading
from firebase_admin import db
from threading import Timer

class Bike():
    """
    Represents an individual bike object.
    """
    _id = None
    position = None #Current lat/long position.
    _speed = None #Current speed in km/h.
    isMoving = False #Is the bike currently moving?
    route = None #The route calculated for this bike.
    route_index = 0
    parking_approved = False

    def __init__(self, id, speed):
        self._id = id
        self._speed = speed

    def start(self, route):
        self.route = route
        self.position = route[0]
        self.isMoving = True
        self.update_db()

    def stop(self):
        self.isMoving = False

    def get_id(self):
        return self._id

    def getSpeed(self):
        return self._speed

    def set_position(self, position):
        self.position = position
    
    def get_position(self):
        return self.route[self.route_index]

    def get_route(self):
        return self.route

    def get_route_index(self):
        return self.route_index

    def reset_route(self, route):
        self.route_index = 0
        self.route = route

    def check_in_parking_area(self, parkings):
        self.parking_approved = False
        for parking in (parkings):
            if parking[1]["lat"] < self.position["lat2"] < parking[0]["lat"] and\
                parking[1]["long"] < self.position["lon2"] < parking[0]["long"]:
                self.parking_approved = True
                break

    def move_bike(self, location):
        """
        Moves a bike object to a new location.
        """
        self.position = location
        print(str(self._id) + " " + str(self.position["lat2"]) + " " + str(self.position["lon2"]))

    def update_db(self):
        ref = db.reference("/bikes/" + str(self._id))
        ref.set({
            "id": self._id,
            "lat": self.position["lat2"],
            "long": self.position["lon2"]
        })
        t = threading.Timer(30, self.update_db)
        t.start()
