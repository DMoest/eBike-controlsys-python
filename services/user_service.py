#!/usr/bin/env python3
import random
import db.db
from app.user import User

class UserService():
    users = []

    def __init__(self):
        users_data = db.db.getAllUsers()["users"]
        self.init_users(users_data)

    def init_users(self, users_data):
        """
        Initializes user objects for each city.
        """
        for user in users_data:
            if user["city"] == "Umeå":
                self.users.append(User.create_from_json(user))
            elif user["city"] == "Stockholm":
                self.users.append(User.create_from_json(user))
            elif user["city"] == "Göteborg":
                self.users.append(User.create_from_json(user))

    def get_random_user(self):
        random_user_idx = random.randint(0, len(self.users) - 1)
        user = self.users.pop(random_user_idx)
        return user

    def get_users_count(self):
        return len(self.users)