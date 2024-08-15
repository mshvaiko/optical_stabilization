# Description: This file contains the code to track an object in a video stream using ORB algorytm.

import cv2
import numpy as np

TARGET_IMAGE = r'.\assets\flying_drone_example.png'

# Initiate ORB
orb = None
bf = None
keypoints_1 = None
descriptors_1 = None

def init_orb():
    global orb, bf, keypoints_1, descriptors_1
    orb = cv2.ORB_create()
    bf = cv2.BFMatcher()

    # Load the target image
    image = cv2.imread(TARGET_IMAGE)
    gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    rgb_image =cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    cv2.imshow('Input Image', rgb_image)

    # find the keypoints with ORB
    keypoints_1, descriptors_1 = orb.detectAndCompute(gray_image, None)

    # draw only keypoints location,not size and orientation
    img2 = cv2.drawKeypoints(rgb_image, keypoints_1, None, color=(0,255,0), flags=0)

    # Display the image with the keypoints
    cv2.imshow('Image', img2)

def process_frame(frame):
    # Init ORB if needed
    if orb is None:
        init_orb()

    # Initialize coordinates
    coordinates = None

    # convert frame to gray scale 
    frame_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    # compute the descriptors with BRIEF
    keypoints_2, descriptors_2 = orb.detectAndCompute(frame_gray, None)
    
    # Initialize list to store coordinates
    coord_array = []

    if descriptors_2 is not None:
        matches = bf.match(descriptors_1, descriptors_2)
        for match in matches:
            # .trainIdx gives keypoint index from current frame 
            train_idx = match.trainIdx
            
            # current frame keypoints coordinates
            pt2 = keypoints_2[train_idx].pt

            # Append coordinates to the list
            coord_array.append(pt2)
            
            # draw circle to pt2 coordinates , because pt2 gives current frame coordinates
            cv2.circle(frame,(int(pt2[0]),int(pt2[1])),2,(255,0,0),2)

    # Get the center of the major cluster
    cX, cY = None, None
    if coord_array:
        major_cluster_center = get_major_cluster_center(coord_array)
        if major_cluster_center:
            cX, cY = int(major_cluster_center[0]), int(major_cluster_center[1])
    if (cX is None) or (cY is None):
        return None

    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Adjust coordinates to make the center of the screen the origin
    cX_centered = cX - width // 2
    cY_centered = height // 2 - cY
    coordinates = (cX_centered, cY_centered)

    # Print the coordinates on the frame
    cv2.circle(frame, (int(cX), int(cY)), 1, (0, 0, 255), -1)
    cv2.putText(frame, f"({cX_centered}, {cY_centered})", (cX + 10, cY + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    return coordinates

def get_major_cluster_center(points, radius=50, min_cluster_size=30):
    """
    Get the center of the major cluster, ignoring small clusters that produce noise.

    :param points: List of points (x, y).
    :param radius: Radius to consider for density calculation.
    :param min_cluster_size: Minimum size of a cluster to be considered as major.
    :return: Center of the major cluster or None if no cluster meets the minimum size.
    """
    points_array = np.array(points)
    max_density = 0
    best_center = None

    for point in points_array:
        # Calculate distances from the current point to all other points
        distances = np.linalg.norm(points_array - point, axis=1)
        
        # Count points within the specified radius
        density = np.sum(distances < radius)
        
        # Update the best center if the current point has a higher density
        if density > max_density:
            max_density = density
            best_center = point

    # Check if the best cluster meets the minimum size requirement
    if max_density < min_cluster_size:
        return None

    # Calculate the mean of the points within the radius of the best center
    distances = np.linalg.norm(points_array - best_center, axis=1)
    in_radius_points = points_array[distances < radius]
    center_x, center_y = np.mean(in_radius_points, axis=0)
    return center_x, center_y