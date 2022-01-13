import unittest
from app.bike import Bike
from app.user import User
import main
import utils.helpers as helpers
from unittest.mock import MagicMock
from unittest.mock import patch
import json
from multiprocessing import Process


from app.customer import Customer



######################################### Tests for Bike class #######################################



class TestBike(unittest.TestCase):

    def test_bike_create(self):
        """
        Object can be created successfully.
        """
        parkings = {
            "parkings": [
                        [
                            {"lat": 63.828615, "long": 20.253928},
                            {"lat": 63.826621, "long": 20.250680},
                            {"lat": 63.827423, "long": 20.251668}
                        ],
                        [
                            {"lat": 63.825414, "long": 20.262796},
                            {"lat": 63.824045, "long": 20.260819},
                            {"lat": 63.824454, "long": 20.261379}
                        ]
                    ]
        }
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.825107, "longitude": 20.261642, "parkings": parkings}
        bike = Bike.create_from_json(bike_json)
        self.assertEqual(bike._id, 1)
        self.assertEqual(bike._city, "Umeå")
        self.assertEqual(bike._status, "in repair")
        self.assertEqual(bike._active, False)
        self.assertEqual(bike._position, {"lat2": 63.825107, "lon2": 20.261642})

    def test_valid_parking_position(self):
        parkings = [
                    [
                        {"lat": 63.824920, "long": 20.263607},
                        {"lat": 63.824319, "long": 20.260667}
                    ],
                    [
                        {"lat": 63.828420, "long": 20.253622},
                        {"lat": 63.826940, "long": 20.250028}
                    ]
                ]
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.827211, "longitude": 20.252348, "parkings": parkings}
        bike = Bike.create_from_json(bike_json)
        
        bike.check_in_parking_area(parkings)

        self.assertTrue(bike._parking_approved)

    def test_invalid_parking_position(self):
        parkings = [
                    [
                        {"lat": 63.824920, "long": 20.263607},
                        {"lat": 63.824319, "long": 20.260667}
                    ],
                    [
                        {"lat": 63.828420, "long": 20.253622},
                        {"lat": 63.826940, "long": 20.250028}
                    ]
                ]
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.826263, "longitude": 20.254804, "parkings": parkings}
        bike = Bike.create_from_json(bike_json)
        
        bike.check_in_parking_area(parkings)

        self.assertFalse(bike._parking_approved)

    def test_charging(self):
        """
        Test that bikes charging status is updated.
        """
        parkings = {
            "parkings": [
                        [
                            {"lat": 63.828615, "long": 20.253928},
                            {"lat": 63.826621, "long": 20.250680},
                            {"lat": 63.827423, "long": 20.251668}
                        ],
                        [
                            {"lat": 63.825414, "long": 20.262796},
                            {"lat": 63.824045, "long": 20.260819},
                            {"lat": 63.824454, "long": 20.261379}
                        ]
                    ]
        }
        
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.827211, "longitude": 20.252348, "parkings": parkings}
        bike = Bike.create_from_json(bike_json)

        bike.charge_bike()

        self.assertTrue(bike._is_charging)

    def test_start(self):
        """
        Test that start method set correct active status and that
        updatedb() is called.
        """
        parkings = {
            "parkings": [
                        [
                            {"lat": 63.828615, "long": 20.253928},
                            {"lat": 63.826621, "long": 20.250680},
                            {"lat": 63.827423, "long": 20.251668}
                        ],
                        [
                            {"lat": 63.825414, "long": 20.262796},
                            {"lat": 63.824045, "long": 20.260819},
                            {"lat": 63.824454, "long": 20.261379}
                        ]
                    ]
        }

        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.827211, "longitude": 20.252348, "parkings": parkings}
        bike = Bike.create_from_json(bike_json)

        bike.update_db = MagicMock()
        bike.start_trip = MagicMock()
        bike.end_trip = MagicMock()
        bike.start({})
        
        self.assertTrue(bike._active)
        bike.update_db.assert_called_once()

    def test_stop(self):
        """
        Test that start method set correct active status and that
        updatedb() is called.
        """
        parkings = {
            "parkings": [
                        [
                            {"lat": 63.828615, "long": 20.253928},
                            {"lat": 63.826621, "long": 20.250680},
                            {"lat": 63.827423, "long": 20.251668}
                        ],
                        [
                            {"lat": 63.825414, "long": 20.262796},
                            {"lat": 63.824045, "long": 20.260819},
                            {"lat": 63.824454, "long": 20.261379}
                        ]
                    ]
        }
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.827211, "longitude": 20.252348, "parkings": parkings}
        bike = Bike.create_from_json(bike_json)

        bike.update_db = MagicMock()
        bike.start_trip = MagicMock()
        bike.end_trip = MagicMock()
        bike.stop()
        
        self.assertFalse(bike._active)
        bike.update_db.assert_called_once()



######################### Tests for Customer class ######################################



