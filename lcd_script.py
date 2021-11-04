#!/usr/bin/python3
import time
import threading
from CUSTOM_PACKAGES import LCD as lcd_module
from flask import Flask, request, render_template

app = Flask(__name__)
lcd = lcd_module.LCD()
global_string = "STARTING UP"
#lcd_thread = threading.Thread(target=lcd_driver)

@app.route('/')
def my_form():
    return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    global_string = processed_text
    lcd.print_string(global_string)
    return render_template("my-form-two.html", user_data=processed_text)

    

if __name__ == "__main__":
    #lcd_thread.start()
    lcd.print_string(global_string)
    app.run(debug=True, host='0.0.0.0')
    lcd.cleanup()
