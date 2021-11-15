import requests
import threading

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

    def __init__(self, id, speed, city, status, active, position):
        self._id = id
        self._speed = speed,
        self._city = city,
        self._status = status,
        self._active = active
        self._position = position

    def start(self):
        self._active = True
        self.update_db()

    def stop(self):
        self._active = False

    def get_id(self):
        return self._id

    def getSpeed(self):
        return self._speed

    def set_position(self, position):
        self._position = position
    
    def get_position(self):
        return self._position

    def check_in_parking_area(self, parkings):
        self._parking_approved = False
        for parking in (parkings):
            if parking[1]["lat"] < self.position["lat2"] < parking[0]["lat"] and\
                parking[1]["long"] < self.position["lon2"] < parking[0]["long"]:
                self._parking_approved = True
                break

    def move_bike(self, location):
        """
        Moves a bike object to a new location.
        """
        self._position = location

    def update_db(self):
        print(str(self._id) + " " + str(self._position["lat2"]) + " " + str(self._position["lon2"]))

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
        # ref = db.reference("/bikes/" + str(self._id))
        # ref.set({
        #     "id": self._id,
        #     "lat": self.position["lat2"],
        #     "long": self.position["lon2"]
        # })