class TestCustomer(unittest.TestCase):
    """
    Test that bike object is started and that the start_bike method
    in Customer object gets called when calling run()
    """
    def test_run(self):
        parkings = {
            "parkings": [
                        [
                            {"lat": 63.828615, "long": 20.253928},
                            {"lat": 63.826621, "long": 20.250680},
                            {"lat": 63.827423, "long": 20.251668}
                        ],
                        [
                            {"lat": 63.825414, "long": 20.262796},
                            {"lat": 63.824045, "long": 20.260819},
                            {"lat": 63.824454, "long": 20.261379}
                        ]
                    ]
        }
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.827211, "longitude": 20.252348, "parkings": parkings}
        bike = Bike.create_from_json(bike_json)
        user_json = {
            "_id": "61954fd32cec02b4ff0a2bfd",
            "firstname": "Siv",
            "lastname": "Björk",
            "adress": "Lillvägen 2I",
            "postcode": "548 72",
            "city": "Umeå",
            "phone": "0442-599 96",
            "email": "marie.lind@example.org",
            "email_verified_at": "2021-11-17T18:54:10.964000Z",
            "payment_method": "monthly",
            "payment_status": "paid",
            "updated_at": "2021-11-17T18:54:11.477000Z",
            "created_at": "2021-11-17T18:54:11.477000Z"
            }
        user = User.create_from_json(user_json)
        routes = helpers.calc_random_route_by_city("Umeå")
        customer = Customer(routes, 1, bike, user)

        bike.start = MagicMock()
        bike.stop = MagicMock()
        customer.start_bike = MagicMock()

        customer.run()
        customer.start_bike.assert_called_once()
        bike.start.assert_called_once()

    @patch('time.sleep', return_value=None)
    def test_start_bike(self, patched_time_sleep):
        parkings = {
            "parkings": [
                        [
                            {"lat": 63.828615, "long": 20.253928},
                            {"lat": 63.826621, "long": 20.250680},
                            {"lat": 63.827423, "long": 20.251668}
                        ],
                        [
                            {"lat": 63.825414, "long": 20.262796},
                            {"lat": 63.824045, "long": 20.260819},
                            {"lat": 63.824454, "long": 20.261379}
                        ]
                    ]
        }
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": True, "latitude": 63.827211, "longitude": 20.252348, "parkings": parkings}
        bike = Bike.create_from_json(bike_json)
        user_json = {
            "_id": "61954fd32cec02b4ff0a2bfd",
            "firstname": "Siv",
            "lastname": "Björk",
            "adress": "Lillvägen 2I",
            "postcode": "548 72",
            "city": "Umeå",
            "phone": "0442-599 96",
            "email": "marie.lind@example.org",
            "email_verified_at": "2021-11-17T18:54:10.964000Z",
            "payment_method": "monthly",
            "payment_status": "paid",
            "updated_at": "2021-11-17T18:54:11.477000Z",
            "created_at": "2021-11-17T18:54:11.477000Z"
            }
        user = User.create_from_json(user_json)
        routes = helpers.calc_random_route_by_city("Umeå")
        customer = Customer(routes, 1, bike, user)

        bike.move_bike = MagicMock()
        bike.start = MagicMock()
        bike.stop = MagicMock()

        customer.start_bike(bike)
        bike.move_bike.assert_called()


#################################### Test main ########################################


# class TestMain(unittest.TestCase):
#     def test_init_bike(self):
#         """
#         Test funktion to initialize new Bike object.
#         """
#         bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.827211, "longitude": 20.252348}
#         bike = main.init_bike(bike_json)
#         self.assertIsInstance(bike, Bike)
#         self.assertEqual(bike._id, 1)


#     def test_init_users(self):
#         """
#         Test that list of users in main is properly populated.
#         """
#         users = [
#             {
#                 "_id": "61954fd32cec02b4ff0a2bfd",
#                 "firstname": "Siv",
#                 "lastname": "Björk",
#                 "adress": "Lillvägen 2I",
#                 "postcode": "548 72",
#                 "city": "Umeå",
#                 "phone": "0442-599 96",
#                 "email": "marie.lind@example.org",
#                 "email_verified_at": "2021-11-17T18:54:10.964000Z",
#                 "payment_method": "monthly",
#                 "payment_status": "paid",
#                 "updated_at": "2021-11-17T18:54:11.477000Z",
#                 "created_at": "2021-11-17T18:54:11.477000Z"
#             },
#         ]

#         main.init_users(users)
#         self.assertEqual(len(main.users), 1)
#         self.assertIsInstance(main.users[0], User)

#     def test_init_bikes(self):
#         """
#         Test that list of bikes in main is properly populated.
#         """
#         bikes = [
#             {
#                 "_id": 1,
#                 "city": "Umeå",
#                 "status": "in repair",
#                 "active": False,
#                 "latitude": 63.827211,
#                 "longitude": 20.252348
#             }
#         ]

#         main.init_bikes(bikes)
#         self.assertEqual(len(main.bikes_in_city["Umeå"]), 1)
#         self.assertIsInstance(main.bikes[0], Bike)

#     def test_init_processes(self):
#         """
#         Test that list of bikes in main is properly populated.
#         """
#         users = [
#             {
#                 "_id": "61954fd32cec02b4ff0a2bfd",
#                 "firstname": "Siv",
#                 "lastname": "Björk",
#                 "adress": "Lillvägen 2I",
#                 "postcode": "548 72",
#                 "city": "Umeå",
#                 "phone": "0442-599 96",
#                 "email": "marie.lind@example.org",
#                 "email_verified_at": "2021-11-17T18:54:10.964000Z",
#                 "payment_method": "monthly",
#                 "payment_status": "paid",
#                 "updated_at": "2021-11-17T18:54:11.477000Z",
#                 "created_at": "2021-11-17T18:54:11.477000Z"
#             },
#         ]

#         bikes = [
#             {
#                 "_id": 1,
#                 "city": "Umeå",
#                 "status": "in repair",
#                 "active": False,
#                 "latitude": 63.827211,
#                 "longitude": 20.252348
#             }
#         ]

#         main.init_users(users)
#         main.init_bikes(bikes)
#         main.init_processes(1)
#         self.assertEqual(len(main.processes), 1)
#         self.assertIsInstance(main.processes[0], Process)




if __name__ == '__main__':
    unittest.main()