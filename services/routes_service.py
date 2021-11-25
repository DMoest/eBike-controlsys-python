#!/usr/bin/env python3
import utils.helpers as helpers

class RouteService():
    
    umea_calculated_routes = None
    stockholm_calculated_routes = None
    goteborg_calculated_routes = None

    def __init__(self):
        self.umea_calculated_routes = helpers.calc_random_route_by_city("Umeå")
        self.stockholm_calculated_routes = helpers.calc_random_route_by_city("Stockholm")
        self.goteborg_calculated_routes = helpers.calc_random_route_by_city("Göteborg")

    def get_routes_for_umea(self):
        return self.umea_calculated_routes

    def get_routes_for_stockholm(self):
        return self.umea_calculated_routes

    def get_routes_for_goteborg(self):
        return self.goteborg_calculated_routes
