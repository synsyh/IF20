"""
IF20-trajectory by Yuning Sun
5:38 PM 7/1/21
Module documentation: 
"""
import numpy as np
from matplotlib import pyplot as plt


class TrajectoryCalculator:
    def __init__(self, trajectory, lag):
        self.trajectory = trajectory
        self.path = self.path_trajectory(lag)
        self.path_x = self.path[:, 0]
        self.path_y = self.path[:, 1]

    def curvature(self):
        x_lst = self.trajectory[:, 0]
        y_lst = self.trajectory[:, 1]
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

    def tangential(self):
        x_lst = self.trajectory[:, 0]
        y_lst = self.trajectory[:, 1]
        x_diff_1 = x_lst[1:] - x_lst[:-1]
        y_diff_1 = y_lst[1:] - y_lst[:-1]
        arc_length = np.sqrt(np.square(x_diff_1) + np.square(y_diff_1))  # calculate the arc length
        e_tx = x_diff_1 / arc_length
        e_ty = y_diff_1 / arc_length
        e_txy = np.array(list(zip(e_tx, e_ty)))
        e_txy = np.append(e_txy, np.array(e_txy[-1, :]).reshape((1, 2)), axis=0)
        return e_txy

    def path_trajectory(self, lag=1):
        x_lst = self.trajectory[:, 0]
        y_lst = self.trajectory[:, 1]
        e_txy = self.tangential()
        e_tx = e_txy[:, 0]
        e_ty = e_txy[:, 1]
        X_lst = x_lst + lag * e_tx
        Y_lst = y_lst + lag * e_ty
        result = np.array(list(zip(X_lst, Y_lst)))
        return result

    def show(self):
        plt.plot(self.path_x, self.path_y)
        plt.plot(self.trajectory[:, 0], self.trajectory[:, 1])
        plt.show()

def main():
    x = np.linspace(0, 10, 100)
    y = 2 * np.sin(x)
    trajectory = TrajectoryCalculator(np.array(list(zip(x, y))), 2)
    trajectory.show()


if __name__ == '__main__':
    main()
