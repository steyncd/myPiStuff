import RPi.GPIO as GPIO
import time as time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
GPIO.setup(27, GPIO.OUT) # GPIO Assign mode

print("setting output to low")
GPIO.output(27, GPIO.LOW) # out
time.sleep(4)

print("setting output to high")
GPIO.output(27, GPIO.HIGH) # out

GPIO.cleanup()
