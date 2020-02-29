#! /usr/bin/python3.5
import sys
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
cpio_channels=[4,5,6,12,13,16,17,18,19,20,21,22,23,24,25,26,27]# base channels
print("using ",sys.version) #what version of python
mode=GPIO.getmode()
print("mode is ",mode)
GPIO.setmode(GPIO.BCM)
mode=GPIO.getmode()
print("mode is ",mode)
GPIO.setup(4,GPIO.OUT)
GPIO.output(4,1)
print("value is ",GPIO.input(4))
GPIO.setup(5,GPIO.IN)
print("input value is ",GPIO.input(5))
GPIO.cleanup()
print("board ",GPIO.BOARD)
print("bcm ",GPIO.BCM)
