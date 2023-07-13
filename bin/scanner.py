import cv2
from detect import *
import sys
import re

# Check if a string is a valid IP Address
def is_valid_ip(address):
    pattern = r'^((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))$'
    return re.match(pattern, address) is not None

arguments = sys.argv[1:]

# Exit if provided more than 1 argument
if len(arguments) > 1:
    print("Usage: py scanner.py <ip address>")
    sys.exit(1)

# Exit if not a valid IP Address
if len(arguments) == 1:
    if not is_valid_ip(arguments[0]):
        raise ValueError("Not an IP Address!")


def url_camera(wifi_ip):
    # Open the video capture
    port = '4747'
    url = 'http://' + wifi_ip + ':' + port + '/video'
    print(url)
    return url


def main():
    paused = False
    # Executing scanner
    while True:
            
        # Read a frame from the video capture
        ret, frame = video_capture.read()

        # If the frame was read successfully
        if ret:
            # Draw a box around detected code
            draw(frame)

            # Display the frame
            cv2.imshow("Video", frame)


            # Detect QR codes and get their values
            qr_code_values = decode_ticket(frame)
            
            # Print the QR code values
            if qr_code_values != None and paused == False:
                print(qr_code_values)
                paused = True

      
        key = cv2.waitKey(1)
        # Exit if 'ESC' is pressed
        if key == 27:
            break
        elif key == 48:  # Continue if "0" is pressed
            paused = False

    # Release the video capture and close the windows
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(arguments) > 0:

        print("Connecting to remote camera...")
        video_capture = cv2.VideoCapture(url_camera(arguments[0]))  # Connect to a remote camera using its IP Address
        
        # Check if remote camera is opened, if not, switch to default camera.
        if video_capture.isOpened():
            print("Connected successfully")
        else:
            print("Failed to connect to camera. Switching to default camera...")
            video_capture = cv2.VideoCapture(0)
            if not video_capture.isOpened():
                print("Failed to connect to default camera!")
                exit()

    if len(arguments) == 0:

        print("Connecting to default camera...")
        video_capture = cv2.VideoCapture(0)
        
    # Camera settings
    video_capture.set(cv2.CAP_PROP_FPS, 5)

    main()
