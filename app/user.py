
class User():
    """
    Represents a registered user in the eBike system.
    """

    _id = None
    city = None

    def __init__(self, id, city):
        self._id = id,
        self.city = city

    @classmethod
    def create_from_json(cls, json_data):
        return cls(
            json_data["_id"],
            json_data["city"])