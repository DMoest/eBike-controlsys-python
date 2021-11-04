from multiprocessing import Process
from bike_controller import BikeController
import asyncio

def main():
    bike = BikeController()
    number_of_bikes = int(input("Enter number of bikes to use in simulation: "))
    bike.run(number_of_bikes)
        
if __name__ == "__main__":
    main()