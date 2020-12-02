# Module for SPI IO Expander

#TODO: Init with a read for any registers and keep track of their bits 
#	   as they are changed to mitigate a read per every write


#		GP0 = Pin 10 = LSB

import spidev

class IC_MCP23S08:

	_CONTROL_BYTE_PREFIX = 0b01000
	_GPIO_ADDR = 0x09

	def __init__(self, A_ZERO, A_ONE):
		
		self.spidev_init()
		self.A_ZERO = A_ZERO	
		self.A_ONE 	= A_ONE
		self.control_byte = _CONTROL_BYTE_PREFIX << 3 | A_ONE << 2 | A_ZERO << 1
		self.gpio = READ_REG(_GPIO_ADDR)
		

	# This will set Pin pin_num to Value val (0 or 1)
	def WRITE_GPIO(self, pin_num, val):
		if(val != 0 or val != 1):
			return
		if(pin_num > 7 or pin_num < 0):
			return
		opcode = self.control_byte
		data = write_bit(pin_num, val, gpio)
		spi.xfer([opcode, _GPIO_ADDR, data])


	def READ_GPIO(self, pin_num):
		opcode = self.control_byte | 0b1

	def WRITE_REG(self, reg, data):
		opcode = self.control_byte
		spi.xfer([opcode, reg, data])

	def READ_REG(self, reg_addr):
		opcode = self.control_byte | 0b1
		return spi.xfer2([opcode, reg_addr, 0x0])[2]


	def spidev_init(self):
		spi_bus = 0  # SPI0 = 0; SPI1 = 1
		device  = 0  # CE is active low on slave
		self.spi = spidev.SpiDev()
		self.spi.open(spi_bus, device)
		self.spi.max_speed_hz = 10000000 # 10MHz


	'''
	# Function write_bit: Takes a binary string and modifies a single bit in it
	# Input: bit - value of significance of the bit you want to modify
	#		 val - value (1 or 0) you want the bit to become
	#	 	 bin_string - binary string you want to modify
	# Output: binary string with single bit updated
	'''
	def write_bit(self, bit, val, bin_string):
		current_bit_value = (bin_string & (0b1 << bit)) >> bit
		if(current_bit_value == val):
			return bin_string
		else:
			if(current_bit_value == 0):
				return bin_string + (0b1 << (bit))
			else:
				return  bin_string - (0b1 << (bit))


	'''
	# Functinon cleanup: closes spi
	'''
	def cleanup(self):
		self.spi.close()

	def test_module(self):
		print("You have accessed a method of the IC_MCP23S08 module")
		