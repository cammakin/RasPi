#!/usr/bin/python
# Main File for Project
# Author: Cameron Makin
# Date: 03/14/2021
# Notes: 
import time
from CUSTOM_PACKAGES import LCD as lcd_module

def main():
    lcd = lcd_module.LCD()
<<<<<<< HEAD
    lcd.print_string("Hey Alexa,      hi!             ")
=======
    lcd.print_string("asd")
    # "                                "
>>>>>>> eda66f235de2de30f8bfad89846f8593e4d0c511
    time.sleep(1)
    lcd.cleanup()

if __name__ == "__main__":
    main()