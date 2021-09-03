"""
IF20-monitor_test by Yuning Sun
5:06 PM 8/18/21
Module documentation: 
"""
import cv2
import numpy as np

START_X = 60
MIDDLE_RANGE = (200, 400)
LAG_WIDTH = 3
LEFT_BIAS = 3
RIGHT_BIAS = 5
DISCONTINUOUS_THRESHOLD = 10

capture = cv2.VideoCapture(0)
while True:
    _, img = capture.read()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
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
    img[:, start_point] = (255, 0, 0)
    img[:, start_point - max_bias] = (0, 0, 255)
    cv2.imshow('detect', img)
    if cv2.waitKey(1) == ord('q'):
        break
