from Adafruit_IO import MQTTClient
import cv2
import base64

class Adafruit:
    def __init__(self, info:dict) -> None:
        self.username = info["username"]
        self.aio_key = info["key"]

        self.aio = MQTTClient(self.username, self.aio_key)

        self.paused = False

    def __connected(self, client):
        print("Connected to Adafruit IO!  Listening for {0} changes...".format(self.username))
        # Subscribe to changes on a feed named DemoFeed.
        client.subscribe('paused')
        client.subscribe('continue')

    def __subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed!")

    def __disconnected(self, client):
        print("Disconnected from Adafruit IO!")

    def __message(self, client, feed_id, payload):
        print("Feed {0} received new value: {1}".format(feed_id, payload))
        if feed_id == "paused":
            self.paused = True if payload == "1" else False

        if feed_id == "continue":
            self.paused = False
            self.send("paused", "0")

    def connect(self):
        self.aio.on_connect = self.__connected
        self.aio.on_disconnect = self.__disconnected
        self.aio.on_message = self.__message
        self.aio.on_subscribe = self.__subscribe

        self.aio.connect()
        self.aio.loop_background()

        # Reset paused to False:
        self.send("paused", "0")

    def send(self, feed, data: any):
        """
        Send any data to 'feed_name

        :param feed: feed name to display.
        :param n: people traffic at checkin.
        """
        self.aio.publish(feed, data)

    def send_img(self, feed, frame):
        """
        Send image to 'feed_name

        :param feed: feed name to display.
        :param frame: frame to send.
        """
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

        self.aio.publish(feed, jpg_as_text)