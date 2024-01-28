import numpy as np

from rendering import PointsInSpace


class Robot:
    def __init__(self, vert_arr, x, y, theta):
        # Vert arr is
        # 1 2
        # 4 3
        # If the robot faces up
        self.vert_arr = vert_arr
        self.x = x
        self.y = y
        self.theta = theta
        self.l = abs(vert_arr[1][0] - vert_arr[0][0])

    def transform(self, dtheta, dx, dy, rot_axis=None):
        if rot_axis is None:
            rot_axis = [self.x, self.y]

        new_angle = self.theta + dtheta
        transform_arr = np.array(
            [
                [np.cos(new_angle), -np.sin(new_angle), dx],
                [np.sin(new_angle), np.cos(new_angle), dy],
                [0, 0, 1],
            ]
        )

        transformed_points = []

        for point in self.vert_arr:
            new_point = point[:]
            new_point.append(1)

            new_point[0] -= rot_axis[0]
            new_point[1] -= rot_axis[1]
            new_point = np.array(new_point)

            transformed_point = transform_arr @ new_point
            transformed_point = transformed_point[:2]
            transformed_point[0] += rot_axis[0]
            transformed_point[1] += rot_axis[1]

            transformed_points.append(transformed_point.tolist())
            
        # print(f"{transformed_points = }")
        self.vert_arr = transformed_points

    def drive(self, v_left, v_right, dt):
        if v_left == v_right:
            dx = dt * v_left * np.cos(self.theta)
            dy = dt * v_left * np.sin(self.theta)
            self.transform(0, dx, dy)
            return

        R = (self.l / 2) * (v_left + v_right) / (v_right - v_left)
        omega = (v_right - v_left) / self.l
        dtheta = omega * dt

        if v_left < v_right:
            dx = R * np.sin(dtheta)
            dy = R * (np.cos(dtheta) - 1)
            self.transform(dtheta, dx, dy)
        elif v_left > v_right:
            dx = R * np.sin(dtheta)
            dy = R * (1 - np.cos(dtheta))
            self.transform(dtheta, dx, dy)

    def get_vert_arr(self):
        return self.vert_arr


def main():
    vert_array = [[-1, 1], [1, 1], [1, -1], [-1, -1]]
    lim_x = [-20, 20]
    lim_y = [-29, 11]
    frame_count = 10000

    robot = Robot(vert_array, 0, 9, 0)
    pis = PointsInSpace(4, lim_x, lim_y)
    
    for i in range(frame_count):
        robot.drive(1, 0.8, 0.1)
        rendering_array = np.array(robot.get_vert_arr()).T
        pis.draw_point([rendering_array[0], rendering_array[1]])


if __name__ == "__main__":
    main()
