import numpy as np
from matplotlib import pyplot as plt
from math import sqrt


# calculate the curvature of a trajectory, which is the CP trajectory given by the customer;
# input param: trajectory is a n*2 numpy array; n is the number of nodes in the trajectory;
# input param: trajectory column 0 are x coordinates, column 1 are y coordinates;
# return a n*1 numpy array
def curvature(trajectory):
    x_lst = trajectory[:, 0]
    y_lst = trajectory[:, 1]
    x_diff_1 = x_lst[1:] - x_lst[:-1]
    y_diff_1 = y_lst[1:] - y_lst[:-1]
    y_prime = y_diff_1 / x_diff_1
    y_diff_2 = y_prime[1:] - y_prime[:-1]
    y_prime_2 = y_diff_2 / x_diff_1[:-1]  # y''
    kappa = np.abs(y_prime_2) / ((1 + np.square(y_prime[:-1])) ** 1.5)  # kappa = |y''|/(1+y'2)^(3/2)
    # 差分法会减少点的个数，因而需要补全。
    kappa = np.append(kappa, kappa[-1])
    kappa = np.append(kappa, kappa[-1])
    return kappa


# calculate the tangential unit vector of a trajectory
# input param: trajectory is a n*2 numpy array
# return a n*2 numpy array
def e_t(trajectory):
    x_lst = trajectory[:, 0]
    y_lst = trajectory[:, 1]
    x_diff_1 = x_lst[1:] - x_lst[:-1]
    y_diff_1 = y_lst[1:] - y_lst[:-1]
    arc_length = np.sqrt(np.square(x_diff_1) + np.square(y_diff_1))  # calculate the arc length
    e_tx = x_diff_1 / arc_length
    e_ty = y_diff_1 / arc_length
    e_txy = np.array(list(zip(e_tx, e_ty)))
    e_txy = np.append(e_txy, np.array(e_txy[-1, :]).reshape((1, 2)), axis=0)
    return e_txy


# calculate the positional info for path generation
# input param: trajectory is a n*2 numpy array; lag is the specified lag length, a number
# return a n*2 numpy array
def path_trajectory(trajectory, lag=1):
    x_lst = trajectory[:, 0]
    y_lst = trajectory[:, 1]
    e_txy = e_t(trajectory)
    e_tx = e_txy[:, 0]
    e_ty = e_txy[:, 1]
    X_lst = x_lst + lag * e_tx
    Y_lst = y_lst + lag * e_ty
    result = np.array(list(zip(X_lst, Y_lst)))
    return result


# calculate the NP speed based on the derivation result
# input param: v is the measured CP speed; lag is the lag length; kappa is the local curvature
# △△△△mind that it's used to calculate the pointwise NP speed,
# thus all input params and returned result are pointwise value, not array
def point_speed(v, lag, kappa):
    return v * sqrt(1 + (lag * kappa) ** 2)


# following is an example.
x = np.linspace(0, 10, 100)
y = 2 * np.sin(x)
trajectory = np.array(list(zip(x, y)))
print(trajectory)
print(curvature(trajectory))
print(e_t(trajectory))
Path_x = path_trajectory(trajectory, 2)[:, 0]
Path_y = path_trajectory(trajectory, 2)[:, 1]
plt.plot(x, y)
plt.plot(Path_x, Path_y)
plt.show()
