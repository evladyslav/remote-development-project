import RPi.GPIO as GPIO
import time


PINS = [17, 18, 19, 20]


def init_buttons():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in PINS:
        GPIO.setup(pin, GPIO.OUT) 


def press_button(button):
    if button == 'button1':
        pin = PINS[0]
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5) 
        GPIO.output(pin, GPIO.HIGH) 
    elif button == 'button2':
        pin = PINS[1]
        GPIO.output(pin, GPIO.LOW) 
        time.sleep(0.5)  
        GPIO.output(pin, GPIO.HIGH) 
    elif button == 'button3':
        pin = PINS[2]
        GPIO.output(pin, GPIO.LOW) 
        time.sleep(0.5) 
        GPIO.output(pin, GPIO.HIGH) 
    elif button == 'button4':
        pin = PINS[3]
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(pin, GPIO.HIGH) 
    