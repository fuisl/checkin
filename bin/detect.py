import cv2
from pyzbar import pyzbar

def decode_ticket(frame):
    """
    Take a frame read from OpenCV, decode and return the values as a list.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    codes = pyzbar.decode(gray)

    decoded_data = list()
        
    for code in codes:
        data = code.data.decode("utf-8")
        
        decoded_data.append(data)

    if decoded_data:
        return decoded_data

def draw(frame):
    """
    Draw a green box around detected QR/Barcode to the imported frame.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    decoded_obj = pyzbar.decode(gray)

    for obj in decoded_obj:
        x, y, w, h = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    return None
