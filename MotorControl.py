import pigpio

# pin definitions
motor1_enable = 4
motor1_1 = 22
motor1_2 = 27

motor2_enable = 25
motor2_1 = 24
motor2_2 = 23


# create the gpio object
pi = pigpio.pi()

# set the motors pins as outputs
pi.set_mode(motor1_enable, pigpio.OUTPUT)
pi.set_mode(motor1_1, pigpio.OUTPUT)
pi.set_mode(motor1_2, pigpio.OUTPUT)

pi.set_mode(motor2_enable, pigpio.OUTPUT)
pi.set_mode(motor2_1, pigpio.OUTPUT)
pi.set_mode(motor2_2, pigpio.OUTPUT)

# initial testing... drive forward on both motors
pi.write(motor1_1, 1)
pi.write(motor1_2, 0)

pi.write(motor2_1, 1)
pi.write(motor2_2, 0)

pi.write(motor1_enable, 1)
pi.write(motor2_enable, 1)

while True:
    for i in range(1000000):
        x = 1

    pi.write(motor1_enable, 1)
    pi.write(motor2_enable, 1)

    for i in range(1000000):
        x = 1

    pi.write(motor1_enable, 0)
    pi.write(motor2_enable, 0)



