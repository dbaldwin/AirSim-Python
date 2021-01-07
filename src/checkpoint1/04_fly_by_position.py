import airsim
import time

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

# Fly right - NED/XYZ
client.moveToPositionAsync(0, 3, 0, 2).join()

# Talk about why this doesn't work with y=0
#client.moveToPositionAsync(39, 0, 0, 5).join()

# Fly to checkoiut using XYZ coords
client.moveToPositionAsync(39, 4, -3, 5).join()

# Delay so drone can settle before landing
time.sleep(3)

# Land
client.landAsync(30, which_drone).join()