# PositionTracker
Position tracking for my automated forklift project

# Requirements
## Hardware
- [Raspberry Pi](http://www.raspberrypi.org)
- [IR Tracking Camera](http://www.robotshop.com/en/ir-tracking-camera.html)
- [L293D Motor Driver](https://www.adafruit.com/product/807)

## Software
- [pigpio daemon](http://abyz.co.uk/rpi/pigpio/) (This allows us to access I2C without running our Python script as root)
- [Python 3](https://www.python.org/downloads/)

---

# Setup
## External Sensors
- Set up an isosceles triangle of IR LEDs above the camera
- These LEDs should be fairly close together, but far enough apart for the camera to identify each one seperately
- The distance between the camera and the LEDs determines the tracking area

## Raspberry Pi
- Get I2C set up
- Connect the IR Camera to the I2C1 ports on the Raspberry Pi. Note that the Vcc should be connected to 3.3V and **NOT** 5V, as the IR Tracking Camera is a 3.3V device
- Set up the pigpiodaemon (pigpiod) to run on boot, as it is required for the script to access the GPIO
- Modify the settings in PositionTracker.py for your setup for the correct ports and measurements

---

# Running the script
- run ```python3 PositionTracker.py```
