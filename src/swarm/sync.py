import airsim
import time

# Initialize the drone client
client = airsim.MultirotorClient()

# Execute the mission
client.enableApiControl(True, 'Drone1')
client.enableApiControl(True, 'Drone2')

client.takeoffAsync(5, 'Drone1')
client.takeoffAsync(5, 'Drone2').join()

client.moveToPositionAsync(-2, 0, 0, 2, 600, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), -1, 1, 'Drone1')
client.moveToPositionAsync(-2, 0, 0, 2, 600, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), -1, 1, 'Drone2').join()

client.moveToPositionAsync(-2, 2, 0, 2, 600, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), -1, 1, 'Drone1')
client.moveToPositionAsync(-2, -2, 0, 2, 600, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), -1, 1, 'Drone2').join()

client.moveToPositionAsync(0, 0, 0, 2, 600, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), -1, 1, 'Drone1')
client.moveToPositionAsync(0, 0, 0, 2, 600, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0), -1, 1, 'Drone2').join()

time.sleep(3)

client.landAsync(10, 'Drone1')
client.landAsync(10, 'Drone2')