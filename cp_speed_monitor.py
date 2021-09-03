"""
IF20-contact_point_speed by Yuning Sun
1:08 PM 7/1/21
Module documentation: 
"""
import math
import os
import threading
import time

import cv2
import numpy as np

DEFAULT_V = 10
START_X = 60
MIDDLE_RANGE = (200, 400)
LAG_WIDTH = 3
PIXEL_DIFF_THRESHOLD = 2
DISCONTINUOUS_THRESHOLD = 10
LEFT_BIAS = 3
RIGHT_BIAS = 5

# TODO: GET RATIO and DIRECTION
X_RATIO = 1
Y_RATIO = 1


def detect(img):
    # n, m are the size of image
    n, m = len(img), len(img[0])
    # record the position of last pixel in order to reduce calculation
    last_pixel = []
    # since x in range (0, 60) are all black,
    # detection would be start from 60
    x = START_X
    # k is the number of lost pixel
    # because we detect pixel from top to bottom,
    # there may have such situation that image loses a part of lag,
    # and k is the the number of lost x pixel
    # if k is grater that DISCONTINUOUS_THRESHOLD, the program stops
    k = 0
    for j in range(MIDDLE_RANGE[0], MIDDLE_RANGE[1]):
        pixel = img[x][j]
        avg = np.average(img[x][j - LAG_WIDTH: j + LAG_WIDTH])
        if pixel - avg > 2:
            last_pixel.append(j)
    start_point = int(sum(last_pixel) / len(last_pixel))
    max_bias = 0
    y = start_point
    while x < n:
        # this means program detects discontinuous trajectory
        if len(last_pixel) == 0:
            k += 1
        else:
            y = int(sum(last_pixel) / len(last_pixel))
        last_pixel = []
        for j in range(y - LEFT_BIAS, y + RIGHT_BIAS):
            pixel = img[x][j]
            avg = np.average(img[x][j - LAG_WIDTH: j + LAG_WIDTH])
            if pixel - avg > 0:
                last_pixel.append(j)
                max_bias = max(max_bias, abs(j - start_point))
                k = 0
        if k > DISCONTINUOUS_THRESHOLD:
            break
        x += 1
    return start_point, max_bias


class Velocity:
    def __init__(self):
        self._v = DEFAULT_V
        self.last_absolute_v_x = 0
        self.last_absolute_v_y = 0
        self.lag_length = 0

    def set_initial_v(self, v_x, v_y):
        self.last_absolute_v_x = v_x
        self.last_absolute_v_y = v_y

    def get_lag_length(self):
        return self.lag_length

    def update(self, distance_x, distance_y, interval):
        """
        Update relative velocity of lag
        :param distance_x: relative distance in x axis
        :param distance_y: relative distance in y axis
        :param interval: time interval
        :return:
        """
        distance_x = distance_x * X_RATIO
        distance_y = distance_y * Y_RATIO
        self.lag_length = math.sqrt(distance_x ** 2 + distance_y ** 2)
        self.last_absolute_v_x = distance_x / interval
        self.last_absolute_v_y = distance_y / interval

    def get_absolute_v_x(self):
        return self.last_absolute_v_x

    def get_absolute_v_y(self):
        return self.last_absolute_v_y


class CPSpeedMonitor(threading.Thread):
    def __init__(self, v):
        super().__init__()
        self.flag = True
        self.v = v

    def stop(self):
        self.flag = False

    def run(self) -> None:
        capture_x = cv2.VideoCapture(0)
        capture_y = cv2.VideoCapture(1)
        last_time = time.time()
        while self.flag:
            ret, frame_x = capture_x.read()
            ret, frame_y = capture_y.read()
            _, relative_bias_x = detect(frame_x)
            _, relative_bias_y = detect(frame_y)
            current_time = time.time()
            self.v.update(relative_bias_x, relative_bias_y, current_time - last_time)
            last_time = current_time


if __name__ == '__main__':
    # main()
    pass
