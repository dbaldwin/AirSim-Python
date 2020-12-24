import airsim
import cv2
from cv2 import aruco
import time

class ArucoUtils:

    def __init__(self, client, cameraType):
        self.client = client
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
        self.aruco_params = aruco.DetectorParameters_create()
        self.cameraType = cameraType

    # Get images from AirSim API
    def getVideoFrame(self):

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
            rawImage = self.client.simGetImage("0", self.cameraType)

            if (rawImage == None):
                print("Camera is not returning image, please check airsim for error messages")
                sys.exit(0)
            else:
                png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
                cv2.putText(png, 'FPS ' + str(fps), textOrg, fontFace, fontScale, (255,0,255), thickness)

                gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)

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
                        cv2.line(png, topLeft, topRight, (0, 255, 0), 2)
                        cv2.line(png, topRight, bottomRight, (0, 255, 0), 2)
                        cv2.line(png, bottomRight, bottomLeft, (0, 255, 0), 2)
                        cv2.line(png, bottomLeft, topLeft, (0, 255, 0), 2)

                        # Place a dot in the center of the marker
                        cx = int((topLeft[0] + bottomRight[0])/2)
                        cy = int((topLeft[1] + bottomRight[1])/2)
                        cv2.circle(png, (cx, cy), 3, (0, 0, 255), -1)

                        # Display marker ID
                        cv2.putText(png, str(markerID), (topLeft[0], topLeft[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Display the video frame
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