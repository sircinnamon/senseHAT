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
purple = [76,0,153]

#Pieces. index 0 is the origin. 1-3 are the rest in rotation 1, relative to origin
piece_1 = [(0,0),(0,-1),(0,1),(0,2)] #line
piece_2 = [(0,0),(0,-1),(1,0),(1,-1)] #square
piece_3 = [(0,0),(1,0),(0,-1),(0,-2)] #L
piece_4 = [(0,0),(-1,0),(0,-1),(0,-2)] #reverse L
piece_5 = [(0,0),(-1,0),(0,-1),(1,-1)] #reverse Z
piece_6 = [(0,0),(1,0),(0,-1),(-1,-1)] #Z
piece_7 = [(0,0),(1,0),(0,-1),(-1,0)] #T

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
	remaining_pieces = list(all_pieces)
	shuffled = []
	while(len(remaining_pieces) > 1):
		print(str(len(remaining_pieces)))
		rand = randint(0,len(remaining_pieces)-1)
		shuffled.append(remaining_pieces.pop(rand))
	shuffled.extend(remaining_pieces)
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
	screen = list(game_map)
	for coord in active_piece:
		if(tuple_to_index(coord) > 0 and tuple_to_index(coord) < 64):
			screen[tuple_to_index(coord)] = piece_colour
	return screen

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

def lower_piece(piece):
	new_piece = []
	for coord in piece:
		new_piece.append((coord[0],coord[1]+1))
	print(str(new_piece))
	return new_piece

def check_collision(game_map, piece):
	#check if piece overlaps a part of the game map or the bottom edge
	for coord in piece:
		if (coord[1] > 7):
			print("collision: bottom "+str(coord))
			return True
		elif game_map[tuple_to_index(coord)] != e and (tuple_to_index(coord) > 0):
			print("collision: heap ("+str(game_map[tuple_to_index(coord)]) + ") "+str(coord))
			return True
	return False

def add_piece_to_map(piece, game_map, colour):
	for coord in piece:
		if(tuple_to_index(coord) > 0 and tuple_to_index(coord) < 64):
			game_map[tuple_to_index(coord)] = colour
	return game_map

def above_top(piece):
	for coord in piece:
		if(coord[1] < 0):
			return True
	return False

def crosses_edge(piece):
	left_side=False
	right_side=False
	for coord in piece:
		if(coord[0] > 7 or coord[0] < 0):
			return True
	return False

def move(move_type, piece, game_map):
	#only perform if legal
	new_piece = []
	for tile in piece:
		new_piece.append((tile[0]+move_type[0],tile[1]+move_type[1]))
	i = move_type[2]
	while(i > 0):
		new_piece = rotate_piece(piece)
		i = i-1

	if(crosses_edge(new_piece)):
		return piece
	elif(check_collision(game_map,new_piece)):
		return piece
	return new_piece


running = True
spawn = (4,-1)
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
locked_in = False
input_move = (0,0,0)

while running:
	#get input
	events = sense.stick.get_events()
	if len(events) > 0:
		event = events[0];
		if(event.direction == "up"):
			#rotate?
			print("up move")
			input_move = (0,0,1)
		elif(event.direction == "down"):
			#double drop?
			print("down move")
			#input_move = (0,1,0)
		elif(event.direction == "left"):
			#move left
			print("left move")
			input_move = (-1,0,0)
		elif(event.direction == "right"):
			#move right
			print("right move")
			input_move = (1,0,0)

	#perform input if needed and legal
	if(not locked_in):
		current_piece = move(input_move, current_piece, game_map)
	input_move = (0,0,0)
	
	#lower piece & check for piece "lock in"
	lowered_piece = lower_piece(current_piece)
	if check_collision(game_map, lowered_piece):
		#lock in at prev position
		game_map = add_piece_to_map(current_piece, game_map, current_piece_colour)
		locked_in = True
	else:
		current_piece = lowered_piece

	#check if locked in above top line to trigger game over
	if(locked_in and above_top(lowered_piece)):
		game_over(game_map,score)

	#check for lines to remove
	#generate new piece if needed
	if(locked_in):
		locked_in = False
		if(len(piece_queue) == 0):
			piece_queue = deque(shuffle_pieces())
		current_piece = piece_queue.popleft()
		current_piece_colour = current_piece[1]
		current_piece = place_piece(current_piece[0],spawn)

	#sleep
	sense.set_pixels(create_screen(current_piece, current_piece_colour, game_map))
	time.sleep(0.5)



