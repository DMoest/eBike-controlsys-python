from multiprocessing import Process
from bike_controller import BikeController

def main():
    """
    Initializes and runs a new BikeController.
    """
    bike = BikeController()
    number_of_bikes = int(input("Enter number of bikes to use in simulation: "))
    bike.run(number_of_bikes)
        
if __name__ == "__main__":
    main()