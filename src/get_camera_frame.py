import airsim
import cv2
from aruco.ArucoUtils import ArucoUtils

# Initialize the AirSim client
drone = airsim.MultirotorClient()

# Image types
# "depth", "segmentation", "seg", "scene", "disparity", "normals"
imageType = "scene"

# Initialize the camera view
aruco = ArucoUtils(drone, imageType)

# Grab a frame from the camera
frame = aruco.getFrame()

# Display the frame
cv2.imshow('Camera', frame)

# Wait for a keypress to exit
cv2.waitKey(0)