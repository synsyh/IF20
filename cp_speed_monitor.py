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


def detect(img):
    n, m = len(img), len(img[0])
    last_pixel = []
    x = START_X
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

    def update(self, v):
        self._v = v

    def get(self):
        return self._v


class CPSpeedMonitor(threading.Thread):
    def __init__(self, v):
        super().__init__()
        self.flag = True
        self.v = v

    def stop(self):
        self.flag = False

    def run(self) -> None:
        capture_v = cv2.VideoCapture(0)
        capture_h = cv2.VideoCapture(1)
        last_v = 0
        last_h = 0
        while self.flag:
            ret, frame_v = capture_v.read()
            ret, frame_h = capture_h.read()
            _, max_bias_v = detect(frame_v)
            _, max_bias_h = detect(frame_h)
            # TODO: time
            self.v.update(math.sqrt((max_bias_h - last_h) ** 2 + (max_bias_v - last_v) ** 2))
            last_h = max_bias_h
            last_v = max_bias_v


if __name__ == '__main__':
    # main()
    pass
