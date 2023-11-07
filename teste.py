import time


ground = {
    "maxSpeed": 5,
    "acceleration": 0.5,
    "deceleration": 0.5,
}
air = {
    "maxSpeed": 5,
    "acceleration": 0.5,
    "deceleration": 0.5,
}

dash = {
    "power": 12,
}
jump = {
    "power": 10,
}
movement = [0,0,0]

speed = [0,12]

if movement[1] < 0 :
    if speed[1] > air["maxSpeed"]: #TODO
        print("1")
        speed[1] = speed[1] - air["deceleration"] if speed[1] > air["maxSpeed"] + air["deceleration"] else air["maxSpeed"]
    else:
        print("2")
        speed[1] -= min (jump["power"] - speed[1], 0) if speed[1] < 0 else jump["power"]
else:
    print("3")
    speed[1] = speed[1] + air["acceleration"] if speed[1] < air["maxSpeed"] else min(speed[0]+air["deceleration"],0)


print(speed)
time.sleep(1)
