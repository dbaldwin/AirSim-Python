import airsim
import cv2
import time
import sys
from threading import Thread # So we can get the camera feed and send commands in parallel
from cv2 import aruco

# Setup default camera
cameraType = "scene"

# All camera types
cameraTypeMap = { 
 "depth": airsim.ImageType.DepthVis,
 "segmentation": airsim.ImageType.Segmentation,
 "seg": airsim.ImageType.Segmentation,
 "scene": airsim.ImageType.Scene,
 "disparity": airsim.ImageType.DisparityNormalized,
 "normals": airsim.ImageType.SurfaceNormals
}

aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
aruco_params = aruco.DetectorParameters_create()

# Get images from AirSim API
def getVideoFrame():

    # Display FPS
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    thickness = 2
    textSize, baseline = cv2.getTextSize("FPS", fontFace, fontScale, thickness)
    textOrg = (10, 10 + textSize[1])
    frameCount = 0
    startTime = time.time()
    fps = 0

    # Infinite loop
    while True:

        # because this method returns std::vector<uint8>, msgpack decides to encode it as a string unfortunately.
        rawImage = client.simGetImage("0", cameraTypeMap[cameraType])

        if (rawImage == None):
            print("Camera is not returning image, please check airsim for error messages")
            sys.exit(0)
        else:
            png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
            cv2.putText(png, 'FPS ' + str(fps), textOrg, fontFace, fontScale, (255,0,255), thickness)

            (H, W) = png.shape[:2]

            #cv2.circle(png, center=(png.shape[1]-10, 10), radius=4, color=(0, 255, 0), thickness=-1)
            
            gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)

            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

            # If markers are detected
            if ids is not None:

                # Enumerate each marker and draw its boundaries
                for i in range(len(ids)):
                    cv2.line(png, tuple(corners[i][0][0]), tuple(corners[i][0][1]), (0, 255, 0), 2)
                    cv2.line(png, tuple(corners[i][0][1]), tuple(corners[i][0][2]), (0, 255, 0), 2)
                    cv2.line(png, tuple(corners[i][0][2]), tuple(corners[i][0][3]), (0, 255, 0), 2)
                    cv2.line(png, tuple(corners[i][0][3]), tuple(corners[i][0][0]), (0, 255, 0), 2)

                    # Draw marker id
                    x = int(corners[i][0][1][0]) + 5
                    y = int(corners[i][0][0][1]) + 10
                    cv2.putText(png, str(ids[i][0]), (x, y), fontFace, fontScale, (255, 0, 255), thickness)



            cv2.imshow("Video", png)

        frameCount  = frameCount  + 1
        endTime = time.time()
        diff = endTime - startTime
        if (diff > 1):
            fps = frameCount
            frameCount = 0
            startTime = endTime
    
        # Quit on q or x
        key = cv2.waitKey(1) & 0xFF
        if (key == 27 or key == ord('q') or key == ord('x')):
            break


# Establish connection with AirSim
client = airsim.MultirotorClient()
# client.confirmConnection()
# client.enableApiControl(True)
# client.armDisarm(True)

# Takeoff
#client.takeoffAsync().join()

# Begin the video thread
videoThread = Thread(target=getVideoFrame)
videoThread.start()

time.sleep(1)

# Fly to the ArUco Tower
#client.moveToPositionAsync(220, -15, 35, 10)
