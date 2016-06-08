"""This is the actual module for using the IR camera with the Pi."""

import pigpio
from time import sleep


class IRCamera:
    """Class for handling sensor communication."""

    def __init__(self, i2c_bus=1, sensor_address=0x58):
        """
        Initialize the IR Camera.

        Parameters:
            i2c_bus: The number of the i2c bus (default 1)
            sensor_address: the i2c port for the camera (default 0x58)
        """
        # store the parameters
        self.i2c_bus = i2c_bus
        self.sensor_address = sensor_address

        # create the pigpio object and connect to the device
        self.pi = pigpio.pi()
        self.device = self.pi.i2c_open(i2c_bus, self.sensor_address)

        # Initialize the sensor itself
        self.__initialize_sensor()

    def __initialize_sensor(self):
        """Send the commands to the IR camera to ready it for use."""
        init_commands = (
            [0x30, 0x01, 0x30, 0x08, 0x06, 0x90, 0x08, 0xC0, 0x1A, 0x40, 0x33, 0x33]
        )
        for i, j in zip(init_commands[0::2], init_commands[1::2]):
            self.pi.i2c_write_byte_data(self.device, i, j)
            sleep(0.01)

    def get_positions(self):
        """
        Ask the sensor for positions of IR emitters.

        Returns:
            List of found IR emitters in [x, y] format.
            Returns an empty list if none are found.
        """
        self.pi.i2c_write_byte(self.device, 0x36)
        data = self.pi.i2c_read_i2c_block_data(self.device, 0x36, 16)

        # reset the positions list
        positions = list()

        # process the data received over i2c
        i = 0
        for j in range(1, 11, 3):
            x = data[1][j] + ((data[1][j+2] & 0x30) << 4)
            y = data[1][j+1] + ((data[1][j+2] & 0xC0) << 2)
            i += 1
            if x != 1023 or y != 1023:  # 1023,1023 means NOT FOUND
                positions.append([x, y])  # append to list

        # Note that if nothing was found, positions will be an empty list
        return positions

    def close_connection(self):
        """Close the I2C connection."""
        self.pi.close(self.device)
