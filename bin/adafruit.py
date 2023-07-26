import requests
from Adafruit_IO import Client

class Adafruit:
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
        self.username = info["username"]
        self.aio_key = info["key"]
        # feed = info["feed"]

        self.aio = Client(self.username, self.aio_key)
    
    def send(self, feed, data: any):
        """
        Send any data to 'feed_name

        :param feed: feed name to display.
        :param n: people traffic at checkin.
        """
        self.aio.send_data(feed, data)

    def fetch(self, feed):
        """
        Fetch a data from a feed.

        :param feed: feed name to receive data.
        """
        # Construct the URL for the feed data
        url = f"https://io.adafruit.com/api/v2/{self.username}/feeds/{feed}/data"

        # Set up headers with the API key
        headers = {
            "X-AIO-Key": self.aio_key
        }

        try:
            # Send GET request to fetch data
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                # print(f"Failed to fetch data. Status code: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
