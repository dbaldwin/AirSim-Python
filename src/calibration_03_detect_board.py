import os
import cv2
from cv2 import aruco
import pickle

# Default aruco dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

# Create the board
# Must be the same board loaded into AirSim for calibration
charuco_board = aruco.CharucoBoard_create(3, 3, .025, .0125, aruco_dict)

# Store all found corners and ids
all_corners = []
all_ids = []

# Loop over the calibration images and detect markers
for subdir, dirs, files in os.walk('.\src\calibration\images'):

    # Loop over the files in the directory
    for file in files:

        # Read into a variable
        frame = cv2.imread(subdir + '\\' + file)

        # Covert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the markers
        corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict)
        
        # Now let's detect the charuco corners
        if ids is not None:
            num_markers, inter_corners, inter_ids = cv2.aruco.interpolateCornersCharuco(corners, ids, gray, charuco_board)

            if num_markers > 0:
                all_corners.append(inter_corners)
                all_ids.append(inter_ids)

# Let's do the calibration
try:
    cal = aruco.calibrateCameraCharuco(all_corners, all_ids, charuco_board, gray.shape, None, None)
except:
    print("Error calibrating")

# Get the calibration result
retval, cameraMatrix, distCoeffs, rvecs, tvecs = cal

# Save the camera calibration params
f = open('.\src\calibration\calibration.pckl', 'wb')
pickle.dump((cameraMatrix, distCoeffs), f)
f.close()