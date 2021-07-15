"""
IF20-main_test by Yuning Sun
4:19 PM 7/1/21
Module documentation: 
"""
import unittest

import numpy as np

from cp_speed_monitor import Velocity, CPSpeedMonitor
from stage_controller import StageController


def main():
    velocity = Velocity()
    cp_speed_monitor = CPSpeedMonitor(velocity)

    x = np.linspace(0, 10, 100)
    y = 2 * np.sin(x)
    new_trajectory = np.array(list(zip(x, y)))
    lag = 2
    stage_controller = StageController(new_trajectory, lag, velocity, cp_speed_monitor)

    cp_speed_monitor.start()
    stage_controller.start()
    cp_speed_monitor.join()
    stage_controller.join()


if __name__ == '__main__':
    main()
