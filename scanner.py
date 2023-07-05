import cv2
from detect import *

def main():
    # Open the video capture
    wifi_ip = '172.16.133.112'
    port = '4747'
    url = 'http://' + wifi_ip + ':' + port + '/video'
    print(url)
    video_capture = cv2.VideoCapture(url)
    
    # Check if remote camera is opened, if not, switch to default camera.
    if video_capture.isOpened():
        print("Connected successfully")
    else:
        print("Failed to connect to the camera. Switching to default camera...")
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            print("Failed to connect to default camera!")
            exit()

    # Camera settings
    video_capture.set(cv2.CAP_PROP_FPS, 5)


    paused = False
    # Executing scanner
    while True:
        if not paused:
        # Read a frame from the video capture
            ret, frame = video_capture.read()

            # If the frame was read successfully
            if ret:
                # Display the frame
                cv2.imshow("Video", frame)

                # Detect QR codes and get their values
                qr_code_values = decode_ticket(frame)
                
                # Print the QR code values
                if qr_code_values != None:
                    print(qr_code_values)

                    #paused = True
      
        key = cv2.waitKey(1)
        # Exit if 'q' is pressed
        if key == ord('q'):
            break
        elif key == ord('c'):
            paused = not paused

    # Release the video capture and close the windows
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
