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

# Fly right
client.moveByVelocityAsync(0, 1, 0, 4, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), which_drone).join()

# Yaw right and then fly left through the ring
client.moveByVelocityAsync(2.5, 0, 0, 16, airsim.DrivetrainType.MaxDegreeOfFreedom,  airsim.YawMode(False, 90), which_drone).join()

# Delay so drone can settle before landing
time.sleep(3)

# Land
client.landAsync(30, which_drone).join()