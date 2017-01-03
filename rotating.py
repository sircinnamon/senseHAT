from sense_hat import SenseHat

sense = SenseHat()

r = [255,0,0]
e = [0,0,0]
image = [
e,e,e,r,r,e,e,e,
e,e,e,r,r,e,e,e,
e,e,e,r,r,e,e,e,
e,e,e,r,r,e,e,e,
e,e,e,r,r,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,r,r,e,e,e,
e,e,e,r,r,e,e,e
]

sense.set_pixels(image)

while True:
    x = sense.get_accelerometer_raw().['x']
    y = sense.get_accelerometer_raw().['y']

    x = round(x, 0)
    y = round(y, 0)

    if x == -1:
        sense.set_rotation(180)
    elif y == 1:
        sense.set_rotation(90)
    elif y == -1:
        sense.set_rotation(270)
    else:
        sense.set_rotation(0)