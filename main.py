"""
IF20-main by Yuning Sun
4:19 PM 7/1/21
Module documentation: 
"""
import threading
import numpy as np
import matplotlib.pyplot as plt

from cp_speed_monitor import CPSpeedMonitor, Velocity
from stage_controller import StageController

velocity = Velocity()
cp_speed_monitor = CPSpeedMonitor(velocity)

x = np.linspace(0, 10, 100)
y = 2 * np.sin(x)
new_trajectory = np.array(list(zip(x, y)))
stage_controller = StageController(new_trajectory, velocity, cp_speed_monitor)

cp_speed_monitor.start()
stage_controller.start()
cp_speed_monitor.join()
stage_controller.join()
