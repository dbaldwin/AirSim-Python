import airsim
import sys
from threading import Thread # So we can get the camera feed and send commands in parallel
from aruco.ArucoUtils import ArucoUtils
import time

set# Establish connection with AirSim
client = airsim.MultirotorClient()
#client.confirmConnection()
#client.enableApiControl(True)
#client.armDisarm(True)

# Takeoff
#client.takeoffAsync().join()

# Begin the video thread
aruco = ArucoUtils()
videoThread = Thread(target=aruco.getVideoFrameAndDrawMarkers(client, 'scene'))
videoThread.start()

# Pause before we go
#time.sleep(3)

# Fly to the ArUco Tower
#client.moveToPositionAsync(220, -15, 35, 10)
