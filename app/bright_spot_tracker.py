# Description: This file contains the code to track a bright spot in a video stream.

import cv2
import numpy as np

# Define the range for red color in HSV
LOWER_RED1 = np.array([127, 50, 50])
UPPER_RED1 = np.array([147, 255, 255])
LOWER_RED2 = np.array([150, 100, 100])
UPPER_RED2 = np.array([180, 255, 255])

def process_frame(frame, osd_frame = None):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create masks for red color
    mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
    mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize coordinates
    coordinates = None

    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Calculate the moments of the largest contour
        M = cv2.moments(largest_contour)
        
        if M["m00"] != 0:
            # Calculate the centroid of the contour
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
            # Get the dimensions of the frame
            height, width, _ = frame.shape

            # Adjust coordinates to make the center of the screen the origin
            cX_centered = cX - width // 2
            cY_centered = height // 2 - cY
            coordinates = (cX_centered, cY_centered)
            
            # Print the coordinates on the frame
            if (osd_frame is not None): 
                cv2.circle(osd_frame, (cX, cY), 1, (0, 0, 255), -1)
                cv2.putText(osd_frame, f"({cX_centered}, {cY_centered})", (cX + 10, cY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Print level colors
    lower_red1_bgr = cv2.cvtColor(np.uint8([[LOWER_RED1]]), cv2.COLOR_HSV2BGR)[0][0]
    cv2.rectangle(osd_frame, (0,0), (50,50), lower_red1_bgr.tolist(), -1)
    upper_red1_bgr = cv2.cvtColor(np.uint8([[UPPER_RED1]]), cv2.COLOR_HSV2BGR)[0][0]
    cv2.rectangle(osd_frame, (50,0), (100,50), upper_red1_bgr.tolist(), -1)
    lower_red2_bgr = cv2.cvtColor(np.uint8([[LOWER_RED2]]), cv2.COLOR_HSV2BGR)[0][0]
    cv2.rectangle(osd_frame, (0,50), (50,100), lower_red2_bgr.tolist(), -1)
    upper_red2_bgr = cv2.cvtColor(np.uint8([[UPPER_RED2]]), cv2.COLOR_HSV2BGR)[0][0]
    cv2.rectangle(osd_frame, (50,50), (100,100), upper_red2_bgr.tolist(), -1)

    return coordinates
