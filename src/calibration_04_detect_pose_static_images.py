import cv2
from cv2 import aruco
import pickle
import os

# Open the calibration parameter file created from step 3
calibration = open('.\src\calibration\calibration.pckl', 'rb')

# Grab the data and store it in variables
cameraMatrix, distCoeffs = pickle.load(calibration)

# Close the file
calibration.close()

# Default aruco dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

# Loop over the calibration images and detect markers
for subdir, dirs, files in os.walk('.\src\calibration\images'):

    for file in files:

        # Read into a variable
        frame = cv2.imread(subdir + '\\' + file)

        # Covert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the markers
        corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict)

        if ids is not None:

            # rvecs and tvecs are the rotation and translation vectors for each of the markers in corners.
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 1, cameraMatrix, distCoeffs)

            for rvec, tvec in zip(rvecs, tvecs):
                aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, 1)

        # Display the pose
        cv2.imshow('frame', frame)

        # Pause before the next frame
        cv2.waitKey(3000)