"""
We're trying to get the camera pose so we can do some autonomous positioning. This script allows the user to move the drone around using keyboard commands, while observing the esimate pose on the markers.
"""
import airsim
import cv2
from cv2 import aruco
import pickle
from threading import Thread

# Open the calibration parameter file created from step 3
calibration = open('.\src\calibration\calibration.pckl', 'rb')

# Grab the data and store it in variables
cameraMatrix, distCoeffs = pickle.load(calibration)

# Close the file
calibration.close()

# Default aruco dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

# Create the airsim client
flyClient = airsim.MultirotorClient()
flyClient.confirmConnection()
flyClient.enableApiControl(True)
flyClient.armDisarm(True)

# Takeoff thread
def takeoff():
    t = Thread(target=flyClient.takeoffAsync())
    t.start()

# Fly thread
def fly(direction):
    """
    +x = forward
    -x = backward
    +y = right
    -y = left
    +z = down
    -z = up
    duration = set to 1 for a second of movement
    """

    duration = 1 # Second
    velocity = 0.5

    t = Thread()

    if (direction == 'forward'):
        t = Thread(target=flyClient.moveByVelocityAsync(velocity, 0, 0, duration))
    elif (direction == 'left'):
        t = Thread(target=flyClient.moveByVelocityAsync(0, -velocity, 0, duration))
    elif (direction == 'backward'):
        t = Thread(target=flyClient.moveByVelocityAsync(-velocity, 0, 0, duration))
    elif (direction == 'right'):
        t = Thread(target=flyClient.moveByVelocityAsync(0, velocity, 0, duration))
    elif (direction == 'up'):
        t = Thread(target=flyClient.moveByVelocityAsync(0, 0, -0.25, duration))
    elif (direction == 'down'):
        t = Thread(target=flyClient.moveByVelocityAsync(0, 0, .25, duration))

    t.start()


# Client for gathering images from camera
imageClient = airsim.MultirotorClient()

# Loop and get the images
while True:

    # because this method returns std::vector<uint8>, msgpack decides to encode it as a string unfortunately.
    rawImage = imageClient.simGetImage("0", airsim.ImageType.Scene)

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
        for id, rvec, tvec in zip(ids, rvecs, tvecs):

            # Draw axes
            aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, 1)

            # The tvec of the marker is the x/y/z translation from the camera center
            tvec = tvec.flatten()
            x, y, z = tvec
            print('Marker: ', id, 'x: ', x, 'y: ', y, 'z: ', z)

    # Show the pose
    cv2.imshow('Pose', frame)


    # Listen for key presses to control drone or quit script
    key = cv2.waitKey(1) & 0xFF

    # Let's use specific key strokes to control the drone - WASD
    if(key == ord('t')):
        takeoff()
    elif (key == ord('w')):
        fly('forward')
    elif (key == ord('a')):
        fly('left')
    elif (key == ord('s')):
        fly('backward')
    elif (key == ord('d')):
        fly('right')
    elif(key == ord('e')):
        fly('up')
    elif(key == ord('q')):
        fly('down')
    # Escape or x will exit the script
    elif (key == 27 or key == ord('x')):
        break

