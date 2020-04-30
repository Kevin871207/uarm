import cv2
import numpy as np

dispW=640
dispH=480
flip=2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

board_size = 7
error = 25  # detect
board_pos = []
one_x=74
one_y=354
x_error=3
y_error=2
for x in range(0, 7):
    for y in range(0, 7):
        n=one_x+x*55-(x_error*y)
        m=one_y-y*50-(y_error*x) 
        board_pos.append((n, m))


def pos_to_2d(pos):
    return int(pos % 7), int(pos / 7)


def get_board(debug):
    cam= cv2.VideoCapture(camSet)
    ret, frame = cam.read()
    crop_img=frame[50:450,100:530]
    cv2.imwrite("board.png", crop_img)

    board = np.zeros((7, 7), dtype='u1')

    img = cv2.imread('board.png', 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('grayboard.png', gray)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=100, param2=25, minRadius=20, maxRadius=45)
    # circles = np.uint16(np.around(circles))
    circles = np.around(circles).astype(np.uint16)

    black_c, white_c = 0, 0
    black_pos = []
    white_pos = []

    for i in circles[0, :]:
        cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 255), 1)
        if img[i[1], i[0]][0]-5 > 150 or img[i[1], i[0]][1]-5 > 150 or img[i[1], i[0]][2]-5 > 150:
            white_c += 1
            white_pos.append((i[0], i[1]))
        else:
    	    black_c += 1
    	    black_pos.append((i[0], i[1]))
    for b_pos in black_pos:
        for pos in board_pos:
            if pos[0] + error > b_pos[0] > pos[0] - error and pos[1] + error > b_pos[1] > pos[1] - error:
                px, py = pos_to_2d(board_pos.index(pos))
                board[6-px][py] = 1
                py+=65
                py=chr(py)
#                print('black {} {:d}'.format(py,px+1))

    for w_pos in white_pos:
        for pos in board_pos:
            if pos[0] + error > w_pos[0] > pos[0] - error and pos[1] + error > w_pos[1] > pos[1] - error:
                px, py = pos_to_2d(board_pos.index(pos))
                board[6-px][py] = 2
                py+=65
                py=chr(py)
#                print("white {} {:d}".format(py,px+1))
    if debug:
            cv2.imshow('detected circles', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    return board


def get_move(server_board, img_board, color):
    move = None
    if color == "B":
        color = 1
    else:
        color = 2
    for px in range(7):
        for py in range(7):
            if img_board[px][py] != server_board[px][py] and img_board[px][py] == color:
                move = chr(py+65)+ str(7 - px)
    return move
