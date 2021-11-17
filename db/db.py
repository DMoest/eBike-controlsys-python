import requests


def getAllBikes():
    r = requests.get('http://ebike_backend:8000/api/bike')
    print(r.text.encode('utf-8'))
    return r.text

def getAllUsers():
    r = requests.get('http://ebike_backend:8000/api/user')
    return r.text
