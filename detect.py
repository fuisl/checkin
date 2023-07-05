import cv2
from pyzbar import pyzbar

def decode_ticket(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    codes = pyzbar.decode(gray)

    decoded_data = list()
        
    for code in codes:
        data = code.data.decode("utf-8")
        
        decoded_data.append(data)

    if decoded_data:
        return decoded_data