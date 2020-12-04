import time
from CUSTOM_PACKAGES import LCD as lcd_module

def main():
    lcd = lcd_module.LCD()
    lcd.print_string("Hey Alexa,      cum on my face! ")
    time.sleep(1)
    lcd.cleanup()

if __name__ == "__main__":
    main()