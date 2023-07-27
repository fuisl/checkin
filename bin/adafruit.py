import requests
from Adafruit_IO import Client
import cv2
import base64

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
    
    TARGET_SIZE_BYTES = 100 * 1024
    def send_img(self, feed, frame):
        # Resize the frame while keeping the aspect ratio
        target_width = 320  # You can adjust this value to control the size
        aspect_ratio = frame.shape[1] / frame.shape[0]
        target_height = int(target_width / aspect_ratio)
        resized_frame = cv2.resize(frame, (target_width, target_height))
        
        # Convert the frame to JPEG format as bytes
        _, buffer = cv2.imencode(".jpg", resized_frame)
        jpg_as_bytes = buffer.tobytes()

        # Encode the bytes to base64 and convert to string
        jpg_as_text = base64.b64encode(jpg_as_bytes).decode("utf-8")

        self.aio.send_data(feed, jpg_as_text)