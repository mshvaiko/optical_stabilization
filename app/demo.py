#!/usr/bin/env python

import time
import cv2
import numpy as np
import bright_spot_tracker as bst
import orb_tracker as ot

# Define the video file path
# VIDEO_PATH = r'./assets/moving_red_spot.mp4' # bright_spot_tracker
# VIDEO_PATH = r'./assets/flying_drone.mov' # orb_tracker
# VIDEO_PATH = r'./assets/red_drone_in_the_sky_from_start.mp4' # bright_spot_tracker, orb_tracker
# VIDEO_PATH = r'./assets/red_drone_in_the_sky_bird.mp4' # bright_spot_tracker, orb_tracker
# VIDEO_PATH = r'./assets/VID_20240817_115314.mp4' # bright_spot_tracker, orb_tracker
VIDEO_PATH = './assets/VID_20240817_115358.mp4' # bright_spot_tracker, orb_tracker

# FOR DEBUG: Use playback delay to match the video frame rate
DEBUG_FRAME_DELAY = True

def dispay_image(frame, osd_frame, title, max_width=1920, max_height=1080):
    # Print the cross and misc text
    cv2.line(osd_frame, (osd_frame.shape[1] // 2, 0), (osd_frame.shape[1] // 2, osd_frame.shape[0]), (0, 255, 0), 1)
    cv2.line(osd_frame, (0, osd_frame.shape[0] // 2), (osd_frame.shape[1], osd_frame.shape[0] // 2), (0, 255, 0), 1)
    cv2.putText(osd_frame, f"Press 'q' to exit", (0, 120),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Blend the osd_frame with the frame
    merged_frame = cv2.addWeighted(frame, 1, osd_frame, 1, 0)

    # Get the current frame dimensions
    height, width = merged_frame.shape[:2]

    # Check if resizing is needed
    if width > max_width or height > max_height:
        # Calculate the scaling factor
        scaling_factor = min(max_width / width, max_height / height)
        # Resize the frame
        merged_frame = cv2.resize(merged_frame, (int(width * scaling_factor), int(height * scaling_factor)))

    # Display the frame
    cv2.imshow(title, merged_frame)

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
        # Capture frame
        ret, frame = cap.read()

        if not ret:
            break

        bst_coordinates, ot_coordinates = None, None

        # Create a frame to display the OSD (debug info)
        osd_frame = np.zeros(frame.shape, dtype=np.uint8)

        # Use the bright spot tracker module
        bst_coordinates = bst.process_frame(frame, osd_frame)

        # Use the ORB tracker module
        ot_coordinates = ot.process_frame(frame, osd_frame)

        # Use the coordinates from the module that detected the drone
        coordinates = bst_coordinates or ot_coordinates
        print(f"Drone coordinates: {coordinates}")

        dispay_image(frame, osd_frame, 'Tracking Drone')

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