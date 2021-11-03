
class Bike():
    _id = None
    position = None
    _speed = None
    isMoving = False

    def __init__(self, id, speed):
        self._id = id
        self._speed = speed

    def start(self):
        print("starting bike with id: " + str(self._id))
        self.isMoving = True

    def stop(self):
        print("stopping bike with id: " + str(self._id))
        self.isMoving = False

    def getSpeed(self):
        return self._speed

    def set_position(self, position):
        self.position = position

    def printLocation(self):
            print ("{:s} {:.5f} {:.5f}".format(
                str(self._id), self.position['lat2'], self.position['lon2']))




