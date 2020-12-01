import airsim

client = airsim.MultirotorClient()
state = client.getMultirotorState()

# Print the different components of the state object
collision = state.collision
print("Collision: ")
print(collision)
print("-------------------------------------------------------")

kinematics_estimated = state.kinematics_estimated
print("Kinematics: ")
print(kinematics_estimated)
print("-------------------------------------------------------")

gps = state.gps_location
print("GPS: ")
print(gps)
print("-------------------------------------------------------")

landed_state = state.landed_state
print("Landed state: ")
print(landed_state)
print("-------------------------------------------------------")

timestamp = state.timestamp
print("Timestamp: ")
print(timestamp)
print("-------------------------------------------------------")

ready = state.ready
print("Ready: ")
print(ready)
print("-------------------------------------------------------")

ready_message = state.ready_message
print("Ready message: ")
print(ready_message)
print("-------------------------------------------------------")

can_arm = state.can_arm
print("Can arm: ")
print(can_arm)
print("-------------------------------------------------------")

rc_data = state.rc_data
print("RC data: ")
print(rc_data)
print("-------------------------------------------------------")


# inematicsState()
#     gps_location = GeoPoint()
#     timestamp = np.uint64(0)
#     landed_state = LandedState.Landed
#     rc_data = RCData()
#     ready = False
#     ready_message = ""
#     can_arm = False

# Print collision info
#print(state.collision)
#print(state.ready)