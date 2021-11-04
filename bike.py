import helpers
import random

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

    def __init__(self, id, speed, route):
        self._id = id
        self._speed = speed
        self.route = route

    def start(self):
        self.isMoving = True

    def stop(self):
        self.isMoving = False

    def getSpeed(self):
        return self._speed

    def set_position(self, position):
        self.position = position

    def get_route(self):
        return self.route

    def get_route_index(self):
        return self.route_index

    def reset_route(self, route):
        self.route_index = 0
        self.route = route

    def move_bike(self):
        """
        Moves a bike object to a new location.
        """
        self.route_index += 1
        if self.route_index == len(self.route):
            self.printLocation()
            speed = random.randint(5, 20)
            new_route = helpers.calc_random_route_by_city("umea", speed)
            self.reset_route(new_route)
        else:
            self.position = self.route[self.route_index]
            self.printLocation()

    def printLocation(self):
        """
        Prints current latitude and longitude of the bike.
        """
        print ("{:s} {:.5f} {:.5f}".format(
            str(self._id), self.position['lat2'], self.position['lon2']))




