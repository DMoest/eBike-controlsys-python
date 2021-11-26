#!/usr/bin/env python3

import requests

class Api():
    """
    Module that comminicates with the API
    """
    def __init__(self):
        pass

    def getAllBikes(self):
        r = requests.get('http://ebike_backend:8000/api/bike')
        return r.json()

    def getAllUsers(self):
        r = requests.get('http://ebike_backend:8000/api/user')
        return r.json()
