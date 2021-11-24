#!/usr/bin/env python3

import sys
import os
import random
import signal
from collections import defaultdict
from multiprocessing import Process, Pool, Manager
from app.bike import Bike
from app.user import User
from app.customer import Customer
import utils.helpers as helpers
import db.db


# Fix to handle utf-8 input and output.
sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)
sys.stdin = open(1, 'w', encoding='utf-8', closefd=False)

umea_calculated_routes = helpers.calc_random_route_by_city("Umeå")
stockholm_calculated_routes = helpers.calc_random_route_by_city("Stockholm")
customers = []
bikes = []
users = []
bikes_in_city = defaultdict(dict)

def signal_handler(sig, frame):
    """
    Terminate processes on exit signal.
    """
    sys.exit(0)

def init_bike(bike):
    """
    Initializes new Bike object.
    """  
    return Bike.create_from_json(bike)

def init_users(users_data):
    """
    Initializes user objects for each city.
    """
    for user in users_data:
        if user["city"] == "Umeå":
            users.append(User.create_from_json(user))
        elif user["city"] == "Stockholm":
            users.append(User.create_from_json(user))

def get_random_user():
    random_user_idx = random.randint(0, len(users) - 1)
    user = users.pop(random_user_idx)
    return user

def get_random_bike():
    random_bike_idx = random.randint(0, len(bikes) - 1)
    bike = bikes.pop(random_bike_idx)
    return bike


def init_bikes(bikes_data):
    """
    Initializes bike objects for each city.
    """
    for bike in bikes_data:
        if bike["city"] == "Umeå":
            bikes_in_city["Umeå"].setdefault("Umeå",[]).append(bike)
        elif bike["city"] == "Stockholm":
            bikes_in_city["Stockholm"].setdefault("Stockholm",[]).append(bike)
        # elif bike["city"] == "Göteborg":
            # bikes_in_city["göteborg"].append(bike)

    for item in bikes_in_city["Umeå"]["Umeå"]:
        bike = init_bike(item)
        bikes.append(bike)

    for item in bikes_in_city["Stockholm"]["Stockholm"]:
        bike = init_bike(item)
        bikes.append(bike)

def init_processes(NUM_USERS):
    """
    Randomly pair up the given number of users with a randomly selected bike
    and start separate processes for each.
    """
    for i in range(NUM_USERS):
        print("users: " + str(len(users)))
        if len(users) > 0:
            user = get_random_user()
            
        bike = get_random_bike()

        customer = None
        if user.city == "Umeå":
            customer = Customer(umea_calculated_routes, user._id, bike, user)
        elif user.city == "Stockholm":
            customer = Customer(stockholm_calculated_routes, user._id, bike, user)

        customers.append(customer)
        # process = Process(target=customer.run) 
        # processes.append(process)

def start_customer(customer):
    customer.run()

def main():
    NUM_USERS = int(sys.argv[1])

    bikes_data = db.db.getAllBikes()["bikes"]
    users_data = db.db.getAllUsers()["users"]

    init_users(users_data)
    init_bikes(bikes_data)

    # Exit with status message if number of user exedes number of bikes.
    if NUM_USERS > len(bikes):
        print("Maximum amount of customers are: " + str(len(bikes)))
        sys.exit(0)

    init_processes(NUM_USERS)

    # Start processes.
    p = Pool(NUM_USERS)
    p.map(start_customer, customers)


if __name__ == "__main__":
    main()
    signal.signal(signal.SIGINT, signal_handler)
