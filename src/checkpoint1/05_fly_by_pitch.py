import airsim
import time
import math

# Select which drone
which_drone = ''

# Initialize the drone client
client = airsim.MultirotorClient()

# Confirm the connection
client.confirmConnection()

# Enable API control
client.enableApiControl(True, which_drone)

# Arm the drone
client.armDisarm(True, which_drone)

# Takeoff
client.takeoffAsync(5, which_drone).join()

# Fly right with roll angle of 10 degrees
client.moveByRollPitchYawZAsync(math.radians(5), 0, 0, -2.5, 2.5, which_drone).join()

time.sleep(5)

# Fly forward with pitch angle of 15 degrees
client.moveByRollPitchYawZAsync(0, math.radians(5), 0, -2.5, 10, which_drone).join()

# Delay so drone can settle before landing
time.sleep(5)

# Land
client.landAsync(30, which_drone).join()