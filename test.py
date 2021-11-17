import unittest
from app.bike import Bike
from app.user import User
import utils.helpers as helpers
from unittest.mock import MagicMock
from unittest.mock import patch

from app.customer import Customer

class TestBike(unittest.TestCase):
    def test_bike_create(self):
        """
        Object can be created successfully.
        """
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.825107, "longitude": 20.261642}
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
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.827211, "longitude": 20.252348}
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
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.826263, "longitude": 20.254804}
        bike = Bike.create_from_json(bike_json)
        
        bike.check_in_parking_area(parkings)

        self.assertFalse(bike._parking_approved)

    def test_charging(self):
        """
        Test that bikes charging status is updated.
        """
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.827211, "longitude": 20.252348}
        bike = Bike.create_from_json(bike_json)

        bike.charge_bike()

        self.assertTrue(bike._is_charging)

    def test_start(self):
        """
        Test that start method set correct active status and that
        updatedb() is called.
        """
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.827211, "longitude": 20.252348}
        bike = Bike.create_from_json(bike_json)

        bike.update_db = MagicMock()
        bike.start()
        
        self.assertTrue(bike._active)
        bike.update_db.assert_called_once()

    def test_stop(self):
        """
        Test that start method set correct active status and that
        updatedb() is called.
        """
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.827211, "longitude": 20.252348}
        bike = Bike.create_from_json(bike_json)

        bike.update_db = MagicMock()
        bike.stop()
        
        self.assertFalse(bike._active)
        bike.update_db.assert_called_once()




class TestCustomer(unittest.TestCase):
    """
    Test that bike object is started and that the start_bike method
    in Customer object gets called when calling run()
    """
    def test_run(self):
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.827211, "longitude": 20.252348}
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
        customer.start_bike = MagicMock()

        customer.run()
        customer.start_bike.assert_called_once()
        bike.start.assert_called_once()

    @patch('time.sleep', return_value=None)
    def test_start_bike(self, patched_time_sleep):
        bike_json = {"_id": 1, "city": "Umeå", "status": "in repair", "active": False, "latitude": 63.827211, "longitude": 20.252348}
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

        customer.start_bike(bike)
        bike.move_bike.assert_called()




if __name__ == '__main__':
    unittest.main()