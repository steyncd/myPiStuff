import RPi.GPIO as g
import time as t
import paho.mqtt.client as mqtt

g.setwarnings(False)
g.setmode(g.BCM)

g.setup(27, g.OUT)
g.setup(22, g.OUT)
g.setup(23, g.OUT)
g.setup(24, g.OUT)
g.setup(10, g.IN, pull_up_down=g.PUD_DOWN)
g.setup(9, g.IN, pull_up_down=g.PUD_DOWN)

devices = [27,22,23,24]

for device in devices:
    g.output(device, 1)

startLoopRunning = False
toggleLightRunning = False


def startLoop():
    global startLoopRunning
    startLoopRunning = True
    action = 1
    print("Starting first loop")
    for i in range(30):
        print("Starting device loop " + str(i) + " with action " + str(action))
        for device in devices:
            print("setting device " + str(device) + " to state " + str(action))
            g.output(device, action)
            t.sleep(0.08)

        print("reversing list")
        devices.reverse()
        print("switching action")
        if action == 0:
            action = 1
        else:
            action = 0
    startLoopRunning = False


def toggleLights():
    global toggleLightRunning
    toggleLightRunning = True
    for device in devices:
        g.output(device, 0)

    t.sleep(4)

    for device in devices:
        g.output(device, 1)

    toggleLightRunning = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Hello, Connected to MQTT Broker")

def on_message(client, userdata, message):
    print("message received")


client = mqtt.Client("HelloGeyser")
client.connect("127.0.0.1",1883)
client.on_connect = on_connect
client.on_message = on_message

client.publish("helloliam/geyser/connection","Hello! I am connected")
client.subscribe("helloliam/geyser/cmnd")


while True:
    if g.input(10) == g.HIGH:
        print("start button pressed")

    if g.input(10) == g.HIGH and not startLoopRunning:
        print("starting loop")
        startLoop()

    if g.input(9) == g.HIGH:
        print("toggle button pressed")

    if g.input(9) == g.HIGH and not toggleLightRunning:
        print("toggling lights")
        toggleLights()

g.cleanup()

