from detect import FaceDetect, CodeDetect
from abc import ABC, abstractmethod
from updater import FaceUpdater, CodeUpdater
from adafruit import Adafruit

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

    @abstractmethod
    def update():
        """
        Update detected code to database
        """
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
    

class FaceScanner(FaceDetect, FaceUpdater, Scanner):
    def __init__(self):
        super(Scanner, self).__init__()
        super(FaceUpdater, self).__init__()
        self._knn_clf = None
        self._model_path = None
    
    def load_model(self, knn_clf=None, model_path=None):
        self._knn_clf = knn_clf
        self._model_path = model_path

    def scan(self):
        paused = False

        info = {"username":"fuisl",
                "key":"aio_Zpqj39l0FDq745LDnw1P1zuKxXXE"}
        """
        Feed names and its input data:

        traffic: people/minute: float -> 4.52 p/m
        info: detected info: string -> "10422021 - Tran Hai Duong - 4YC8UA"
        face: frame with face detected: OpenCV frame
        paused: pausing status: bool -> True/False
        """
        ada = Adafruit(info)

        switch2 = 59
        switch = 14
        while True:
            ret, frame = self.cap.read()

            if ret:
                # Resize
                frame_small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

                switch += 1
                # process image for every 15 frams
                if switch % 15 == 0:
                    faces = self.detect(frame_small,self._knn_clf, self._model_path)
                
                switch2 += 1
                if switch2 % 60 == 0:
                    if ada.fetch('paused')[0]['value'] == '0':
                        paused = False

                if faces:  # if any face detected
                    frame = self.draw(frame, faces)

                    if (faces[0][0] != 'unknown') & (paused == False):
                        paused = True
                        ada.send('paused', '1')
                        print(faces[0][0])
                        # TODO: Add update() method here
                        # self.update(faces[0][0])
                        
                        ada.send_img('face', frame)

                cv2.imshow('Face Scanner', frame)

            key = cv2.waitKey(1)

            if key == 27:  # exit if ESC is pressed
                break
            elif key == 48:  # continue if '0' is pressed
                paused = False

        self.cap.release()
        cv2.destroyAllWindows()
    

class CodeScanner(CodeDetect, CodeUpdater, Scanner):
    def __init__(self):
        super(Scanner, self).__init__()
        super(CodeUpdater, self).__init__()

    def scan(self):
        paused = False

        while True:
            ret, frame = self.cap.read()

            if ret:
                codes = self.detect(frame)
                if (paused == False) & (codes != None):
                    paused = True  # switch statement for pausing camera
                    print(codes[0])
                    # TODO: Add update() method here
                    self.update(codes[0])

                self.draw(frame)
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