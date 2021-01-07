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
client.takeoffAsync(30, which_drone).join()

# Fly right
client.moveByVelocityAsync(0, 1, 0, 4, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), which_drone).join()

# Fly forward through ring
client.moveByVelocityAsync(5, 0, 0, 9, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), which_drone).join()

#client.moveByMotorPWMsAsync(1, 0.5, 0.5, 1, 5).join()

time.sleep(3)

# Land
client.landAsync(30, which_drone).join()