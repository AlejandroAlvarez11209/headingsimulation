# TODO: Think of a better name for this file
import time

import matplotlib.pyplot as plt
import numpy as np


class PointsInSpace:
    def __init__(self, n, x_lim, y_lim=None, m=""):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        self.n = n
        self.m = m

        if y_lim is None:
            y_lim = x_lim

        self.ax.set_xlim(x_lim)
        self.ax.set_ylim(y_lim)

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

        # zero = np.array([0])
        zero = np.zeros(n)

        # Not sure why assignment needs to be like this
        (self.point,) = self.ax.plot(zero, zero, m, animated=True)
        plt.show(block=False)
        plt.pause(0.1)
        self.bg = self.fig.canvas.copy_from_bbox(self.fig.bbox)
        self.ax.draw_artist(self.point)
        self.fig.canvas.blit(self.fig.bbox)

    def draw_point(self, point, delay=0):
        # Pass in 2xn array
        if self.n == 1:
            point = np.array(point)[:, None]

        self.fig.canvas.restore_region(self.bg)
        self.point.set_data(point[0], point[1])

        self.ax.draw_artist(self.point)
        self.fig.canvas.blit(self.fig.bbox)
        self.fig.canvas.flush_events()

        if delay > 0:
            plt.pause(delay)


if __name__ == "__main__":
    lim = [-2, 2]
    pp = PointsInSpace(2, lim)
    frame_count = 1000

    tic = time.time()
    for j in range(frame_count):
        x_1 = np.cos((j / 100) * np.pi)
        y_1 = np.sin((j / 100) * np.pi)
        
        x_2 = np.cos((j / 100) * np.pi + np.pi)
        y_2 = np.sin((j / 100) * np.pi + np.pi)

        pp.draw_point([[x_1, x_2], [y_1, y_2]])

    print(f"Average FPS: {frame_count / (time.time() - tic)}")
