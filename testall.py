import RPi.GPIO as GPIO
import time as time

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
GPIO.setup(27, GPIO.OUT) # GPIO Assign mode
GPIO.setup(22, GPIO.OUT) # GPIO Assign mode
GPIO.setup(23, GPIO.OUT) # GPIO Assign mode
GPIO.setup(24, GPIO.OUT) # GPIO Assign mode

GPIO.output(27, GPIO.LOW) # out
time.sleep(1)
GPIO.output(22, GPIO.LOW) # out
time.sleep(1)
GPIO.output(23, GPIO.LOW) # out
time.sleep(1)
GPIO.output(24, GPIO.LOW) # out
time.sleep(5)

GPIO.output(27, GPIO.HIGH) # out
GPIO.output(22, GPIO.HIGH) # out
GPIO.output(23, GPIO.HIGH) # out
GPIO.output(24, GPIO.HIGH) # out

GPIO.cleanup()
