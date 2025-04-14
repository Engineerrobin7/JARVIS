import cv2
import pytesseract

# Specify the path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def OCR():
    # Open the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    while True:
        # Capture a frame from the camera
        success, img = cap.read()
        if not success or img is None:
            print("Error: Failed to capture frame from camera.")
            break

        try:
            # Process the captured frame
            imgT = img.copy()
            textRecognized = pytesseract.image_to_string(img, lang='eng')
            print("Recognized Text:")
            print(textRecognized)

            # Display the frame with recognized text
            cv2.imshow("Image", imgT)
        except Exception as e:
            print(f"Error processing frame: {e}")

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()