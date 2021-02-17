import airsim
import math
import time

# Initialize the drone client
client = airsim.MultirotorClient()

# Confirm the connection
client.confirmConnection()

# Enable API control
client.enableApiControl(True)

# Takeoff and wait
client.takeoffAsync().join()

# Wait for input
airsim.wait_key("Press any key to begin the pitch sequence")

# Pitch up in 15 degree increments
for i in range(6):
    
    camera_pitch = (i + 1) * 15
    
    print("Pitching camera to: " + str(camera_pitch))

    # Set the camera pose based on pitch
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(math.radians(camera_pitch), 0, 0))

    # Pitch the camera
    client.simSetCameraPose("0", camera_pose)

    # Sleep
    time.sleep(1)

# Pitch down in 15 degree increments
for i in range(6):
    
    camera_pitch = (i + 1) * -15
    
    print("Pitching camera to: " + str(camera_pitch))

    # Set the camera pose based on pitch
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(math.radians(camera_pitch), 0, 0))

    # Pitch the camera
    client.simSetCameraPose("0", camera_pose)

    # Sleep
    time.sleep(1)

print("Done")