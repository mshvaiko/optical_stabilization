#!/usr/bin/env python

import time
import cv2
import numpy as np
import bright_spot_tracker as bst

# Define the video file path
VIDEO_PATH = r'.\assets\moving_red_spot.mp4' # 1

# FOR DEBUG: Use playback delay to match the video frame rate
DEBUG_FRAME_DELAY = True

def main():
    # Open the video file using cv2.VideoCapture
    cap = cv2.VideoCapture(VIDEO_PATH)

    # Check if the video file was opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video {VIDEO_PATH}.")
        exit()

    # Get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1 / fps

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break

        # Process the frame to find and track the drone
        coordinates = bst.process_frame(frame)
        if coordinates:
            print(f"Drone coordinates: {coordinates}")

        # Print the cross and misc text
        cv2.line(frame, (frame.shape[1] // 2, 0), (frame.shape[1] // 2, frame.shape[0]), (0, 255, 0), 1)
        cv2.line(frame, (0, frame.shape[0] // 2), (frame.shape[1], frame.shape[0] // 2), (0, 255, 0), 1)
        cv2.putText(frame, f"Press 'q' to exit", (0, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Display the resulting frame
        cv2.imshow('Tracking Drone', frame)

        # Introduce a delay to match the frame rate of the video
        if DEBUG_FRAME_DELAY:
            time.sleep(frame_delay)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()