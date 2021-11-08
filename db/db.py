import firebase_admin
from firebase_admin import db

class Firebase:
    cred_obj = None
    app = None

    def __init__(self):
        self.cred_obj = firebase_admin.credentials.Certificate('./fb_secret.json')
        self.app = firebase_admin.initialize_app(self.cred_obj, {
            'databaseURL':'https://bike-test-dfe8c-default-rtdb.firebaseio.com/'
            })
