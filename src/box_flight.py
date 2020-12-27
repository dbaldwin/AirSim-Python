"""
This script demonstrates how to fly in a box pattern using different DriveTrain and YawMode types. The coordinates are the same for each pass and it's the YawMode and DriveTrain values that lead to different orientation.
"""
import airsim
import sys
import time

# Initialize the drone client
client = airsim.MultirotorClient()

# Confirm the connection
client.confirmConnection()

# Enable API control
client.enableApiControl(True)

# Arm the drone
client.armDisarm(True)

# Takeoff
client.takeoffAsync().join()

# AirSim uses NED coordinates so negative axis is up.
# -10 meters above the original launch point.
z = -10

# Fly given velocity vector for 5 seconds
duration = 5

# Box with nose pointed towards heading
client.moveByVelocityZAsync(5, 0, z, duration, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0)).join()
time.sleep(2)

client.moveByVelocityZAsync(0, 5, z, duration, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0)).join()
time.sleep(2)

client.moveByVelocityZAsync(-5, 0, z, duration, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0)).join()
time.sleep(2)

client.moveByVelocityZAsync(0, -5, z, duration, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0)).join()
time.sleep(2)

# Reset heading
client.rotateToYawAsync(0)
time.sleep(2)

# Box with nose pointed forward the whole time
client.moveByVelocityZAsync(5, 0, z, duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0)).join()
time.sleep(2)

client.moveByVelocityZAsync(0, 5, z, duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0)).join()
time.sleep(2)

client.moveByVelocityZAsync(-5, 0, z, duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0)).join()
time.sleep(2)

client.moveByVelocityZAsync(0, -5, z, duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0)).join()
time.sleep(2)

# Box with nose pointed towards the inside of the box
client.moveByVelocityZAsync(5, 0, z, duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 90)).join()
time.sleep(2)

client.moveByVelocityZAsync(0, 5, z, duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 180)).join()
time.sleep(2)

client.moveByVelocityZAsync(-5, 0, z, duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 270)).join()
time.sleep(2)

client.moveByVelocityZAsync(0, -5, z, duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0)).join()
time.sleep(2)

# Land
time.sleep(2)
client.landAsync().join()