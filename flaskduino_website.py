from flask import Flask, render_template, request, redirect, url_for, flash
from pyduino import Arduino
from flask_toastr import Toastr
from extra.pin_def import LED_PINS
import time
import signal

# intialize flask variable
app = Flask(__name__)
toastr = Toastr(app)

# set configuration
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['TOASTR_TIMEOUT'] = 5000
app.config['TOASTR_SHOW_METHOD'] = 'slideDown'
app.config['TOASTR_POSITION_CLASS'] = 'toast-top-center'

# set to True if you have an arduino connected to pc else set to False
haveArduino = False

# set global variables
author = "Anthony"
appTitle = "FlaskDuino"

# initialize connection to Arduino
# if your arduino was running on a serial port other than '/dev/ttyACM0/'
# declare: a = Arduino(serial_port='/dev/ttyXXXX')
if haveArduino == True:
    a = Arduino()
    time.sleep(3)

# declare the pins we're using
#LED_PINS = LED_PINS

# initialize the digital pin as output
#a.set_pin_mode(LED_PIN,'O')
for pin in LED_PINS:
    if haveArduino == True:
        a.set_pin_mode(int(pin["pin_num"]), pin["pin_mode"])

print('Arduino initialized')

# we are able to make 2 different requests on our webpage
# GET = we just type in the url
# POST = some sort of form submission like a button
@app.route('/')
def index():
    return render_template('index.html', appTitle=appTitle)

@app.route('/toggle_gpio_pins')
def toggle_gpio_pins():
    return render_template('toggle_gpio_pins.html', appTitle=appTitle, LED_PINS=LED_PINS)

@app.route('/servo_control')
def servo_control():
    return render_template('servo_control.html', appTitle=appTitle, LED_PINS=LED_PINS)

@app.route('/analog_read')
def analog_read():
    return render_template('analog_read.html', appTitle=appTitle, LED_PINS=LED_PINS)

@app.route('/pins/on/<int:id>', methods=['POST'])
def turn_on(id):
    if id is None:
        return 404
    else:
        pin_id = id

        if haveArduino == True:
            a.digital_write(pin_id, 1)

        flash(f'GPIO: {pin_id} turned on!', 'pin-on')

        return redirect('/toggle_gpio_pins')

@app.route('/pins/off/<int:id>', methods=['POST'])
def turn_off(id):
    if id is None:
        return 404
    else:
        pin_id = id

        if haveArduino == True:
            a.digital_write(pin_id, 0)

        flash(f'GPIO: {pin_id} turned off!', 'pin-off')

        return redirect('/toggle_gpio_pins')
    
@app.route('/pins/PWM/<int:id>/<int:control>', methods=['POST'])
def pwm_control(id, control):
    if id is None:
        return 404
    else:
        pin_id = id
        pin_control = control
        
        if haveArduino == True:
            a.analog_write(pin_id, pin_control)
            
        flash(f'GPIO: {pin_id} turned to {pin_control} !', 'message')
        
        return redirect('/servo_control')

def close_connections():
    if haveArduino == True:
        a.close

if __name__ == "__main__":

    if signal.CTRL_C_EVENT:
        if haveArduino == True:
            close_connections()

    # lets launch our webpage!
    # do 0.0.0.0 so that we can log into this webpage
    # using another computer on the same network later
    if haveArduino == False:
        app.run(host='0.0.0.0', debug=True)
        #app.run(host='127.0.0.1', debug=True)
    else:
        app.run(host='0.0.0.0')