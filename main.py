from multiprocessing import Process
from bike_controller import BikeController
import sys

def main():
    """
    Initializes and runs a new BikeController.
    """
    NUM_BIKES = int(sys.argv[1])

    bike = BikeController()
    # number_of_bikes = int(input("Enter number of bikes to use in simulation: "))
    bike.run(NUM_BIKES)
        
if __name__ == "__main__":
    main()