import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
del_V = 6
GPIO.setup(del_V, GPIO.IN)
state = 1

while True:
    state = GPIO.input(del_V)
    GPIO.output(led, not state)