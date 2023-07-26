import requests
from Adafruit_IO import Client, Feed
from abc import ABC, abstractmethod

import json

import time
from datetime import datetime, timedelta

class Adafruit(ABC):
    def __init__(self, info):
        """
        Initialize object Adafruit

        :param info: dictionary contains info of user and dashboard.
        Example:
        
        dict = {
            "username":"fuisl",
            "key"="..."
        }

        username: Adafruit username
        key: AIO Key
        id: dashboard_id
        """
        username = info["username"]
        aio_key = info["key"]
        # feed = info["feed"]

        self.aio = Client(username, aio_key)
    
    def traffic_update(self, feed, n):
        """
        Show number of people check-in per minute (people/minute)

        :param feed: feed name to display.
        :param n: people traffic at checkin.
        """
        pass

    def face_update(self, feed, img):
        """
        Show picture of face_detected and checked_in frame that appears in database.
        
        :param feed: feed name to display.
        :param img: encoded image that has green box drew on face.
        """
        pass

    def info_update(self, feed, info):
        """
        :param feed: feed name to display.
        :param info: a formatted string to display ticket info.
        """
        pass

    def indicator_update(self, feed, status):
        """
        :param feed: feed name to display.
        :param status: True/False indicates paused status
        """
        pass
