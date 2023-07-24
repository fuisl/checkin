from detect import FaceDetect, CodeDetect
from abc import ABC, abstractmethod

import cv2
import re
import sys

class Scanner(ABC):
    def __init__(self):
        self.cap
    
    @abstractmethod
    def detect():
        pass
    
    @abstractmethod
    def draw():
        pass

    def update():
        raise NotImplementedError

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
    

class FaceScanner(FaceDetect, Scanner):
    def update():  # Update method for return data from Face Detect -> list of tuples
        pass
    

class CodeScanner(CodeDetect, Scanner):
    def update():  # Update method for return data from Code Detect -> list of string
        pass

arguments = sys.argv[1:]
if __name__ == "__main__":
    pass