"""
IF20-camera_controller by Yuning Sun
4:36 PM 5/14/21
Module documentation: 
"""
import cv2
import time

# 打开摄像头并灰度化显示
i = 0
capture = cv2.VideoCapture(0)
while True:
    # 获取一帧
    ret, frame = capture.read()
    # print(frame.shape)
    # 将这帧转换为灰度图
    # time.sleep(0.5)
    cv2.imshow('frame', frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # 把输入图像灰度化
    # 直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
    ret, img_binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    cv2.imshow('binary', img_binary)
    # cv2.imwrite('process_{}.png'.format(i), frame)
    i = i + 1
    # print(img_binary.shape)
    # 如果输入q，则退出
    if cv2.waitKey(1) == ord('q'):
        break
