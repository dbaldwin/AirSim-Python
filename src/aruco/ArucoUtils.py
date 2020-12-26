import airsim
import cv2
from cv2 import aruco
import time

class ArucoUtils:

    imageTypes = { 
        "depth": airsim.ImageType.DepthVis,
        "segmentation": airsim.ImageType.Segmentation,
        "seg": airsim.ImageType.Segmentation,
        "scene": airsim.ImageType.Scene,
        "disparity": airsim.ImageType.DisparityNormalized,
        "normals": airsim.ImageType.SurfaceNormals
    }

    def __init__(self):
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
        self.aruco_params = aruco.DetectorParameters_create()
        self.font_face = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5

    # Get images from AirSim API
    def getVideoFrameAndDrawMarkers(self, client, imageType):

        # Display FPS
        thickness = 2
        textSize, baseline = cv2.getTextSize("FPS", self.font_face, self.font_scale, thickness)
        textOrg = (10, 10 + textSize[1])
        frameCount = 0
        startTime = time.time()
        fps = 0

        # Infinite loop
        while True:

            # because this method returns std::vector<uint8>, msgpack decides to encode it as a string unfortunately.
            rawImage = client.simGetImage("0", self.imageTypes[imageType])

            if (rawImage == None):
                print("Camera is not returning image, please check airsim for error messages")
                sys.exit(0)
            else:
                png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
                cv2.putText(png, 'FPS ' + str(fps), textOrg, self.font_face, self.font_scale, (255,0,255), thickness)

                # Pass the image into the detection function to draw boundaries
                self.drawMarkers(png)

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

    def getFrame(self):

        rawImage = self.client.simGetImage("0", self.cameraType)

        if rawImage is None:
            print("No image returned")
            sys.exit(0)
        else:
            # Decode the image
            png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)

        return png


    def drawMarkers(self, image):

        # Convert the frame to gray
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect maker corners and ids
        corners, ids, rejected = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)

        # If markers are detected
        if ids is not None:

            ids = ids.flatten()

            # Loop through the makers and draw
            for (markerCorner, markerID) in zip(corners, ids):

                # Get the marker corners (returned in TL, TR, BR, BL order)
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
            
                # Convert to integers
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))

                # Draw the bounding box
                cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

                # Place a dot in the center of the marker
                cx = int((topLeft[0] + bottomRight[0])/2)
                cy = int((topLeft[1] + bottomRight[1])/2)
                cv2.circle(image, (cx, cy), 3, (0, 0, 255), -1)

                # Display marker ID
                cv2.putText(image, str(markerID), (topLeft[0], topLeft[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Display the video frame
                cv2.imshow("Video", image)

    def detectPose(self):
        pass
        
