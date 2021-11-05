from bike_controller import BikeController
import helpers
import sys

def main():
    """
    Initializes and runs a new BikeController.
    """
    NUM_BIKES = int(sys.argv[1])
    base_routes = helpers.loadJson()

    calculated_routes = {}

    for city in base_routes.keys():
        calculated_routes[city] = {}
        for i, route in enumerate(base_routes[city]):
            calculated_routes[city][i] = {}
            for speed in range(5, 25):
                calculated_routes[city][i][speed] = helpers.calculate_route(route, speed)
            print(calculated_routes[city][i].keys())
    bike = BikeController(calculated_routes)
    bike.run(NUM_BIKES)
        
if __name__ == "__main__":
    main()