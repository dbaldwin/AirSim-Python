import airsim
import sys
from threading import Thread # So we can get the camera feed and send commands in parallel
from aruco.ArucoUtils import ArucoUtils

# Establish connection with AirSim
client = airsim.MultirotorClient()
# client.confirmConnection()
# client.enableApiControl(True)
# client.armDisarm(True)

# Takeoff
#client.takeoffAsync().join()

temp = ArucoUtils(client, "scene")
temp.getVideoFrame()

#print(temp.getFrame())

# Begin the video thread
# videoThread = Thread(target=getVideoFrame)
# videoThread.start()

# time.sleep(1)

# Fly to the ArUco Tower
#client.moveToPositionAsync(220, -15, 35, 10)
