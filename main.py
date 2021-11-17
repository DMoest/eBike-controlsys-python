#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.customer import Customer
import utils.helpers as helpers
import sys
import random
from app.bike import Bike
from app.user import User
from multiprocessing import Process
import signal
import db.db
from collections import defaultdict
import json

# firebase = Firebase()
calculated_routes = helpers.calc_random_route_by_city("umea")
processes = []
bikes = []
umea_users = []
bikes_in_city = defaultdict(dict)

def signal_handler(sig, frame):
    for process in processes:
        process.terminate()
    sys.exit(0)

def init_bike(bike):    
    return Bike.create_from_json(bike)

def main():
    """
    Initializes and runs a new BikeController.
    """
    # NUM_BIKES = int(sys.argv[1])
    NUM_USERS = int(sys.argv[1])

    bikes_data = json.loads(db.db.getAllBikes())["bikes"]
    users_data = json.loads(db.db.getAllUsers()["users"])
    
    for user in users_data:
        if user["city"] == "Umeå":
            umea_users.append(User.create_from_json(user))

    for bike in bikes_data:
        if bike["city"] == "Umeå":
            bikes_in_city["Umeå"].setdefault("Umeå",[]).append(bike)
        # elif bike["city"] == "Stockholm":
        #     # bikes_in_city["stockhom"].append(bike)
        # elif bike["city"] == "Göteborg":
            # bikes_in_city["göteborg"].append(bike)

    for item in bikes_in_city["Umeå"]["Umeå"]:
        bike = init_bike(item)
        bikes.append(bike)

    if NUM_USERS > len(bikes):
        print("Maximum amount of customers are: " + str(len(bikes)))
        sys.exit(0)

        
    for i in range(len(bikes)):
        random_user_idx = random.randint(0, len(umea_users) - 1)
        user = umea_users.pop(random_user_idx)

        random_bike_idx = random.randint(0, len(bikes) - 1)
        bike = bikes.pop(random_bike_idx)

        customer = Customer(calculated_routes, user._id, bike, user)
        processes.append(Process(target=customer.run))

    for process in processes:
        process.start()

if __name__ == "__main__":
    main()
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()