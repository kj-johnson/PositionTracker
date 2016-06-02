"""This module tracks your location."""

from IRCamera import IRCamera
from time import sleep


# IMPORTANT NOTES
# This tracker requires the data to be set in the SETTINGS section.
# Hardware-wise, this tracker requires an isosceles triangle (NOT EQUILATERAL)
# of IR LEDs to be mounted above the camera
# Ideally, the triangle will point north for ease of accuracy checking using a
# magnetometer (optional)

# SETTINGS
i2c_bus = 1  # i2c bus number (either 0 or 1)
ir_camera_port = 0x58
ir_emitter_pattern_width = 3  # inches
ir_emitter_pattern_height = 6  # inches
ceiling_height = 96  # inches
has_magnetometer = False  # enables error correction using magnetometer


# make your camera object
camera = IRCamera(i2c_bus, ir_camera_port)

# calculate the size of the square you can travel in (so you can report your
# location accurately)
# We factor in a 10% overlap in the hopes of making absolutely sure we can't
# travel too far and lose sight of the sensor

# Testing
while True:
    sleep(0.01)  # needs to wait before trying to read again
    positions = camera.get_positions()
    if len(positions) > 0:
        print(positions)
