from sense_hat import SenseHat
import time

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

shake_strength = 1
while True:
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x = abs(x)
    y = abs(y)
    z = abs(z)

    if x > shake_strength or y > shake_strength or z > shake_strength:
		sense.set_pixels(image)
    else:
        sense.clear()