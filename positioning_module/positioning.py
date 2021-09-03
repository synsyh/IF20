"""
IF20-positioning by Yuning Sun
3:43 PM 7/10/21
Module documentation: 
"""
import cv2
import numpy as np


def read_path():
    x = []
    y = []
    with open('path.txt') as f:
        for line in f.readlines():
            data = line.strip().split('\t')
            x.append(data[0])
            y.append(data[1])
    print()


def read_video_x():
    capture = cv2.VideoCapture('output_x.avi')
    i = 0
    last_position = 345
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter('positioning.mp4', fourcc, 10.0, size)
    while capture.isOpened():
        capture.read()
        ret, frame = capture.read()
        if ret:
            grey_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            new_frame = grey_frame[last_position - 30:last_position + 10, :]
            positions = np.where(new_frame < 50)
            new_positions = positions[0] + positions[1]
            max_index = new_positions.argmax()
            x = positions[0][max_index] + last_position - 30
            y = positions[1][max_index]
            last_position = x
            frame[x - 5:x + 5, y - 5: y + 5] = (0, 0, 255)
            # cv2.imshow('frame', frame)
            out.write(frame)
            # if cv2.waitKey(1) == ord('q'):
            #     break
            i += 1
        else:
            break
    capture.release()
    out.release()
    cv2.destroyAllWindows()


def read_video_y():
    capture = cv2.VideoCapture('output_y.avi')
    i = 0
    last_position = 345
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # out = cv2.VideoWriter('positioning.mp4', fourcc, 10.0, size)
    while capture.isOpened():
        ret, frame = capture.read()
        if ret:
            grey_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            new_frame = grey_frame[last_position - 50:last_position + 10, :]
            positions = np.where(new_frame < 50)
            new_positions = positions[0] - positions[1]
            max_index = new_positions.argmax()
            x = positions[0][max_index] + last_position - 50
            y = positions[1][max_index]
            last_position = x
            frame[x - 5:x + 5, y - 5: y + 5] = (0, 0, 255)
            cv2.imshow('frame', frame)
            # out.write(frame)
            if cv2.waitKey(1) == ord('q'):
                break
            i += 1
        else:
            break
    capture.release()
    # out.release()
    cv2.destroyAllWindows()


def find_position():
    frame = cv2.imread('x.jpg')
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    frame[frame > 100] = 255
    cv2.imshow('frame', frame)
    cv2.waitKey()
    cv2.destroyAllWindows()
    print()


if __name__ == '__main__':
    read_video_y()
