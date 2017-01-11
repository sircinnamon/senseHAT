from sense_hat import SenseHat
import time
from random import randint
from collections import deque
import sys

sense = SenseHat()

r = [255,0,0]
g = [0,255,0]
w = [255,255,255]
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
#Program for playing the game "Snake"

def move(vertical, horizontal, snake):
	x = x+horizontal
	y = y+vertical
	if(x>7 or x<0):
		x = -1
	if(y>7 or y<0):
		y = -1
	return x,y

def place_food(snake):
	#generate a random number N from 0 to (64-len(snake))
	#return the Nth empty tile coords
	place = randint(1, (64-len(snake)))
	i = 0; #records how many blank squares have been traversed
	j = 0;  #records how many squares have been traversed
	while(i != place):
		if(snake.count(index_to_tuple(j)) == 0):
			i += 1
		j += 1
	return index_to_tuple(j-1)

def create_screen(snake, food):
	new_image = [e] * 64
	for index,coord in enumerate(snake):
		new_image[tuple_to_index(coord)] = g
	new_image[tuple_to_index(food)] = w
	return new_image

def game_over(snake, food, score):
	end_screen = create_screen(snake, food)
	i = 0
	while(i < 4):
		sense.set_pixels(end_screen)
		time.sleep(0.2)
		sense.clear()
		time.sleep(0.2)
		i += 1
	sense.show_message("SCORE: "+ str(score))
	sys.exit()

def tuple_to_index(tup):
	return tup[0]+(tup[1]*8)

def index_to_tuple(index):
	return ((index%8), (index-(index%8))/8)

running = True
snake = deque([(4,4)]) #Head of snake starts here
score = 0
food = place_food(snake)
sense.set_pixels(create_screen(snake, food))
head = snake[0]
current_direction = (0,0)
while running:
	events = sense.stick.get_events()
	if len(events) > 0:
		event = events[0];
		if(event.direction == "up"):
			current_direction = (0,-1)
		elif(event.direction == "down"):
			current_direction = (0,1)
		elif(event.direction == "left"):
			current_direction = (-1,0)
		elif(event.direction == "right"):
			current_direction = (1,0)

	head = (head[0]+current_direction[0], head[1]+current_direction[1])
	
	if(head[0] > 7 or head[0] < 0 or head[1] > 7 or head[1] < 0):
		#hit walls
		game_over(snake, food, score)
		running = False
	elif(snake.count(head)>0 and current_direction != (0,0)):
		#hit self
		game_over(snake, food, score)
		running = False

	snake.appendleft(head)
	if(food == head):
		score += 1
		food = place_food(snake)
	else:
		snake.pop() 
	if(running):
		sense.set_pixels(create_screen(snake, food))
		time.sleep(0.5)

game_over(snake,food,score)

