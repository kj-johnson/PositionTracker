import PositionTracker
import MotorControl
from time import sleep
from math import sqrt, pow, cos, sin, radians, degrees, acos, hypot


class Forklift:
    tracker = PositionTracker.PositionTracker()
    motor = MotorControl.MotorControl()
    start_point = [0, 0]
    end_point = [0, 0]
    target_point = 0  # 0 = don't move, 1 = move to start, 2 = move to end
    keep_running = True
    run_mode = 1  # 1 = only specify end position, 2 = specify start and finish
    distance_tolerance = 2  # will stop when it is within x inches (don't set too low or it will never stop)

    @staticmethod
    def prompt_for_location(display_string="Enter location"):
        x = float(input(display_string + ' (X): '))
        y = float(input(display_string + ' (Y): '))
        return [x, y]

    def prompt_for_start_point(self):
        self.start_point = self.prompt_for_location("Start location")

    def prompt_for_end_point(self):
        self.end_point = self.prompt_for_location("End location")

    def distance_between_self_and_target(self):
        # print("finding distance...")
        position = self.tracker.get_location()[0]
        if self.target_point == 0:
            return 0.0
        if self.target_point == 1:
            return sqrt(pow(self.start_point[0] - position[0], 2) + pow(self.start_point[1] - position[1], 2))
        if self.target_point == 2:
            return sqrt(pow(self.end_point[0] - position[0], 2) + pow(self.end_point[1] - position[1], 2))

    def angle_between_self_and_target(self):
        # print("Finding angle...")
        tracker_output = self.tracker.get_location()
        position = tracker_output[0]
        heading = tracker_output[1]

        # determine which target point you're going for
        if self.target_point == 0:
            return 0.0  # you don't need to turn, so bail
        if self.target_point == 1:
            target = self.start_point
        if self.target_point == 2:
            target = self.end_point

        # create the respective vectors
        # first, the vehicle's heading vector using a unit vector
        c_degrees = self.tracker.bearing_to_math_degrees(heading)
        c_vector = [cos(radians(c_degrees)), sin(radians(c_degrees))]

        # second, get the vector to the destination
        d_vector = [position[0] - target[0], position[1] - target[1]]

        # I don't care about normalizing it now, I just want the angle
        dot_product = c_vector[0]*d_vector[0] + c_vector[1]*d_vector[1]
        c_magnitude = hypot(c_vector[0], c_vector[1])
        d_magnitude = hypot(d_vector[0], d_vector[1])
        if d_magnitude < 0.1:
            return 0.0  # prevent divide by zero error
        theta = degrees(acos(dot_product / (c_magnitude * d_magnitude)))

        theta = 180 - theta  # I'm getting the complement of the angle, so switch it

        delta = c_vector[0]*d_vector[1] - c_vector[1]*d_vector[0]
        if delta >= 0.0:  # clockwise
            return theta
        else:  # counter-clockwise
            return -1.0 * theta

    def print_points(self):
        print(self.start_point)
        print(self.end_point)

    def run(self):
        while self.run_mode == 1:
            # find out what point to go to
            self.prompt_for_end_point()
            self.target_point = 2
            self.keep_running = True
            while self.keep_running:

                # Find the difference in angles
                self.motor.stop()
                angle = self.angle_between_self_and_target()
                # print("Angle is", angle)
                sleep(.5)
                if angle >= 0.0:
                    self.motor.turn_clockwise()
                else:
                    angle *= -1.0  # turn it into a positive number
                    self.motor.turn_counter_clockwise()

                # turn the car
                self.motor.start_motors()
                sleep(angle / 400.0)
                self.motor.stop()
                # sleep(0.25)

                # determine movement direction
                angle = abs(self.angle_between_self_and_target())
                if angle < 90:
                    self.motor.move_forward()
                else:
                    self.motor.move_backward()
                self.motor.start_motors()
                sleep(self.distance_between_self_and_target() / 200.0)  # adjust the divisor for different frequency
                self.motor.stop()

                # check if it is close enough
                if self.distance_between_self_and_target() < self.distance_tolerance:
                    self.keep_running = False
            print("Final position:", self.tracker.get_location()[0])
            print("Distance from desired point:", self.distance_between_self_and_target())
            again = input("Do you want to stop? y/n\n")
            if again == "y":
                exit()

forklift = Forklift()
forklift.run()


