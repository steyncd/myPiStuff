import RPi.GPIO as GPIO
import time as time

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
GPIO.setup(2, GPIO.OUT) # GPIO Assign mode

GPIO.output(2, GPIO.LOW) # out
time.sleep(4)

GPIO.output(2, GPIO.HIGH) # out