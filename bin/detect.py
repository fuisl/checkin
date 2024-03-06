from abc import ABC, abstractmethod

import cv2
from pyzbar import pyzbar


class DetectBehavior(ABC):

    @abstractmethod
    def detect(frame):
        pass

    @abstractmethod
    def draw(frame):
        pass

class CodeDetect(DetectBehavior):

    def detect(self, frame):
        """
        Take a frame read from OpenCV, detect and return values detected as a list.

        Parameter:
        :frame: OpenCV frame
        """

        # Convert frame to gray scale for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Decode frame and extract codes from frame
        objs = pyzbar.decode(gray)
        
        codes = []  # initialize empty list
        for obj in objs:
            code = obj.data.decode("utf-8")  # decode data in object

            codes.append(code)

        if codes:
            return codes
    
    def draw(self, frame):
        """
        Draw a red box around detected QR/Barcode to the imported frame
        """
        # Convert frame to gray scale for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Decode frame and extract locations from frame
        objs = pyzbar.decode(gray)

        for obj in objs:
            x, y, w, h = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return frame