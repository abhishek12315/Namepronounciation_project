import cv2

# Load the image you want to overlay
overlay_image = cv2.imread("Barner_2.jpg")  # Replace "path_to_your_image.jpg" with the actual path to your image file

# Create a VideoCapture object
cap = cv2.VideoCapture(0)  # 0 represents the default camera (usually the webcam)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Failed to open camera")
    exit()

# Get the size of the overlay image
overlay_height, overlay_width, _ = overlay_image.shape

# Get the screen width and height
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create a full-screen window for the camera feed
cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Camera Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Loop to continuously read frames from the camera
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # If frame reading is not successful, break the loop
    if not ret:
        print("Failed to capture frame")
        break

    # Resize the overlay image to match the width of the frame
    resized_overlay = cv2.resize(overlay_image, (frame.shape[1], int(frame.shape[1] * overlay_height / overlay_width)))

    # Calculate the position to overlay the image (bottom-left corner)
    y_offset = frame.shape[0] - resized_overlay.shape[0]
    x_offset = 0

    # Overlay the image on the frame
    frame[y_offset:frame.shape[0], x_offset:x_offset + resized_overlay.shape[1]] = resized_overlay

    # Display the frame in the full-screen window
    cv2.imshow("Camera Feed", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()
