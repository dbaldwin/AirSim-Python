import airsim
import cv2
from cv2 import aruco
import pickle

# Open the calibration parameter file created from step 3
calibration = open('.\src\calibration\calibration.pckl', 'rb')

# Grab the data and store it in variables
cameraMatrix, distCoeffs = pickle.load(calibration)

# Close the file
calibration.close()

# Default aruco dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

# Create the airsim client
drone = airsim.MultirotorClient()

while True:

    # because this method returns std::vector<uint8>, msgpack decides to encode it as a string unfortunately.
    rawImage = drone.simGetImage("0", airsim.ImageType.Scene)

    if (rawImage == None):
        print("Camera is not returning image, please check airsim for error messages")
        sys.exit(0)

    # Get the frame
    frame = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)

    # Convert the frame to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find markers and corners in the image
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict)

    if ids is not None:
        
        # rvecs and tvecs are the rotation and translation vectors for each of the markers in corners.
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 1, cameraMatrix, distCoeffs)

        # Join and enumerate the vectors
        for rvec, tvec in zip(rvecs, tvecs):
            aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, 1)

        # Show the pose
        cv2.imshow('Pose', frame)

    # Exit on escape or q key
    key = cv2.waitKey(1) & 0xFF
    if (key == 27 or key == ord('q')):
        break