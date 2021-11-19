import requests


def getAllBikes():
    r = requests.get('http://ebike_backend:8000/api/bike')
    return r.json()

def getAllUsers():
    r = requests.get('http://ebike_backend:8000/api/user')
    return r.json()
