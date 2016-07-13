"""This module tracks your location."""

from IRCamera import IRCamera
from time import sleep
import math
from math import cos, sin, degrees, radians

# IMPORTANT NOTES
# This tracker requires the data to be set in the SETTINGS section.
# Hardware-wise, this tracker requires an isosceles triangle (NOT EQUILATERAL)
# of IR LEDs to be mounted above the camera
# Ideally, the triangle will point north for ease of accuracy checking using a
# magnetometer (optional)


class PositionTracker:

    def __init__(self):
        # SETTINGS
        self.i2c_bus = 1  # i2c bus number (either 0 or 1)
        self.ir_camera_port = 0x58
        self.ir_emitter_pattern_width = 3.0  # inches
        self.ir_emitter_pattern_height = 3.44  # inches
        self.ceiling_height = 96  # inches
        self.has_magnetometer = False  # enables error correction using magnetometer
        self.tilt_offset_y = 8.5  # how many inches is the tilt off by?

        # make your camera object
        self.camera = IRCamera(self.i2c_bus, self.ir_camera_port)

    # calculate the size of the square you can travel in (so you can report your
    # location accurately)
    # We factor in a 10% overlap in the hopes of making absolutely sure we can't
    # travel too far and lose sight of the sensor

    @staticmethod
    def close_to(value_1, value_2, within_range=5):
        if abs(value_1 - value_2) < within_range:
            return True
        else:
            return False

    @staticmethod
    def rotate_around_origin(x, y, theta):
        # according to what I got out of a Khan Academy video, I need to use
        # x'= x*cos(theta) - y*sin(theta)
        # and
        # y'= x*sin(theta) + y*cos(theta)
        # theta *= -1.0
        position = [0, 0]
        position[0] = x * cos(radians(theta)) - y * sin(radians(theta))
        position[1] = x * sin(radians(theta)) + y * cos(radians(theta))
        return position

    @staticmethod
    def bearing_to_math_degrees(theta):
        vector_direction_degrees = -1 * theta + 90  # convert from bearing into math-appropriate degrees
        while vector_direction_degrees < 0.0:
            vector_direction_degrees += 360.0  # force it into a range from 0 to 360
        return vector_direction_degrees

    @staticmethod
    def math_degrees_to_bearing(theta):
        theta = (theta - 90) * -1
        while theta < 0.0:
            theta += 360.0
        return theta

    def get_location(self):
        found = False
        while not found:
            # needs to wait before trying to read again
            sleep(0.1)

            # Grab the current positions
            positions = self.camera.get_positions()

            # if there are three points, there is a possible triangle
            if len(positions) == 3:
                # convert the positions to the grid-relative format
                point_1, point_2, point_3 = positions[0], positions[1], positions[2]
                point_1[0] -= 512
                point_2[0] -= 512
                point_3[0] -= 512

                point_1[1] -= 384
                point_2[1] -= 384
                point_3[1] -= 384

                # now the points are on a grid from x=[-512,512], y=[-384,384]

                # find the distances between the points
                dist_1_to_2 = math.sqrt(pow(point_2[0] - point_1[0], 2) + pow(point_2[1] - point_1[1], 2))
                dist_1_to_3 = math.sqrt(pow(point_3[0] - point_1[0], 2) + pow(point_3[1] - point_1[1], 2))
                dist_2_to_3 = math.sqrt(pow(point_3[0] - point_2[0], 2) + pow(point_3[1] - point_2[1], 2))

                # determine which, if any, are the points of an isosceles triangle
                # midpoint = [0, 0]
                # top_point = [0, 0]
                # point = -1

                # if dist_1_to_2 == dist_1_to_3 and dist_1_to_2 > dist_2_to_3:  # point 1 is the point, 2/3 are the base
                if self.close_to(dist_1_to_2, dist_1_to_3) and dist_1_to_2 > dist_2_to_3:  # point 1 is the point, 2/3 are the base
                    midpoint = [point_2[0] + (point_3[0] - point_2[0])/2, point_2[1] + (point_3[1] - point_2[1])/2]
                    top_point = point_1
                elif self.close_to(dist_1_to_2, dist_2_to_3) and dist_1_to_2 > dist_1_to_3:  # point 2 is the point, 1/3 are the base
                    midpoint = [point_1[0] + (point_3[0] - point_1[0])/2, point_1[1] + (point_3[1] - point_1[1])/2]
                    top_point = point_2
                elif self.close_to(dist_1_to_3, dist_2_to_3) and dist_1_to_3 > dist_1_to_2:  # point 3 is the point, 1/2 are the base
                    midpoint = [point_1[0] + (point_2[0] - point_1[0])/2, point_1[1] + (point_2[1] - point_1[1])/2]
                    top_point = point_3
                else:  # you didn't find it -- it isn't an isosceles triangle, just three points
                    continue  # start the loop over

                # determine the direction in which the triangle points
                # this can be done by finding the vector from the midpoint to the top of the triangle
                # in other words, top point - midpoint = vector
                vector = [top_point[0] - midpoint[0], top_point[1] - midpoint[1]]
                vector_direction_radians = math.atan2(vector[0], vector[1])  # returns a value from -pi to pi
                vector_direction = degrees(vector_direction_radians)
                # force it into bearing form (0 to 360 degrees instead of -180 to 180)
                if vector_direction < 0.0:
                    vector_direction += 360.0

                vector_direction_degrees = -1 * vector_direction + 90  # convert from bearing into math-appropriate degrees
                while vector_direction_degrees < 0.0:
                    vector_direction_degrees += 360.0  # force it into a range from 0 to 360

                vehicle_position = [top_point[0], -1 * top_point[1]]
                # print("Untouched vehicle position:", vehicle_position)

                # the scaling factor is determined using the specified triangle height -- it allows you to move up and down
                # and still have accurate positioning in real-world units (inches in this case)
                scaling_factor = self.ir_emitter_pattern_height / math.sqrt(pow(top_point[0] - midpoint[0], 2) + pow(top_point[1] - midpoint[1], 2))

                position_in_inches = [vehicle_position[0] * scaling_factor, vehicle_position[1] * scaling_factor]  # adjust from pixels to actual measurements
                # position_in_inches = [position_in_inches[0] * 1.287257143 - 0.346476191, position_in_inches[1] * 1.287257143 - 0.346476191]  # adjust for scaling imperfections
                # print("Camera-read Position:", vehicle_position)
                # print("Camera-read Position (inches):", position_in_inches)

                position_in_inches = [position_in_inches[0], position_in_inches[1] + self.tilt_offset_y]  # adjust for tilt
                # print("Tilt-adjusted Position (inches):", position_in_inches)
                inches_from_center = math.hypot(position_in_inches[0], position_in_inches[1])  # distance from point to the origin


                # print("Distance from center (inches):", inches_from_center)
                # print("Vehicle bearing:", vector_direction)
                # print("Vehicle degrees:", vector_direction_degrees)

                # use the bearing in this case -- the negative is to change which direction you rotate it
                absolute_position = self.rotate_around_origin(position_in_inches[0], position_in_inches[1], -1.0 * vector_direction)

                # print("Corrected position:", absolute_position)
                return [absolute_position, vector_direction]  # [ [x, y], direction ]


