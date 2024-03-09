from abc import ABC, abstractmethod

import cv2
import numpy as np
from pyzbar import pyzbar

"""
This modules contains the abstract class DetectBehavior and its concrete implementation CodeDetect.
"""

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
        objs = pyzbar.decode(gray)  # TODO: change to OpenCV QR/Barcode detection
        
        codes = []  # initialize empty list
        for obj in objs:
            code = obj.data.decode("utf-8")  # decode data in object

            codes.append(code)

        if codes:
            return codes
    
    def draw(self, frame):
        """
        Draw a red box around detected QR/Barcode to the imported frame

        Parameter:
        :frame: OpenCV frame.
        """
        # Convert frame to gray scale for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Decode frame and extract locations from frame
        objs = pyzbar.decode(gray)

        for obj in objs:
            code = obj.data.decode("utf-8")
            x, y, w, h = obj.rect

            # Get the four corners of the QR code
            pts = obj.polygon

            # Convert the corners to numpy array
            pts = np.array(pts, np.int32)

            # Reshape the array to a shape compatible with cv2.polylines()
            pts = pts.reshape((-1, 1, 2))

            # Draw the curved box around the corners
            cv2.polylines(frame, [pts], True, (0, 0, 255), 2)

        return frame