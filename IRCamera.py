

import pigpio
from time import sleep

class IRCamera:
    """"Class for handling sensor communication"""
    def __init__(self, i2c_bus, sensor_address):
        self.i2c_bus = i2c_bus
        self.sensor_address = sensor_address
        self.pi = pigpio.pi()
        self.device = self.pi.i2c_open(i2c_bus, self.sensor_address)
        self.positions = list()
        # Initialize the sensor
        self.__initialize_sensor()

    def __initialize_sensor(self):
        init_commands = [0x30, 0x01, 0x30, 0x08, 0x06, 0x90, 0x08, 0xC0, 0x1A, 0x40, 0x33, 0x33]
        for i, j in zip(init_commands[0::2], init_commands[1::2]):
            self.pi.i2c_write_byte_data(self.device, i, j)
            sleep(0.01)

    def get_positions(self):

        self.pi.i2c_write_byte(self.device, 0x36)
        data = self.pi.i2c_read_i2c_block_data(self.device, 0x36, 16)

        # reset the positions list
        self.positions = list()

        # process the data received over i2c
        i = 0
        for j in range(1, 11, 3):
            x = data[1][j] + ((data[1][j+2] & 0x30) << 4)
            y = data[1][j+1] + ((data[1][j+2] & 0xC0) << 2)
            i += 1
            if x != 1023 or y != 1023:  # 1023,1023 is the designated value for NOT FOUND
                self.positions.append([x, y])  # append to list

        # Note that if nothing was found, positions will be an empty list
        return self.positions

    def close_connection(self):
        self.pi.close(self.device)
