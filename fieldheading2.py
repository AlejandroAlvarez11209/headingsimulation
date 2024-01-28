import matplotlib.pyplot as plt
import numpy as np
import turtle

# Shape class: (array of vertices, center point)
# Vert_arr(Array): Array of vertices points (Points have an x and y component)
# Center(list): 2 element list with x and y component indicating the center of rotation relative to the frame
# of reference of the shape.


class Shape:
    def __init__(self, vert_arr, center):
        self.vert_arr = vert_arr
        self.center = center

    # func rotate_shape: (angle of rotation, rotation axis, center x coordinate, center y coordinate)
    # New_angle(int): Amount to rotate by
    # Current_Angle(int): Angle that square is currently at
    # Rot_axis(list): Point of rotation
    # dx(int): x coordinate of the center of the shape
    # dy(int): y coordinate of the center of the shape
    def rotate_shape(self, new_angle, current_angle, rot_axis, dx, dy):
        # Change-of-frame matrix
        transform = [
            [np.cos(new_angle), -np.sin(new_angle), dx],
            [np.sin(new_angle), np.cos(new_angle), dy],
            [0, 0, 1],
        ]
        # Change-of-frame matrix is turned into an array
        transform = np.array(transform)

        # List to keep track of the transformed points
        new_points_list = []
        # print(f"{self.vert_arr = }")

        # Iterate through the points in the robot frame and transform
        for point in self.vert_arr:
            new_point = point[:]
            new_point.append(1)
            new_point[0] -= rot_axis[0]
            new_point[1] -= rot_axis[1]
            new_point = np.array(new_point)
            # print(f"{new_point = }")
            transformed_point = transform @ new_point
            new_transformed_point = transformed_point[:2]
            new_points_list.append(new_transformed_point)

        # Transform the square center
        updated_center = self.center[:]
        updated_center.append(1)
        updated_center[0] -= rot_axis[0]
        updated_center[1] -= rot_axis[1]
        updated_center = np.array(updated_center)
        transformed_center = transform @ updated_center
        new_center = transformed_center[:2]
        new_center[0] += rot_axis[0]
        new_center[1] += rot_axis[1]

        # Loops through points in new_point_list list, adds center coordinates back to each x and y component
        for a_point in new_points_list:
            a_point[0] += rot_axis[0]
            a_point[1] += rot_axis[1]

        # Adds the shape to the graph
        robot = plt.Polygon(new_points_list)
        plt.gca().add_patch(robot)

        # Adds heading arrow to graph
        plt.quiver(new_center[0], new_center[1], np.cos(new_angle + np.pi / 2 + current_angle),
                   np.sin(new_angle + np.pi / 2 + current_angle), angles='xy')
        # Converts new vertices array into a list
        new_square_verts = []
        for points in new_points_list:
            new_square_verts.append(points.tolist())

        # Squares vertices and center are updated
        self.vert_arr = new_square_verts
        self.center = [new_center[0], new_center[1]]

        return new_angle

    # func drive: (current_angle, time_step, left_speed, right_speed)
    # Left Speed and Right Speed: Speed of motors
    # Current_angle: current angle of heading
    # Time Step: Time moved before rotating
    def drive(self, current_angle, time_step, left_spd, right_spd):
        pass
        # Take difference of two speeds
        diff_spd = right_spd - left_spd

        # Speed (0-255) scaled to angle (0-2pi)
        rot_angle = diff_spd * 2*np.pi/255

        # If Right > Left, pivot is on midpoint of left side
        if diff_spd > 0:
            pivot = [(self.vert_arr[0][0] + self.vert_arr[3][0])/2, (self.vert_arr[0][1] + self.vert_arr[3][1])/2]
            self.rotate_shape(rot_angle, current_angle, pivot,
                              time_step * (left_spd*right_spd)/(left_spd + right_spd) *
                              np.cos(rot_angle + np.pi / 2 + current_angle),
                              time_step * (left_spd*right_spd)/(left_spd + right_spd) *
                              np.sin(rot_angle + np.pi / 2 + current_angle))

        # If Left > Right, pivot is on midpoint of right side
        elif diff_spd < 0:
            pivot = [(self.vert_arr[1][0] + self.vert_arr[2][0])/2, (self.vert_arr[1][1] + self.vert_arr[2][1])/2]
            self.rotate_shape(rot_angle, current_angle, pivot,
                              time_step * (left_spd * right_spd) / (left_spd + right_spd) *
                              np.cos(rot_angle + np.pi / 2 + current_angle),
                              time_step * (left_spd * right_spd) / (left_spd + right_spd) *
                              np.sin(rot_angle + np.pi / 2 + current_angle))

        # If Left = Right, pivot is center
        else:
            pivot = self.center
            self.rotate_shape(0, current_angle, pivot,
                              time_step * left_spd * np.cos(np.pi / 2 + current_angle),
                              time_step * left_spd * np.sin(np.pi / 2 + current_angle))
        return rot_angle


