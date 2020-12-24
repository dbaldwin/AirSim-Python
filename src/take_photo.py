import airsim
import os

client = airsim.MultirotorClient()
responses = client.simGetImages([airsim.ImageRequest(1, airsim.ImageType.Scene)])
airsim.write_file(os.path.normpath("photo.jpg"), responses[0].image_data_uint8)  
