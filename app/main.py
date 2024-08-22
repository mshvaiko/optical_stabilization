#!/usr/bin/env python

import cv2
import bright_spot_tracker as bst
import orb_tracker as ot

# Define the camera index
VIDEO_SOURCE = 0

def main():
    # Open the camera stream using cv2.VideoCapture
    cap = cv2.VideoCapture(VIDEO_SOURCE)

    # Check if the camera stream was opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open camera stream with index {VIDEO_SOURCE}.")
        exit()

    print('Working. To exit press CTRL+C')

    try:
        while True:
            # Capture frame
            ret, frame = cap.read()

            if not ret:
                break

            # Coorfinate variables from different rtacking modules
            bst_coordinates, ot_coordinates = None, None

            # Use the bright spot tracker module
            bst_coordinates = bst.process_frame(frame)

            # Use the ORB tracker module
            ot_coordinates = ot.process_frame(frame)

            # Use the coordinates from the module that detected the drone
            coordinates = bst_coordinates or ot_coordinates
            print(f"Drone coordinates: {coordinates}")
    except KeyboardInterrupt:
        print('Stopped')
    finally:
        # Release the capture and close windows
        cap.release()

if __name__ == "__main__":
    main()