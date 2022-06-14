import math

import numpy as np
from PIL import Image


def get_result_arr():
    img_array = []
    with Image.open('without_circle.jpg') as img:
        img_array = np.array(img)
    x = img_array.shape[0]
    y = img_array.shape[1]
    xs = []
    ys = []
    test = np.zeros((x, y))
    for i in range(x):
        for j in range(y):
            if img_array[i][j][0] > 150 and img_array[i][j][1] < 50 and img_array[i][j][2] < 50:
                xs.append(i)
                ys.append(j)
                test[i][j] = 255
    # test_img = Image.fromarray(test)
    # test_img.show()
    return xs, ys


def get_center():
    with Image.open('center.jpg') as img:
        img_array = np.array(img)
    x = img_array.shape[0]
    y = img_array.shape[1]
    xs = []
    ys = []
    for i in range(x):
        for j in range(y):
            if img_array[i][j][0] == 255 and img_array[i][j][1] == 255 and img_array[i][j][2] == 255:
                xs.append(i)
                ys.append(j)
    # 1290, 1440
    print(sum(xs) / len(xs))
    print(sum(ys) / len(ys))


def get_radius():
    with Image.open('circle.jpg') as img:
        img_array = np.array(img)
    x = img_array.shape[0]
    y = img_array.shape[1]
    for i in range(x):
        if img_array[i][1440][0] > 240 and img_array[i][1440][1] > 240 and img_array[i][1440][2] > 240:
            print(i)
    # for i in range(y):
    #     if img_array[1290][i][0] > 240 and img_array[1290][i][1] > 240 and img_array[1290][i][2] > 240:
    #         1537
    #         print(i)


def get_diff():
    xs, ys = get_result_arr()
    re = 0
    for i in range(len(xs)):
        x = xs[i]
        y = ys[i]
        dis = math.sqrt((x - 1290) ** 2 + (y - 1440) ** 2)
        re += abs(dis - 768.5)
    re /= len(xs)
    # 687
    print(re)


def main():
    # coin width is 502
    get_diff()


if __name__ == '__main__':
    main()
