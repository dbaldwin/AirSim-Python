import cv2
from cv2 import aruco

# Create aruco chessboard then we load it into Unreal
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
board = aruco.CharucoBoard_create(3, 3, .025, .0125, aruco_dict)
image_board = board.draw((200 * 3, 200 * 3))
cv2.imwrite('.\src\calibration\charuco.png', image_board)