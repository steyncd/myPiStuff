import RPi.GPIO as g
import time as t

g.setmode(g.BCM)

g.setup(27,g.OUT)
g.setup(22,g.OUT)
g.setup(23,g.OUT)
g.setup(24,g.OUT)

devices = [27,22,23,24]

action = 1
print("Starting first loop")
for i in range(30):
    print("Starting device loop " + str(i) + " with action " + str(action))
    for device in devices:
        print("setting device " + str(device) + " to state " + str(action))		
        g.output(device,action)
        t.sleep(0.08)

    print("reversing list")
    devices.reverse()
    print("switching action")
    if action == 0:
        action = 1
    else:
        action = 0


g.cleanup()
