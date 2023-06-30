import cv2

def decode_qr_code(frame):
    # Create a QRCodeDetector object
    qr_detector = cv2.QRCodeDetector()

    # Detect and decode QR codes in the frame
    decoded_val, points, _ = qr_detector.detectAndDecode(frame)

    # Extract and return the QR code values
    if decoded_val:
        return decoded_val
    else:
        return None


def main():
    # Open the video capture
    video_capture = cv2.VideoCapture(0)

    scan = True
    while scan:
        # Read a frame from the video capture
        ret, frame = video_capture.read()

        # If the frame was read successfully
        if ret:
            # Display the frame
            cv2.imshow("Video", frame)

            # Detect QR codes and get their values
            qr_code_values = decode_qr_code(frame)
            
            # Print the QR code values
            if qr_code_values != None:
                print("QR Code values:", qr_code_values)
                scan = False

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close the windows
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
