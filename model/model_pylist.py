"""
Python list model
"""
from datetime import date
from .Model import Model

class model(Model):
    def __init__(self):
        self.guestentries = []

    def select(self, email):
        """
        Returns guestentries list of lists
        Each list in guestentries contains: name, email, date, message
        :return: List of lists
        """
        return self.guestentries

    def insert(self, name, email):
        """
        Appends a new list of values representing new message into guestentries
        :param name: String
        :param email: String
        :return: True
        """
        params = [name, email, date.today()]
        self.guestentries.append(params)
        return True
