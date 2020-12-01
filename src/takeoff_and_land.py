import airsim

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

# Hover for a few
client.hoverAsync().join()

# Land
client.landAsync().join()