import time
# from CUSTOM_PACKAGES import LCD as lcd_module
import cgi

def main():
	lcd = lcd_module.LCD()
	formData = cgi.FieldStorage()
	message = formData.getvalue('message')
	# lcd.print_string("Hello World")
	# time.sleep(1)
	# lcd.cleanup()

if __name__ == "__main__":
    main()
