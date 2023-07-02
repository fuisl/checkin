import cv2
from pyzbar import pyzbar

"""
def decode_qr_code(frame):
    # Create a QRCodeDetector object
    qr_detector = cv2.QRCodeDetector()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect and decode QR codes in the frame
    decoded_val, points, _ = qr_detector.detectAndDecode(gray)

    # Extract and return the QR code values
    if decoded_val:
        return decoded_val
    else:
        return None
"""
    
def decode_ticket(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    codes = pyzbar.decode(gray)

    decoded_data = list()
        
    for code in codes:
        data = code.data.decode("utf-8")
        data_type = code.type
        print(f"QR Code: {data}, Type: {data_type}")

        decoded_data.append(data)

    if decoded_data:
        return decoded_data