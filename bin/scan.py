from detect import CodeDetect
from abc import ABC, abstractmethod
# from updater import Updater

import cv2
import re
import sys

class Scanner(ABC):
    def __init__(self, index=0):
        self.cap = None
        self.cam_index = index

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
            self.cap = cv2.VideoCapture(self.cam_index)
            if self.cap.isOpened():
                print("Connected successfully!")

        elif self._is_valid_ip(ip):
            print(f"Connecting to {ip}...")
            self.cap = cv2.VideoCapture(self._url_camera(ip, port))

            if self.cap.isOpened():
                print("Connected successfully!")
            else:
                print("Failed to connect to camera. Switching to default camera...")
                self.cap = cv2.VideoCapture(self.cam_index)

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
    
    def update(self, event_code):
        """
        Update event code to database

        Parameter:
            :event_code: Event code to update
        """
        pass

class CodeScanner(CodeDetect, Scanner):
    def __init__(self, event_code=None):
        """
        Initialize CodeScanner class

        Parameter:
            :event_code: Event code to scan. It's a practice to declare event code.
        """
        super().__init__()
        # self._updater = Updater(event_code)
        
    def scan(self):
        """
        Scan method will start connnected camera and start scanning for QR Code. With using OpenCV display, this module will also display the detected QR Code on the screen.

        If the detected QR Code is not flickering, it will update the detected QR Code to the database. 
        """
        paused = False
        count = 0
        prev_code = None
        valid = None
        valid_count = 0

        while True:
            ret, frame = self.cap.read()

            # Calculate and display FPS on top of the screen
            # fps = self.cap.get(cv2.CAP_PROP_FPS)
            # cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)
            if ret:
                codes = self.detect(frame)
                self.draw(frame)

                if codes is not None:
                    cv2.putText(frame, f"{codes[0]}", (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (12, 196, 255), 1)

                """
                If no code is detected, 
                count the number of frames. 
                If the number of frames is greater than 30, 
                reset the paused state to False.

                If the number of frames is greater than 90,
                reset the valid state to None. --> use to display valid state on screen.
                """
                if codes == None:
                    count += 1
                    valid_count += 1
                    if count > 30:  # 45 frames = 1.5 seconds
                        paused = False
                        count = 0
                    if valid_count > 90:  # 90 frames = 3 seconds
                        valid = None
                        valid_count = 0

                """
                If code is detected, and not because the code is flickering,
                do some action.
                """
                if (paused == False) & (codes != None) & (codes != prev_code):
                    print(codes[0])  # print detected id
                    prev_code = codes  # store detected id
                    # self._updater.update(codes[0])  # update to database
                    # self._updater.count(codes[0])  # count number of people have scanned.
                    result = self.update(codes[0])  # update to database

                    # Check if the detected code is valid or not; VALID is when the return value is not None
                    if result != None:
                        valid = True
                    else:
                        valid = False
                    paused = True

                    #TODO: display info on screen or print to console
                
                if valid == True:
                    cv2.putText(frame, "Valid", (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)
                elif valid == False:
                    cv2.putText(frame, "Invalid", (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)

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