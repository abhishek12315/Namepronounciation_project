import cv2
from pyzbar import pyzbar

# Load the logo and banner images
logo = cv2.imread('C:/Users/palla/Desktop/namepron/From_Aditya/source_code/logo.jpg')
banner = cv2.imread('C:/Users/palla/Desktop/namepron/From_Aditya/source_code/Banner.jpg')

# Define the coordinates for placing the logo and banner
logo_x = 50
logo_y = 400
banner_x = 0
banner_y = 600

# Load the camera
cap = cv2.VideoCapture(1)

while True:
    # Read frame from the camera
    ret, frame = cap.read()

    # Add the logo to the frame
    frame[logo_y:logo_y+logo.shape[0], logo_x:logo_x+logo.shape[1]] = logo

    # Add the banner to the frame
    frame[banner_y:banner_y+banner.shape[0], banner_x:banner_x+banner.shape[1]] = banner

    # Display the frame
    cv2.imshow('Camera', frame)

    # Check for QR codes
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        # Extract QR code data
        qr_data = barcode.data.decode('utf-8')

        # Parse the data
        name, umid, college = qr_data.split(',')

        # Print the information on the camera frame
        text = f'Name: {name}, UMID: {umid}, College: {college}'
        cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Check for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
