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
teal = [0,255,255]
yellow = [255,255,0]
orange = [255,128,0]
dark_blue = [0,0,102]
dark_green = [0,204,0]
dark_red = [204,0,0]
purple [76,0,153]

#Pieces. index 0 is the origin. 1-3 are the rest in rotation 1, relative to origin
piece_1 = [(0,0),(0,-1),(0,1),(0,2)] #line
piece_2 = [(0,0),(0,-1),(1,0),(1,-1)] #square
piece_3 = [(0,0),(1,0),(0,-1),(0,-2)] #L
piece_4 = [(0,0),(-1,0),(0,-1),(0,-2)] #reverse L
piece_5 = [(0,0),(-1,0),(0,-1),(1,-1)] #reverse Z
piece_6 = [(0,0),(1,0),(0,-1),(-1,-1)] #Z
piece_7 = [(0,0),(1,0),(0,-1),(-1,-1)] #T

all_pieces = [(piece_1,teal),(piece_2,yellow),(piece_3,orange),(piece_4,dark_blue),(piece_5,dark_green),(piece_6,dark_red),(piece_7,purple)]
#Program for playing the game "Tetris"

def tuple_to_index(tup):
	return tup[0]+(tup[1]*8)

def index_to_tuple(index):
	return ((index%8), (index-(index%8))/8)

def rotate_piece(piece):
	#index 0 is relative origin
	new_piece = [piece[0],rotate_tile(piece[0],piece[1]),rotate_tile(piece[0],piece[2]),rotate_tile(piece[0],piece[3])]
	return new_piece

def rotate_tile(origin, tile):
	#return the coordinates of a point rotated clockwise around an origin
	tile_relative = ((tile[0]-origin[0]),(tile[1]-origin[1]))
	tile_rotated = ((-1*tile_relative[1]), tile_relative[0])
	tile_coordinates = ((tile_rotated[0]+origin[0]),(tile_rotated[1]+origin[1]))
	return tile_coordinates 

def shuffle_pieces():
	remaining_pieces = all_pieces
	shuffled = []
	while(len(remaining_pieces) > 1):
		rand = randint(0,len(remaining_pieces))
		shuffled.append(remaining_pieces.pop(rand))
	shuffled.append(remaining_pieces.pop())
	return shuffled

def place_piece(template, point):
	#convert a relative position list to actual
	coords = []
	coords.append(((template[0][0]+point[0]),(template[0][1]+point[1])))
	coords.append(((template[1][0]+point[0]),(template[1][1]+point[1])))
	coords.append(((template[2][0]+point[0]),(template[2][1]+point[1])))
	coords.append(((template[3][0]+point[0]),(template[3][1]+point[1])))
	return coords

def create_screen(active_piece,piece_colour,game_map):
	for index,coord in enumerate(active_piece):
		game_map[tuple_to_index(coord)] = piece_colour
	return game_map

def game_over(end_screen, score):
	i = 0
	while(i < 4):
		sense.set_pixels(end_screen)
		time.sleep(0.2)
		sense.clear()
		time.sleep(0.2)
		i += 1
	sense.show_message("SCORE: "+ str(score))
	sys.exit()

running = True
spawn = (4,0)
game_map = [
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e
]
piece_queue = deque(shuffle_pieces())
current_piece = piece_queue.popleft()
current_piece_colour = current_piece[1]
current_piece = place_piece(current_piece[0],spawn) 
score = 0
sense.set_pixels(create_screen(current_piece, current_piece_colour, game_map))

while running:
	events = sense.stick.get_events()
	if len(events) > 0:
		event = events[0];
		if(event.direction == "up"):
		elif(event.direction == "down"):
		elif(event.direction == "left"):
		elif(event.direction == "right"):


