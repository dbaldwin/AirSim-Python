import airsim
import math
import time

# The limitation of this demo is that the drone body will be in the image frame

# Initialize the drone client
client = airsim.MultirotorClient()

# Confirm the connection
client.confirmConnection()

# Enable API control
client.enableApiControl(True)

# Takeoff and wait
client.takeoffAsync().join()

# Wait for input
airsim.wait_key("Press any key to begin the yaw sequence")

# Yaw from 0 to 360 in 60 degree increments
for i in range(6):
    camera_yaw = (i + 1) * 60
    print("Yawing camera to: " + str(camera_yaw))

    # Set the camera pose based on yaw
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, math.radians(camera_yaw)))

    # Yaw the camera
    client.simSetCameraPose("0", camera_pose)

    # Sleep
    time.sleep(1)

print("Done")