#
# if __name__ == '__main__':


testing_bot = turtle.Turtle()
testing_bot2 = turtle.Turtle()
testing_bot3 = turtle.Turtle()
limits = 50
turtle.setworldcoordinates(-limits, -limits, limits, limits)
testing_bot.penup()
testing_bot.goto(0, -limits)
testing_bot.pendown()
testing_bot.goto(0,limits)
testing_bot.penup()
testing_bot.goto(-limits,0)
testing_bot.pendown()
testing_bot.goto(limits,0)
testing_bot.penup()
testing_bot.goto(0,0)
testing_bot.pendown()

# Define vertices of shape
vertices = [[-1, 1], [1, 1], [1, -1], [-1, -1]]
# Make a square shape
square = Shape(vertices, [0, 0])


#     # Initial conditions for loop
#     theta = -np.pi/6
#     x_comp = np.cos(theta + np.pi/2)
#     y_comp = np.sin(theta + np.pi/2)
#     old_angle = 0
#
#     for ii in np.linspace(0, 20, 21):
#         # Plot formatting
#         ax = plt.axes()
#         ax.grid(which="both", color="grey", linewidth=1, linestyle="-", alpha=0.2)
#         plt.gca().set_aspect("equal", adjustable="box")
#
#         # Rotates square by 30 degrees CW
#         if ii == 0:
#             new = square.rotate_shape(theta, old_angle, square.center, 0, 0)
#             old_angle += new
#
#             # Plot graphing
#             plt.ylim(-limits, limits)
#             plt.xlim(-limits, limits)
#             plt.draw()
#             plt.pause(0.2)
#
#         # Rotates square by 60 degrees from its current angle (Meaning a total of 90 degrees CW)
#         if ii == 10:
#             new = square.rotate_shape(np.pi/6, old_angle, square.center, 0, 0)
#             old_angle += new
#             x_comp = np.cos(old_angle + np.pi / 2)
#             y_comp = np.sin(old_angle + np.pi / 2)
#
#             # Turtle graphics. Tracks lower vertices and center of square
#             testing_bot.dot(5, "green")
#             testing_bot2.dot(5, "red")
#             testing_bot3.dot(5, "blue")
#             testing_bot.goto(square.center[0], square.center[1])
#             testing_bot2.goto(square.vert_arr[2][0], square.vert_arr[2][1])
#             testing_bot3.goto(square.vert_arr[3][0], square.vert_arr[3][1])
#
#             # Plot graphing
#             plt.ylim(-limits, limits)
#             plt.xlim(-limits, limits)
#             plt.draw()
#             plt.pause(0.2)
#
#         # Moves square by a distance of 1 in its current direction
#         square.rotate_shape(0, old_angle, square.center, x_comp, y_comp)
#
#         # Turtle graphics formatting
#         testing_bot.dot(5, "green")
#         testing_bot2.dot(5, "red")
#         testing_bot3.dot(5, "blue")
#         testing_bot.goto(square.center[0], square.center[1])
#         testing_bot2.goto(square.vert_arr[2][0], square.vert_arr[2][1])
#         testing_bot3.goto(square.vert_arr[3][0], square.vert_arr[3][1])
#
#         # Plot graphing
#         plt.ylim(-limits, limits)
#         plt.xlim(-limits, limits)
#         plt.draw()
#         plt.pause(0.2)
#
#     turtle.done()
k = 0
for ii in np.linspace(0,20,21):
    ax = plt.axes()
    ax.grid(which="both", color="grey", linewidth=1, linestyle="-", alpha=0.2)
    plt.gca().set_aspect("equal", adjustable="box")

    # Move
    new_ang = square.drive(k, 0.01, 80, 0)
    k += new_ang

    testing_bot.dot(5, "green")
    testing_bot2.dot(5, "red")
    testing_bot3.dot(5, "blue")
    testing_bot.goto(square.center[0], square.center[1])
    testing_bot2.goto(square.vert_arr[2][0], square.vert_arr[2][1])
    testing_bot3.goto(square.vert_arr[3][0], square.vert_arr[3][1])
    plt.ylim(-limits, limits)
    plt.xlim(-limits, limits)
    plt.draw()
    plt.pause(0.2)

turtle.done()
