"""
IF20-camera_positioning by Yuning Sun
4:28 PM 7/15/21
Module documentation: 
"""
import cv2
import numpy as np
import serial


def positioning_x(capture, last_position=345):
    x, y = 0, 0
    if capture.isOpened():
        ret, frame = capture.read()
        if ret:
            grey_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            new_frame = grey_frame[last_position - 30:last_position + 10, :]
            positions = np.where(new_frame < 50)
            new_positions = positions[0] + positions[1]
            max_index = new_positions.argmax()
            x = positions[0][max_index] + last_position - 30
            y = positions[1][max_index]
    return x, y


def positioning_y(capture, last_position=345):
    x, y = 0, 0
    if capture.isOpened():
        ret, frame = capture.read()
        if ret:
            grey_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            new_frame = grey_frame[last_position - 50:last_position + 10, :]
            positions = np.where(new_frame < 50)
            new_positions = positions[0] - positions[1]
            max_index = new_positions.argmax()
            x = positions[0][max_index] + last_position - 50
            y = positions[1][max_index]
    return x, y


def camera_positioning(cmd):
    serial_port = serial.Serial('COM3', baudrate=9600, timeout=0.1)
    serial_port.read()
    receiver = '^'
    capture_v = cv2.VideoCapture(0)
    capture_h = cv2.VideoCapture(1)
    last_position_v = 345
    last_position_h = 345
    vs, hs = [], []
    cmds = []
    for i in range(len(cmd)):
        while '^' not in str(receiver):
            receiver = serial_port.read()
        vx, vy = positioning_x(capture_v, last_position_v)
        vs.append((vx, vy))
        last_position_v = vx
        hx, hy = positioning_y(capture_h, last_position_h)
        last_position_h = hx
        hs.append((hx, hy))
        cmds.append(cmd)
        serial_port.write(cmd[i].encode())
        receiver = serial_port.read()
    serial_port.close()
    capture_v.release()
    capture_h.release()
    with open('positions.txt', 'w') as f:
        for i in range(len(vs)):
            f.write(str(vs[i]) + '\t' + str(hs[i]) + '\t' + cmds[i] + '\r\n')
