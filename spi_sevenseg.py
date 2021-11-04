#!/usr/bin/python
import spidev
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

seg_pin4 = 29
GPIO.setup(seg_pin4, GPIO.OUT)
seg_pin5 = 31
GPIO.setup(seg_pin5, GPIO.OUT)
seg_pin6 = 33
GPIO.setup(seg_pin6, GPIO.OUT)
seg_pin7 = 36
GPIO.setup(seg_pin7, GPIO.OUT)
seg_pin8 = 37
GPIO.setup(seg_pin8, GPIO.OUT)

GPIO.output(seg_pin1, True)

spi_bus = 0 # SPI0
device = 0  # CE is active low on slave

spi = spidev.SpiDev()

spi.open(spi_bus, device)
spi.max_speed_hz = 10000000 # 10MHz

control_byte = 0b01000
A_ZERO = 0
A_ONE = 0
opcode = control_byte << 3 | A_ONE << 2 | A_ZERO << 1
read_mode = opcode | 0b1
write_mode = opcode | 0b0

register = 0x00 
data = 0b00000000 # set all output
spi.xfer([write_mode, register, data])

register = 0x09
data = 0b11111111
spi.xfer2([write_mode, register, data])

response = spi.xfer2([read_mode, register, 0x0])
print(response)

time.sleep(30)
print("done")
spi.close()
GPIO.cleanup()
