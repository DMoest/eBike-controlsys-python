
class Bike():
    _id = None
    position = None
    _speed = None
    isMoving = False
    route = None

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

    def printLocation(self):
            print ("{:s} {:.5f} {:.5f}".format(
                str(self._id), self.position['lat2'], self.position['lon2']))




