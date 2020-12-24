import airsim
import sys
from threading import Thread # So we can get the camera feed and send commands in parallel
from aruco.ArucoUtils import ArucoUtils

# Setup default camera
cameraType = "scene"

# All camera types
cameraTypeMap = { 
 "depth": airsim.ImageType.DepthVis,
 "segmentation": airsim.ImageType.Segmentation,
 "seg": airsim.ImageType.Segmentation,
 "scene": airsim.ImageType.Scene,
 "disparity": airsim.ImageType.DisparityNormalized,
 "normals": airsim.ImageType.SurfaceNormals
}

# Establish connection with AirSim
client = airsim.MultirotorClient()
# client.confirmConnection()
# client.enableApiControl(True)
# client.armDisarm(True)

# Takeoff
#client.takeoffAsync().join()

temp = ArucoUtils(client, cameraTypeMap[cameraType])
temp.getVideoFrame()

# Begin the video thread
# videoThread = Thread(target=getVideoFrame)
# videoThread.start()

# time.sleep(1)

# Fly to the ArUco Tower
#client.moveToPositionAsync(220, -15, 35, 10)
