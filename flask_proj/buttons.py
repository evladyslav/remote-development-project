import RPi.GPIO as GPIO
import time


PINS = [17, 18, 19, 20]


def init_buttons():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in PINS:
        GPIO.setup(pin, GPIO.OUT) 


def simulate(pin): 
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.5) 
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.5)


def press_button(button):
    if button == 'button1':
        pin = PINS[0]
        simulate(pin)

    if button == 'button2':
        pin = PINS[1]
        simulate(pin)    

    if button == 'button3':
        pin = PINS[2]
        simulate(pin)   

    if button == 'button4':
        pin = PINS[3]
        simulate(pin)   