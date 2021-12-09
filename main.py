#!/usr/bin/env python3

import sys
import signal
from multiprocessing import Process, cpu_count
from dependency_injector.wiring import Provide, inject
from app.customer import Customer
from app.customer_thread import CustomerThread
from services.bike_service import BikeService
from services.container import Container
from services.parking_service import ParkingService
from services.routes_service import RouteService
from services.user_service import UserService

# Fix to handle utf-8 input and output.
sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)
sys.stdin = open(1, 'w', encoding='utf-8', closefd=False)

customers = []
customer_threads = []

def signal_handler(sig, frame):
    """
    Terminate processes on exit signal.
    """
    sys.exit(0)

def split_to_chunks(a, n):
    """
    Splits array into n number of chunks.
    """
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def init_processes(NUM_USERS, user_service, bike_service, route_service):
    """
    Randomly pair up the given number of users with a randomly selected bike
    and start separate processes for each.
    """
    for i in range(NUM_USERS):
        if user_service.get_users_count() > 0:
            user = user_service.get_random_user()
            
        bike = bike_service.get_random_bike()
        customer = None

        if user.city == "Umeå":
            customer = Customer(route_service.get_routes_for_umea(), user._id, bike, user)
        elif user.city == "Stockholm":
            customer = Customer(route_service.get_routes_for_stockholm(), user._id, bike, user)
        elif user.city == "Göteborg":
            customer = Customer(route_service.get_routes_for_goteborg(), user._id, bike, user)

        customers.append(customer)

def start_customer(customer):
    """
    Starts a customer object.
    """
    try:
        customer.run()
    except KeyboardInterrupt:
        print("Killing process...")

def start_threds(customers):
    """
    Start a thread for the specified customer.
    """
    for customer in customers:
        thread = CustomerThread(customer)
        thread.start()
        customer_threads.append(thread)

@inject
def main(
    bike_service: BikeService = Provide[Container.bike_service],
    user_service: UserService = Provide[Container.user_service],
    route_service: RouteService = Provide[Container.routes_service]):

    """
    Main function to run the program with neccesary dependencies
    injected.
    """

    NUM_USERS = int(sys.argv[1])

    # Exit with status message if number of user exedes number of bikes.
    if NUM_USERS > bike_service.get_bikes_count():
        print("Maximum amount of customers are: " + str(bike_service.get_bikes_count()))
        sys.exit(0)

    init_processes(NUM_USERS, user_service, bike_service, route_service)

    # Split the customers array in a number of chunks according to the
    # cpu count.
    customer_chunks = split_to_chunks(customers, cpu_count())

    print("Simulation running...")

    # Start one process for each chunk of customers and run each customer
    # in a separate thread on that process.
    for chunk in customer_chunks:
        p = Process(target=start_threds, args=[chunk])
        p.start()

if __name__ == "__main__":
    # Wire dependencies.
    container = Container()
    container.wire(modules=[__name__])
    try:
        main()
    except KeyboardInterrupt:
        print("Exit...")
        
    signal.signal(signal.SIGINT, signal_handler)
