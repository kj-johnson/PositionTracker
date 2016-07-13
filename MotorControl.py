import pigpio


class MotorControl:
    # pin definitions
    motor1_enable = 4
    motor1_1 = 22
    motor1_2 = 27

    motor2_enable = 25
    motor2_1 = 24
    motor2_2 = 23

    # create the gpio object
    pi = pigpio.pi()

    def __init__(self):
        # set the motors pins as outputs
        self.pi.set_mode(self.motor1_enable, pigpio.OUTPUT)
        self.pi.set_mode(self.motor1_1, pigpio.OUTPUT)
        self.pi.set_mode(self.motor1_2, pigpio.OUTPUT)

        self.pi.set_mode(self.motor2_enable, pigpio.OUTPUT)
        self.pi.set_mode(self.motor2_1, pigpio.OUTPUT)
        self.pi.set_mode(self.motor2_2, pigpio.OUTPUT)

    def stop(self):
        # disable motors
        self.pi.write(self.motor1_enable, 0)
        self.pi.write(self.motor2_enable, 0)

    def motor_1_forward(self, forward=True):
        if forward:
            self.pi.write(self.motor1_1, 1)
            self.pi.write(self.motor1_2, 0)
        else:
            self.pi.write(self.motor1_1, 0)
            self.pi.write(self.motor1_2, 1)

    def motor_2_forward(self, forward=True):
        if forward:
            self.pi.write(self.motor2_1, 1)
            self.pi.write(self.motor2_2, 0)
        else:
            self.pi.write(self.motor2_1, 0)
            self.pi.write(self.motor2_2, 1)

    def start_motors(self):
        self.pi.write(self.motor1_enable, 1)
        self.pi.write(self.motor2_enable, 1)

    def turn_counter_clockwise(self):
        # change directions
        self.motor_1_forward(True)
        self.motor_2_forward(False)  # reversed

    def turn_clockwise(self):
        # change directions
        self.motor_1_forward(False)  # reversed
        self.motor_2_forward(True)

    def move_forward(self):
        self.motor_1_forward(True)
        self.motor_2_forward(True)

    def move_backward(self):
        self.motor_1_forward(False)
        self.motor_2_forward(False)
