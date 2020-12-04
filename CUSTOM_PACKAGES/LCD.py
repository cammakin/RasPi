import time
import RPi.GPIO as GPIO
from CUSTOM_PACKAGES import IC_MCP23S08 as io_expander

class LCD:


    def __init__(self):
            # Name of Pin = Pi Pin Num # LCD Pin Num
            self.RS  = 37 # PIN_4
            self.RW  = 36 # PIN_5
            self.EN  = 33 # PIN_6

            self.io_mod = io_expander.IC_MCP23S08(0, 0)
            self.GPIO_init()
            self.LCD_init()

    def print_string(self, data_string):
            '''
            Function:   print_string()
            Parameters: data_string
            Returns:    void
            Takes string input and prints on LCD
            '''
            self.LCD_clear()
            adr = 0
#             #Clear Screen
#             if(len(data_string)<32):
#                 n = 32-len(data_string)
#                 while(n>0):
#                     data_string = data_string + " "
#                     n = n - 1
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
            GPIO.output(self.RS, True) # Select Data Register
            GPIO.output(self.RW, False)# Set to Write 
            print("sending: ", data, " to: ", adr)
            self.io_mod.WRITE_REG(0x09, data)

            GPIO.output(self.EN, True)# Enable On
            self.__delay_ms(2)  
            GPIO.output(self.EN, False)# Enable Off
            self.__delay_ms(3)


    def send_cmd(self, cmd):
            '''
            Function:   send_cmd()
            Parameters: cmd - command to send
            Returns:    void
            Sends command to LCD
            '''
            GPIO.output(self.RS, False) # Select Instruction Register
            GPIO.output(self.RW, False) # Set to Write 

            self.io_mod.WRITE_REG(0x09, cmd)
            
            GPIO.output(self.EN, True)# Enable On
            self.__delay_ms(1)  
            GPIO.output(self.EN, False)# Enable Off
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
            GPIO.output(self.EN, False)             # Enable Off
            self.__delay_ms(1)
            self.send_cmd(0b00111000)   # Use 5x7 char, 2 lines, 8-bit data
            self.__delay_ms(1)
            self.send_cmd(0b00001100)   # Blink cursor OFF, cursor OFF, Display ON
            self.__delay_ms(1)
            self.LCD_clear()
            self.__delay_ms(1)

    def GPIO_init(self):
            GPIO.setmode(GPIO.BOARD)

            GPIO.setup(self.RS, GPIO.OUT)
            GPIO.setup(self.RW, GPIO.OUT)
            GPIO.setup(self.EN, GPIO.OUT)
    #                 GPIO.setup(self.DB0, GPIO.OUT)
    #                 GPIO.setup(self.DB1, GPIO.OUT)
    #                 GPIO.setup(self.DB2, GPIO.OUT)
    #                 GPIO.setup(self.DB3, GPIO.OUT)
    #                 GPIO.setup(self.DB4, GPIO.OUT)
    #                 GPIO.setup(self.DB5, GPIO.OUT)
    #                 GPIO.setup(self.DB6, GPIO.OUT)
    #                 GPIO.setup(self.DB7, GPIO.OUT)


    def write_gpio(self, data):
            '''
            '''
            bit_comparator = 0b1
            for pin in self.gpio_pins:
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
            self.io_mod.cleanup()

