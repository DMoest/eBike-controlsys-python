import utils.helpers as helpers
import sys
import random
from app.bike import Bike
from multiprocessing import Process
import signal
from db.db import Firebase

firebase = Firebase()
calculated_routes = helpers.calc_random_route_by_city("umea")
processes = []

def signal_handler(sig, frame):
    for process in processes:
        process.join()
    sys.exit(0)

def init_bike(id):
    speed = random.randint(5, 20)
    should_reverse = random.randint(0, 1)
    route_idx = random.randint(0, len(calculated_routes["umea"]) - 1)
    points = calculated_routes["umea"][route_idx][speed]
    if should_reverse == 1:
        points.reverse()
    return Bike(id, speed, points)

def main():
    """
    Initializes and runs a new BikeController.
    """
    NUM_BIKES = int(sys.argv[1])

    for i in range(NUM_BIKES):
        bike = init_bike(i)  
        bike.start()
        processes.append(Process(target=bike.move_bike))

    for process in processes:
        process.start()
            
        
if __name__ == "__main__":
    main()
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()