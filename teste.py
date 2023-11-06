import time


ground = {
    "maxSpeed": 5,
    "acceleration": 0.5,
    "deceleration": 0.5,
}

speed = [-7.8,0]
while True:
    if speed[0] < -ground["maxSpeed"]: # decelerate
        speed[0] = speed[0] + ground["deceleration"] if speed[0] < -ground["maxSpeed"] - ground["deceleration"] else -ground["maxSpeed"]

    else:
        speed[0] = max(speed[0]-ground["deceleration"],0) if speed[0] > 0 else min(speed[0]+ground["deceleration"],0)

    print(speed[0])
    time.sleep(1)
