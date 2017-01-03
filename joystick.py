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

while True:
    joystick_pressed = False
    while not joystick_pressed:
        sense.set_pixels(image)
        time.sleep(0.5)
        if len(sense.stick.get_events()) > 0: joystick_pressed = True
        sense.clear()
        time.sleep(0.5)
        if len(sense.stick.get_events()) > 0: joystick_pressed = True
    sense.show_message("Nice")
