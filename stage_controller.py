"""
IF20-stage_controller by Yuning Sun
4:33 PM 5/14/21
Module documentation: 
"""
import threading

import serial
import numpy as np
import math
import matplotlib.pyplot as plt

# 从当前位置向Y正、负向或X正、负向（PosY、NegY、PosX, NegX)按照给定速度vel移动给定距离dis
from trajectory import TrajectoryCalculator

RATIO = 0.00635


def next_command(current_position, next_position, v):
    delta_x = next_position[0] - current_position[0]
    delta_y = next_position[1] - current_position[1]
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    if distance != 0:
        vx = v * delta_x / distance / RATIO
        vy = v * delta_y / distance / RATIO
    else:
        vx = 500
        vy = 500
    vx = math.ceil(abs(vx))
    vy = math.ceil(abs(vy))
    next_x = math.ceil(next_position[0] / RATIO)
    next_y = math.ceil(next_position[1] / RATIO)
    return 'E, C, S3M{},S1M{},P{},(IA3M{},IA1M{},),R^'.format(vx, vy, 0, next_x, next_y)


def point_speed(v, lag, kappa):
    return v * math.sqrt(1 + (lag * kappa) ** 2)


class StageController(threading.Thread):
    def __init__(self, trajectory, lag, v, cp_speed_monitor):
        super().__init__()
        self.lag = lag
        self.trajectory_calculator = TrajectoryCalculator(trajectory, lag)
        self.path = self.trajectory_calculator.path
        self.kappa = self.trajectory_calculator.kappa
        self.v = v
        self.cp_speed_monitor = cp_speed_monitor

    def run(self) -> None:
        serial_port = serial.Serial('COM18', baudrate=9600, timeout=0.1)
        serial_port.read()
        receiver = '^'
        for i in range(len(self.path) - 1):
            while '^' not in str(receiver):
                receiver = serial_port.read()
            cmd = next_command(self.path[i], self.path[i + 1], point_speed(self.v.get(), self.lag, self.kappa))
            serial_port.write(cmd.encode())
            receiver = serial_port.read()
        serial_port.close()
        self.cp_speed_monitor.stop()


if __name__ == '__main__':
    user_path = np.array([[0, 0, 5, 1], [10, 0, 25, 0], [10, 10, 5, 1], [0, 10, 10, 1], [0, 0, 5, 1]])
    # stage_controller = StageController(user_path, 2)
    # stage_controller.start()
    # stage_controller.join()
