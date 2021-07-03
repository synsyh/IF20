import math

import numpy as np
import serial


# 从当前位置向Y正、负向或X正、负向（PosY、NegY、PosX, NegX)按照给定速度vel移动给定距离dis
def PosY(dis, vel):
    import serial
    if vel == 0:
        print("Speed can't be zero!")
    else:
        serport = serial.Serial('COM3', baudrate=9600, timeout=0.1)
        cmd = 'E,C,S1M{},I1M{},R'.format(int(vel / 0.00635), int(dis / 0.00635))
        serport.write(cmd.encode())
        serport.close()


def NegY(dis, vel):
    import serial
    if vel == 0:
        print("Speed can't be zero!")
    else:
        serport = serial.Serial('COM3', baudrate=9600, timeout=0.1)
        cmd = 'E,C,S1M{},I1M-{},R'.format(int(vel / 0.00635), int(dis / 0.00635))
        serport.write(cmd.encode())
        serport.close()


def PosX(dis, vel):
    import serial
    if vel == 0:
        print("Speed can't be zero!")
    else:
        serport = serial.Serial('COM3', baudrate=9600, timeout=0.1)
        cmd = 'E,C,S3M{},I3M{},R'.format(int(vel / 0.00635), int(dis / 0.00635))
        serport.write(cmd.encode())
        serport.close()


def NegX(dis, vel):
    import serial
    if vel == 0:
        print("Speed can't be zero!")
    else:
        serport = serial.Serial('COM3', baudrate=9600, timeout=0.1)
        cmd = 'E,C,S3M{},I3M-{},R'.format(int(vel / 0.00635), int(dis / 0.00635))
        serport.write(cmd.encode())
        serport.close()


# 出现故障时使用RecoverCmd
def RecoverCmd():
    serport = serial.Serial('COM3', baudrate=9600, timeout=0.1)
    serport.write('K'.encode())
    serport.close()


# SetAsHome将当前点设为（0， 0）点
def SetAsHome():
    serport = serial.Serial('COM3', baudrate=9600, timeout=0.1)
    serport.write('E,C,(IA3M-0,IA1M-0,),R'.encode())
    serport.close()


# Back2Home回到（0， 0）点
def Back2Home():
    serport = serial.Serial('COM3', baudrate=9600, timeout=0.1)
    serport.write('E,C,S1M800,S3M800,(IA3M0,IA1M0,),R'.encode())
    serport.close()


# IdleCmd移动至台子的某一最大边角处，执行后便于打印物移除
def IdleCmd():
    serport = serial.Serial('COM3', baudrate=9600, timeout=0.1)
    serport.write('E,C,S1M800,S3M800,(I3M-0,I1M-0,),R'.encode())
    serport.close()


# 用户提供的路径信息data为n*4的numpy数组，n为路径节点数，第一列为当前点横坐标x，第二列为当前点纵坐标y，
# 第三列为当前点到下一点的速度，第四列为当前点处停留时间。如下文中的user_path。
# data由PathGeneration生成Stage可识别命令cmd_lst,cmd_lst类型：元素为字符串的序列。
def PathGeneration(data):
    Xvalue = data[:, 0]
    Yvalue = data[:, 1]
    Svalue = data[:, 2]
    Pvalue = data[:, 3]
    cmd_lst = ['E,C,S3M500,S1M500,(IA3M0,IA1M0,),R^']
    # cmd_lst.append('E,C,')
    for i in range(len(data) - 1):
        deltax = Xvalue[i + 1] - Xvalue[i]
        deltay = Yvalue[i + 1] - Yvalue[i]
        if math.sqrt(deltax ** 2 + deltay ** 2) != 0:
            vx = Svalue[i] * deltax / math.sqrt(deltax ** 2 + deltay ** 2) / 0.00635
            vy = Svalue[i] * deltay / math.sqrt(deltax ** 2 + deltay ** 2) / 0.00635

        else:
            vx = 500
            vy = 500
        cmd_lst.append('E, C, S3M{},S1M{},P{},(IA3M{},IA1M{},),R^'.format(math.ceil(abs(vx)), math.ceil(abs(vy)),
                                                                          int(10 * Pvalue[i]),
                                                                          math.ceil(Xvalue[i + 1] / 0.00635),
                                                                          math.ceil(Yvalue[i + 1] / 0.00635)))
    return cmd_lst


# Run_XY_Path接受元素为字符串的可识别命令序列，发送给Stage执行。
def Run_XY_Path(cmd):
    serport = serial.Serial('COM3', baudrate=9600, timeout=0.1)
    serport.read()
    receiver = '^'
    for i in range(len(cmd)):
        while not '^' in str(receiver):
            receiver = serport.read()
        serport.write(cmd[i].encode())
        receiver = serport.read()
    serport.close()


# 下为举例：路径为1矩形。
user_path = np.array([[0, 0, 5, 1], [10, 0, 25, 0], [10, 10, 5, 1], [0, 10, 10, 1], [0, 0, 5, 1]])
# 生成可识别命令。
user_cmd = PathGeneration(user_path)
# 执行可识别命令。
Run_XY_Path(user_cmd)
