import time
import RPi.GPIO as GPIO

class LCD:

	RS  = 37 # PIN_4
	RW  = 36 # PIN_5
	EN  = 33 # PIN_6

	DB0 = 31 # PIN_7
	DB1 = 29 # PIN_8
	DB2 = 32 # PIN_9
	DB3 = 22 # PIN_10
	DB4 = 18 # PIN_11
	DB5 = 16 # PIN_12
	DB6 = 15 # PIN_13
	DB7 = 13 # PIN_14
	gpio_pins = [DB0, DB1, DB2, DB3, DB4, DB5, DB6, DB7]


	def __init__(self):
		self.LCD_init()
		self.GPIO_init()


	def print_string(self, data_string):
		'''
		Function:   print_string()
		Parameters: data_string
		Returns:    void
		Takes string input and prints on LCD
		'''
		self.LCD_clear()
		adr = 0
		for char in data_string:
			if(adr == 16):
				adr = 64
			self.send_data(ord(char), adr)
			adr += 1

	def send_data(self, data, adr):
		'''
		Function:   send_data()
		Parameters: data, address
		Returns:    void
		Sends data to LCD
		'''
		self.send_cmd(adr | 0b10000000)
		GPIO.output(RS, True) # Select Data Register
		GPIO.output(RW, False)# Set to Write 

		self.write_gpio(data)

		GPIO.output(EN, True)# Enable On
		self.__delay_ms(1)  
		GPIO.output(EN, False)# Enable Off
		self.__delay_ms(3)


	def send_cmd(self, cmd):
		'''
		Function:   send_cmd()
		Parameters: cmd - command to send
		Returns:    void
		Sends command to LCD
		'''
		GPIO.output(RS, False) # Select Instruction Register
		GPIO.output(RW, False) # Set to Write 

		self.write_gpio(cmd)

		GPIO.output(EN, True)# Enable On
		self.__delay_ms(1)  
		GPIO.output(EN, False)# Enable Off
		self.__delay_ms(3)


	def LCD_clear(self):
		'''
		Function:   LCD_clear()
		Parameters: void
		Returns:    void
		Clears display
		'''
		self.send_cmd(0b00000001)


	def LCD_init(self):
		'''
		Function:   LCD_initialize()
		Parameters: void
		Returns:    void
		Initializes LCD
		'''
		self.__delay_ms(100)
		GPIO.output(EN, False)		# Enable Off
		self.__delay_ms(1)
		self.send_cmd(0b00111000)   # Use 5x7 char, 2 lines, 8-bit data
		self.__delay_ms(1)
		self.send_cmd(0b00001100)   # Blink cursor OFF, cursor OFF, Display ON
		self.__delay_ms(1)
		self.LCD_clear()
		self.__delay_ms(1)

	def GPIO_init(self):
		GPIO.setmode(GPIO.BOARD)

		GPIO.setup(RS, GPIO.OUT)
		GPIO.setup(RW, GPIO.OUT)
		GPIO.setup(EN, GPIO.OUT)
		GPIO.setup(DB0, GPIO.OUT)
		GPIO.setup(DB1, GPIO.OUT)
		GPIO.setup(DB2, GPIO.OUT)
		GPIO.setup(DB3, GPIO.OUT)
		GPIO.setup(DB4, GPIO.OUT)
		GPIO.setup(DB5, GPIO.OUT)
		GPIO.setup(DB6, GPIO.OUT)
		GPIO.setup(DB7, GPIO.OUT)


	def write_gpio(self, data):
	'''
	'''
		bit_comparator = 0b1
		for pin in gpio_pins:
			GPIO.output(pin, bit_comparator & data)
			bit_comparator = bit_comparator << 1


	def __delay_ms(self, ms):
		'''
		Function:   __delay_ms()
		Parameters: void
		Returns:    void
		Takes ms input and sleeps for that amount of time
		'''
		time.sleep(ms/1000)

	def cleanup(self):
		self.LCD_clear()
		GPIO.cleanup()