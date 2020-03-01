import sys
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

devices = [27, 22, 23, 24]

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
    action = str(message.payload.decode("utf-8")).strip().lower()
    print("handle_command::received command with topic ", message.topic, "and payload ", message.payload)
    client.publish("helloliam/geyser/lastcommand", action)
    if action == "on" or action == "1":
        g.output(27, g.LOW)
        print("HandleCommand::on command received")
        client.publish("helloliam/geyser/status", "ON")
        print("HandleCommand::Turning HelloGeyser on")
    elif action == "off" or action == "0":
        g.output(27, g.HIGH)
        print("HandleCommand::off command received")
        client.publish("helloliam/geyser/status", "OFF")
        print("HandleCommand::Turning HelloGeyser off")
    elif action == "toggle":
        print("HandleCommand::toggle command received")
        if g.input(27) == g.HIGH:
            g.output(27, g.LOW)
            client.publish("helloliam/geyser/status", "ON")
        else:
            g.output(27, g.HIGH)
            client.publish("helloliam/geyser/status", "OFF")

        print("HandleCommand::toggling HelloGeyser status")
    elif action == "status":
        print("HandleCommand::Status command received")
        print("HandleCommand::checking status")
        if g.input(27) == g.HIGH:
            client.publish("helloliam/geyser/status", "OFF")
        else:
            client.publish("helloliam/geyser/status", "ON")
    elif action == "pulse":
        startLoop()
    elif action == "allon":
        g.output(27, 0)
        g.output(22, 0)
        g.output(23, 0)
        g.output(24, 0)
    elif action == "alloff":
        g.output(27, 1)
        g.output(22, 1)
        g.output(23, 1)
        g.output(24, 1)
    else:
        print("ToggleGeyser::Command not recognized")
        client.publish("helloliam/geyser/status", "Unknown action")


client = mqtt.Client("HelloGeyser")
client.connect("127.0.0.1", 1883)
client.on_connect = on_connect
client.on_message = on_message

client.publish("helloliam/geyser/connection", "Hello! I am connected")
client.subscribe("helloliam/geyser/cmnd")
client.loop_start()

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

    if int(t.strftime("%M")) % 2 == 0:
        client.publish("helloliam/geyser/hoststatus", sys.api_version)

g.cleanup()
