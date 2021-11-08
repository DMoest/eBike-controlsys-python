from app.bike_controller import BikeController
import utils.helpers as helpers
import sys

def main():
    """
    Initializes and runs a new BikeController.
    """
    NUM_BIKES = int(sys.argv[1])
    calculated_routes = helpers.calc_random_route_by_city("umea")
    
    bike = BikeController(calculated_routes)
    print("Running simulation... [ctrl - c] to quit")
    bike.run(NUM_BIKES)
        
if __name__ == "__main__":
    main()