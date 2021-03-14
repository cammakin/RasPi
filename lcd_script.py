#!/usr/bin/python
# Main File for Project
# Author: Cameron Makin
# Date: 03/14/2021
# Notes: 
import time
from CUSTOM_PACKAGES import LCD as lcd_module

def main():
    lcd = lcd_module.LCD()
    lcd.print_string("Hey Alexa,      hi!             ")
    time.sleep(1)
    lcd.cleanup()

if __name__ == "__main__":
    main()