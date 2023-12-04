import cv2

# Initialize the camera capture object
capture = cv2.VideoCapture(0)  # Use 0 to capture video from the default camera

# Define the codec and create a VideoWriter object
codec = cv2.VideoWriter_fourcc(*'XVID')  # Codec for video output (change as needed)
output_file = 'output_video.avi'  # Output video file name
fps = 30  # Frames per second
resolution = (640, 480)  # Resolution of the video (width, height)

out = cv2.VideoWriter(output_file, codec, fps, resolution)

# Check if the camera opened successfully
if not capture.isOpened() or not out.isOpened():
    print("Error: Could not open camera or create video file.")
    exit()

# Loop to capture video frames
while True:
    ret, frame = capture.read()  # Read a frame from the camera

    if not ret:
        print("Error: Failed to capture frame")
        break

    # Display the captured frame (optional, for live preview)
    cv2.imshow('Video Capture', frame)

    # Write the frame to the video file
    out.write(frame)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and video write objects
capture.release()
out.release()
cv2.destroyAllWindows()
