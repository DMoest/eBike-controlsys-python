#!/usr/bin/env python3

class Parking():
    """
    Represents a registered user in the eBike system.
    """

    _id = None
    city = None
    sw = None
    se = None
    nw = None
    ne = None

    def __init__(self, id, city, sw, se, nw, ne):
        self._id = id
        self.city = city
        self.sw = sw
        self.se = se
        self.nw = nw
        self.ne = ne

    @classmethod
    def create_from_json(cls, json_data):
        return cls(
            json_data["_id"],
            json_data["city"],
            (json_data["sw_latitude"], json_data["sw_longitude"]),
            (json_data["se_latitude"], json_data["se_longitude"]),
            (json_data["nw_latitude"], json_data["nw_longitude"]),
            (json_data["ne_latitude"], json_data["ne_longitude"]))