import airsim
import cv2
from cv2 import aruco
from aruco.ArucoUtils import ArucoUtils
import time
from threading import Thread

# Create aruco chessboard then we load it into Unreal
# aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
# board = cv2.aruco.CharucoBoard_create(3, 3, .025, .0125, aruco_dict)
# image_board = board.draw((200 * 3, 200 * 3))
# cv2.imwrite('charuco.png', image_board)

# Initialize the drone object
drone = airsim.MultirotorClient()
drone.confirmConnection()
drone.enableApiControl(True)
drone.armDisarm(True)

counter = 0

def moveAround():
    getCalibrationImages()
    drone.takeoffAsync().join()
    getCalibrationImages()
    drone.moveToPositionAsync(1, 0, 0, 1, 60).join()
    getCalibrationImages()
    drone.moveToPositionAsync(0, -5, 0, 1, 60).join()
    getCalibrationImages()
    drone.moveToPositionAsync(0, 0, -2, 1, 60).join()
    #drone.moveToPositionAsync(0, 0, 2, 1, 60).join()
    getCalibrationImages()
    drone.rotateToYawAsync(-5).join()
    getCalibrationImages()
    drone.rotateToYawAsync(-10).join()
    getCalibrationImages()
    drone.rotateToYawAsync(-20).join()
    getCalibrationImages()
    drone.rotateToYawAsync(-30).join()
    getCalibrationImages()

def getCalibrationImages():

    global counter

    aruco = ArucoUtils(drone, 'scene')

    for i in range(3):

        counter = counter + 1

        # Get the camera frame
        frame = aruco.getFrame()

        # Show it
        cv2.imshow('Camera', frame)

        # Save it
        cv2.imwrite('.\src\calibration_images\image' + str(counter) + '.jpg', frame)

        # Wait 1 second before the next loop
        cv2.waitKey(1000)

moveThread = Thread(target=moveAround)
moveThread.start()