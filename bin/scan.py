from detect import CodeDetect
from abc import ABC, abstractmethod
# from updater import Updater

import cv2
import re
import sys

class Scanner(ABC):
    def __init__(self):
        self.cap = None

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
    
    @abstractmethod
    def detect():
        pass
    
    @abstractmethod
    def draw():
        pass

    @abstractmethod
    def scan():
        pass

    def connect(self, ip=None, port='4747'):
        """
        Connect and setup camera for Scanner.

        Parameter:
            :ip: Remote camera ip address
        """
        if ip == None:
            print("Connecting to default camera...")
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                print("Connected successfully!")

        elif self._is_valid_ip(ip):
            print(f"Connecting to {ip}...")
            self.cap = cv2.VideoCapture(self._url_camera(ip, port))

            if self.cap.isOpened():
                print("Connected successfully!")
            else:
                print("Failed to connect to camera. Switching to default camera...")
                self.cap = cv2.VideoCapture(0)

                if not self.cap.isOpened():
                    raise RuntimeError("Failed to connect to default camera!")
                    
        else:
            raise ValueError("Invalid IP Address")
    
    def _is_valid_ip(self, address):
        """
        Check if a string is valid IP Address
        """
        pattern = r'^((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))$'
        return re.match(pattern, address) is not None
    
    def _url_camera(self, ip, port='4747'):
        """
        Get url to remote camera

        Parameter:
            :ip: ip address
            :port: port to camera (defaul: 4747)
        """
        url = 'http://' + ip + ':' + port + '/video'
        return url

class CodeScanner(CodeDetect, Scanner):
    def __init__(self, event_code):
        """
        Initialize CodeScanner class

        Parameter:
            :event_code: Event code to scan. It's a MUST to declare event code.
        """
        super().__init__()
        # self._updater = Updater(event_code)
        
    def scan(self):
        paused = False

        while True:
            ret, frame = self.cap.read()

            if ret:

                codes = self.detect(frame)
                self.draw(frame)

                if (paused == False) & (codes != None):
                    print(codes[0])  # print detected id

                    # self._updater.update(codes[0])  # update to database
                    # self._updater.count(codes[0])  # count number of people have scanned.
                    paused = True

                    #TODO: display info on screen or print to console

                cv2.imshow("Code Scanner", frame)

            key = cv2.waitKey(1)
            if key == 27:  # exit if ESC is pressed
                break
            elif key == 48:  # continue if '0' is pressed
                paused = False
        
        self.cap.release()
        cv2.destroyAllWindows()

arguments = sys.argv[1:]
if __name__ == "__main__":
    pass