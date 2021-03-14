#!/usr/bin/python
# File for SPI IO Expander
# Author: Cameron Makin
# Date: 03/14/2021
# Notes: 

#TODO: Init with a read for any registers and keep track of their bits 
#	   as they are changed to mitigate a read per every write


#		GP0 = Pin 10 = LSB

import spidev

class IC_MCP23S08:

    def __init__(self, A_ZERO, A_ONE):

        self.spi = self.spidev_init()
        
        self._CONTROL_BYTE_PREFIX = 0b01000 #Every control has this prefix
        self._GPIO_ADDR = 0x09 #Address of the GPIO Register
        self.IO_DIR_ADDR = 0x00 #Address of IO_DIR Register
     
        # Init IC address
        self.A_ZERO = A_ZERO
        self.A_ONE 	= A_ONE

        #  Instruction control_byte (opcode) is a static 5bits + device addr
        self.control_byte = self._CONTROL_BYTE_PREFIX << 3 | A_ONE << 2 | A_ZERO << 1
        
        # Reset IO to all Outputs
        self.config_io_dir(0x00)


    def WRITE_GPIO_PIN(self, pin_num, val):
        '''
        This will set Pin pin_num to Value val (0 or 1)
        '''
        # Check for valid params
        if(val != 0 and val != 1):
            return
        if(pin_num > 7 or pin_num < 0):
            return

        opcode = self.control_byte
        data = self.write_bit(pin_num, val, self.READ_REG(self._GPIO_ADDR)[2])
        self.spi.xfer([opcode, self._GPIO_ADDR, data])


    def READ_GPIO_PIN(self, pin_num):
        '''
        Reads the value of a GPIO Pin
        '''
        opcode = self.control_byte | 0b1
        if(pin_num > 7 or pin_num < 0):
            return -1
        try:
            pin_val = bin(self.spi.xfer2([opcode, self._GPIO_ADDR, 0x0])[2])[pin_num]
        except IndexError:
            return 0
        return pin_val

    def WRITE_REG(self, reg, data):
        '''
        Writes provided date to provided register
        '''
        opcode = self.control_byte
        self.spi.xfer([opcode, reg, data])

    def READ_REG(self, reg_addr):
        '''
        Returns value in provided register
        '''
        opcode = self.control_byte | 0b1
        return self.spi.xfer2([opcode, reg_addr, 0x0])


    def spidev_init(self):
        '''
        Init SPI from Pi to IC using spidev package
        '''
        spi_bus = 0  # SPI0 = 0; SPI1 = 1
        device  = 0  # CE is active low on slave
        spi = spidev.SpiDev()
        spi.open(spi_bus, device)
        spi.max_speed_hz = 10000000 # 10MHz
        return spi


    def write_bit(self, bit, val, bin_string):
        '''
        Function write_bit: Takes a binary string and modifies a single bit in it.
        Use this to preformat the 8bits that will be sent to the IC
        Input: bit - value of significance of the bit you want to modify
            val - value (1 or 0) you want the bit to become
            bin_string - binary string you want to modify
        Output: binary string with single bit updated
        '''
        current_bit_value = (int(bin_string) & (0b1 << bit)) >> bit
        if(current_bit_value == val):
            return bin_string
        else:
            if(current_bit_value == 0):
                return bin_string + (0b1 << (bit))
            else:
                return  bin_string - (0b1 << (bit))

    def config_io_dir(self, directions):
        '''
        Configres the IO Direction of the GPIO Pins
        '''
        self.WRITE_REG(self.IO_DIR_ADDR, directions)            

    
    def cleanup(self):
        '''
        # Functinon cleanup: closes spi
        '''
        self.spi.close()

    def test_module(self):
        print("You have accessed a method of the IC_MCP23S08 module")
