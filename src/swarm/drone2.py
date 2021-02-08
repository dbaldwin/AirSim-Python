import airsim
import time

# Select which drone
which_drone = 'Drone2'

# Initialize the drone client
client = airsim.MultirotorClient()

# Execute the mission
client.enableApiControl(True, which_drone)
client.takeoffAsync(5, which_drone).join()

client.moveToPositionAsync(0, 2, 0, 2, 600, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), -1, 1, which_drone).join()

time.sleep(3)

client.moveToPositionAsync(-2, 2, 0, 2, 600, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), -1, 1, which_drone).join()

time.sleep(3)

client.moveToPositionAsync(-2, 0, 0, 2, 600, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), -1, 1, which_drone).join()

time.sleep(3)

client.moveToPositionAsync(0, 0, 0, 2, 600, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), -1, 1, which_drone).join()

time.sleep(3)

client.landAsync(10, which_drone).join()