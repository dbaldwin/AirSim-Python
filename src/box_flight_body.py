"""
This script demonstrates how to fly in a box pattern using the local (body) frame.
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

# Let's yaw a little so we can tell the difference
client.rotateToYawAsync(45).join()

client.moveByVelocityBodyFrameAsync(5, 0, 0, duration).join()
time.sleep(2)

client.moveByVelocityBodyFrameAsync(0, 5, 0, duration).join()
time.sleep(2)

client.moveByVelocityBodyFrameAsync(-5, 0, 0, duration).join()
time.sleep(2)

client.moveByVelocityBodyFrameAsync(0, -5, 0, duration).join()
time.sleep(2)

# Reset heading
client.rotateToYawAsync(0).join()

# Land
time.sleep(2)
client.landAsync().join()