"""
IF20-stage_controller by Yuning Sun
4:33 PM 5/14/21
Module documentation: 
"""
import threading
import time

import serial
import numpy as np
import math
import matplotlib.pyplot as plt

# 从当前位置向Y正、负向或X正、负向（PosY、NegY、PosX, NegX)按照给定速度vel移动给定距离dis
from cp_speed_monitor import CPSpeedMonitor, Velocity
from trajectory import TrajectoryCalculator

RATIO = 0.00635


def get_absolute_velocity(relative_v, stage_v):
    return relative_v + stage_v


def next_command(current_position, next_position, absolute_v_x, absolute_v_y, lag, kappa, interval):
    """
    Get next command
    :param current_position: current coordinate
    :param next_position: next coordinate
    :param absolute_v_x: absolute velocity of contact point in x axis
    :param absolute_v_y: absolute velocity of contact point in y axis
    :param lag: lag length
    :param kappa:
    :param interval: time interval
    :return: next command string
    """
    stage_distance_x = next_position[0] - current_position[0]
    stage_distance_y = next_position[1] - current_position[1]
    stage_v_x = stage_distance_x / interval
    stage_v_y = stage_distance_y / interval
    relative_v_x = absolute_v_x - stage_v_x
    relative_v_y = absolute_v_y - stage_v_y
    relative_cp_v = math.sqrt(relative_v_x ** 2 + relative_v_y ** 2)
    next_stage_speed = next_point_speed(relative_cp_v, lag, kappa)
    stage_distance = math.sqrt(stage_distance_x ** 2 + stage_distance_y ** 2)
    local_etx = stage_distance_x / stage_distance
    local_ety = stage_distance_y / stage_distance
    next_stage_v_x = next_stage_speed * local_etx
    next_stage_v_y = next_stage_speed * local_ety
    next_stage_v_x = math.ceil(abs(next_stage_v_x))
    next_stage_v_y = math.ceil(abs(next_stage_v_y))
    next_x = math.ceil(next_position[0] / RATIO)
    next_y = math.ceil(next_position[1] / RATIO)
    return 'E, C, S3M{},S1M{},P{},(IA3M{},IA1M{},),R^'.format(next_stage_v_x, next_stage_v_y, 0, next_x, next_y)


# 'E, C, S3M{},S1M{},(IA3M{},IA1M{},),R^'


def next_point_speed(v, lag, kappa):
    """
    Get next point speed
    :param v: current contact point relative speed
    :param lag:
    :param kappa:
    :return:
    """
    return v * math.sqrt(1 + (lag * kappa) ** 2)


class StageController(threading.Thread):
    def __init__(self, trajectory, v: Velocity, cp_speed_monitor: CPSpeedMonitor):
        super().__init__()
        self.trajectory = trajectory
        self.v = v
        self.cp_speed_monitor = cp_speed_monitor

    def run(self) -> None:
        serial_port = serial.Serial('COM18', baudrate=9600, timeout=0.1)
        serial_port.read()
        receiver = '^'
        # prepare
        vx = 10
        x = 0
        prepare_times = 10
        for i in range(prepare_times):
            while '^' not in str(receiver):
                receiver = serial_port.read()
            cmd = 'E, C, S3M{},S1M{},(IA3M{},IA1M{},),R^'.format(vx, 0, x, 0)
            x += 1
            serial_port.write(cmd.encode())
            receiver = serial_port.read()
        trajectory_calculator = TrajectoryCalculator(self.trajectory, self.v.get_lag_length())
        path = trajectory_calculator.path
        kappa = trajectory_calculator.kappa
        # start
        last_time = time.time()
        for i in range(len(path) - 1):
            while '^' not in str(receiver):
                receiver = serial_port.read()
            current_time = time.time()
            cmd = next_command(path[i], path[i + 1], self.v.get_absolute_v_x(), self.v.get_absolute_v_y(), self.v.get_lag_length(), kappa[i],
                               current_time - last_time)
            last_time = current_time
            serial_port.write(cmd.encode())
            receiver = serial_port.read()
        serial_port.close()
        self.cp_speed_monitor.stop()


if __name__ == '__main__':
    user_path = np.array([[0, 0, 5, 1], [10, 0, 25, 0], [10, 10, 5, 1], [0, 10, 10, 1], [0, 0, 5, 1]])
    # stage_controller = StageController(user_path, 2)
    # stage_controller.start()
    # stage_controller.join()
