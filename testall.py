import RPi.GPIO as GPIO
import time as time

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
GPIO.setup(2, GPIO.OUT) # GPIO Assign mode
GPIO.setup(3, GPIO.OUT) # GPIO Assign mode
GPIO.setup(4, GPIO.OUT) # GPIO Assign mode
GPIO.setup(5, GPIO.OUT) # GPIO Assign mode

GPIO.output(2, GPIO.LOW) # out
time.sleep(0.5)
GPIO.output(3, GPIO.LOW) # out
time.sleep(0.5)
GPIO.output(4, GPIO.LOW) # out
time.sleep(0.5)
GPIO.output(5, GPIO.LOW) # out
time.sleep(5)

GPIO.output(2, GPIO.HIGH) # out
GPIO.output(3, GPIO.HIGH) # out
GPIO.output(4, GPIO.HIGH) # out
GPIO.output(5, GPIO.HIGH) # out