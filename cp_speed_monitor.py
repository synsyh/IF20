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


def read_img(root):
    for file_path, dirs, fs in os.walk(root):
        fs = sorted(fs)
        for f in fs:
            file = os.path.join(file_path, f)
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)


def detect(img):
    # track = np.zeros(shape=(480, 640))
    n, m = len(img), len(img[0])
    last_pixel = []
    x = 60
    k = 0
    for j in range(200, 400):
        pixel = img[x][j]
        avg = np.average(img[x][j - 3: j + 3])
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
        # track[x, y] = 255
        last_pixel = []
        for j in range(y - 3, y + 5):
            pixel = img[x][j]
            avg = np.average(img[x][j - 3: j + 3])
            if pixel - avg > 0:
                last_pixel.append(j)
                max_bias = max(max_bias, abs(j - start_point))
                k = 0
        if k > 10:
            break
        x += 1
    # cv2.imwrite('detect_v/' + img_path, track)
    return start_point, max_bias


def detect_all():
    time_start = time.time()
    for file_path, dirs, fs in os.walk('V'):
        fs = sorted(fs)
        for f in fs:
            file = os.path.join(file_path, f)
            img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
            start_point, max_bias = detect(img)
            img = cv2.imread(file)
            img[:, start_point] = (255, 0, 0)
            img[:, start_point - max_bias] = (0, 0, 255)
            cv2.imwrite('detect_v/' + file, img)
    time_end = time.time()
    time_cost = time_end - time_start
    print(time_cost)
    print(time_cost / len(fs))


def mark():
    img = cv2.imread('V/170.jpg')
    img[240][320] = (0, 0, 255)
    cv2.imshow('mark', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    detect_all()


class Velocity:
    def __init__(self):
        self.v = DEFAULT_V

    def update(self, v):
        self.v = v

    def get(self):
        return self.v


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
            self.v.update(math.sqrt((max_bias_h - last_h) ** 2 + (max_bias_v - last_v) ** 2))
            last_h = max_bias_h
            last_v = max_bias_v


if __name__ == '__main__':
    main()
