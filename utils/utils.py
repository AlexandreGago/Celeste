import random
def screen_shake(intensity, amplitude, times):
    direction = -1
    y_shake=1
    for _ in range(0, times):
        y_shake = random.randint(-1, 1)
        for x in range(0, amplitude, intensity):
            yield x * direction, y_shake*x
        for x in range(amplitude, 0, intensity):
            yield x * direction, y_shake*x
        direction *= -1
    while True:
        yield 0, 0