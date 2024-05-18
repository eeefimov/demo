"""Class for handling INGREDIENTS api requests."""
from api.base import BASEAPI


class INGREDIENTS(BASEAPI):
    """Class for handling INGREDIENTS api requests."""
    def __init__(self):
        super().__init__()
        self.endpoint = self.endpoints.ingredients
        self.header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
