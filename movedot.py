from sense_hat import SenseHat
import time

sense = SenseHat()

r = [255,0,0]
e = [0,0,0]
image = [
e,e,e,e,e,e,e,e,
e,r,r,e,e,r,r,e,
e,r,r,e,e,r,r,e,
e,e,e,e,e,e,e,e,
e,e,e,r,r,r,e,e,
e,e,r,e,e,e,r,e,
e,r,e,e,e,e,e,r,
e,e,e,e,e,e,e,e
]
#Program for moving a dot around the grid using a joystick

def move(vertical, horizontal, x, y):
	x = x+horizontal
	y = y+vertical
	if(x>7 or x<0):
		x = -1
	if(y>7 or y<0):
		y = -1
	return x,y

def create_image(x,y):
	new_image = [e] * 64
	new_image[(8*y)+x] = r
	return new_image

running = True
sense.set_pixels(create_image(5,5))
x = 5
y = 5
while running:
	event = sense.stick.wait_for_event(emptybuffer=True)
	if(event.action == "released"):
		#do nothing
		x=x
	elif(event.direction == "up"):
		x, y = move(-1,0,x,y)
	elif(event.direction == "down"):
		x, y = move(1,0,x,y)
	elif(event.direction == "left"):
		x, y = move(0,-1,x,y)
	elif(event.direction == "right"):
		x, y = move(0,1,x,y)

	if(x == -1 or y == -1):
		running = False
	else:
		sense.set_pixels(create_image(x,y))
	time.sleep(0.1)
sense.show_message("Game Over")
sense.set_pixels(image)

