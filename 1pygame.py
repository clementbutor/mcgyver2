import os
from random import randint
import pygame



def load_maze():
	with open("macgyver_texte.txt") as f: 
		data = f.read() 
		lines = data.split('\n')
		maze = []
		for line in lines:
			maze.append([{" ":0, "#":1, "M":2, "G":3}[c] for c in line])
		return maze


def draw(maze, images, window, text_bag, text_fleche):
	window.fill((0, 0, 0))
	window.blit(text_bag, (730, 47))
	window.blit(text_fleche, (750, 94))



	row = 0
	for line in maze:
		col = 0
		for tile in line:
			x = col * 47
			y = row * 47
			if tile == 1:
				window.blit(images["wall_image"], (x, y))
			elif tile == 2:
				window.blit(images["mac_image"], (x, y))				
			elif tile == 3:
				window.blit(images["guardian_image"], (x, y))
			elif tile == 4:
				window.blit(images["tube_image"], (x, y))
			elif tile == 5:
				window.blit(images["needle_image"], (x, y))
			elif tile == 6:
				window.blit(images["ether_image"], (x, y))			
			col += 1	
		row += 1	
				

def randomize_components(maze):
	for tile in (4, 5, 6):
		while True:
			col, row = randint(0, 14), randint(0, 14)
			if maze[row][col]==0:
				maze[row][col]=tile
				break


def find_tile(maze, value):
#Donne la position de Mac (x,y)			

	for row_id, row in enumerate(maze):	
		for col_id, tile in enumerate(row):			
			if tile == value:
				return col_id, row_id
				

	return None				


def direction(maze, direc, bag):
	col, row = find_tile(maze, 2)
	if direc == "haut":
		if row > 0:
			if maze[row - 1][col]!=1:
				check_component(maze, row - 1, col, bag)
				maze[row][col]=0
				maze[row - 1][col] = 2		
	elif direc == "bas":
		if row < 14: 
			if maze[row + 1][col]!=1:
				check_component(maze, row + 1, col, bag)
				maze[row][col]=0
				maze[row + 1][col] = 2				
	elif direc == "gauche":				
		if col > 0: 
			if maze[row][col - 1]!=1:
				check_component(maze, row, col - 1, bag)
				maze[row][col]=0
				maze[row][col - 1] = 2
	elif direc == "droite":
		if col < 14:	
			if maze[row][col + 1]!=1:	
				check_component(maze, row, col + 1, bag)
				maze[row][col]=0
				maze[row][col + 1] = 2
					
				


def check_component(maze, row, col, bag):
	tile = maze[row][col]
	if tile in (4, 5, 6):
		bag.append(tile)
		print(bag)
			

	
def check_victory(maze, guardian_pos, bag, window, text_lose, text_win, text_esc):
	if find_tile(maze, 2) == guardian_pos:
		if len(bag) == 3:			
			#print("win")
			window.fill((0, 0, 0))
			window.blit(text_win, (360, 300))
			window.blit(text_esc, (195, 600))
			return "win"
		else:
			#print("lose")
			window.fill((0, 0, 0))
			window.blit(text_lose, (360, 300))
			window.blit(text_esc, (195, 600))
			return "lose"	
	return "run"	


def draw_bag(maze, images, window, bag): 
	if 4 in bag:
		window.blit(images["tube_image"], (730, 141))
	if 5 in bag:
		window.blit(images["needle_image"], (730, 188))
	if 6 in bag:	
		window.blit(images["ether_image"], (730, 235))



#############################################################################################
def main():
	while True:
		pygame.init()
		pygame.display.set_caption("MacGyver")
		resolution = (799, 705)
		window = pygame.display.set_mode(resolution, pygame.RESIZABLE) #ouverture fenêtre #, pygame.RESIZABLE
		black = (0, 0, 0)
		blank = (255, 255, 255)
		herculanum1_font = pygame.font.SysFont("herculanum", 35)
		herculanum2_font = pygame.font.SysFont("herculanum", 15)
		bag = [] 
		state = "run"
		running = True
		text_bag = herculanum1_font.render("bag", True, blank)
		text_fleche = herculanum1_font.render("☟", True, blank)	
		text_win = herculanum1_font.render("WIN !", True, blank)
		text_lose = herculanum1_font.render("LOSE !", True, blank)
		text_esc = herculanum2_font.render("Press 'ESC' to quit,  any other key will restart the game.", True, blank)
		images = {
			"wall_image" : pygame.image.load("wall.png").convert_alpha(), 
			"tube_image" : pygame.image.load("tube.png").convert_alpha(),
			"seringue_image" : pygame.image.load("seringue.png").convert_alpha(),
			"needle_image" : pygame.image.load("needle.png").convert_alpha(),
			"guardian_image" : pygame.image.load("guardian.png").convert_alpha(),
			"ether_image" : pygame.image.load("ether.png").convert_alpha(),
			"mac_image" : pygame.image.load("mac.png").convert_alpha()
		}
		maze = load_maze()
		randomize_components(maze)
		guardian_pos = find_tile(maze, 3)
		mac_pos = find_tile(maze, 2)
		pygame.key.set_repeat(100, 200)

		while running:

			draw(maze, images, window, text_bag, text_fleche)
			draw_bag(maze, images, window, bag)	

			
			for event in pygame.event.get(): #On parcours la liste de tous les événements reçus
				if event.type == pygame.QUIT: #Si un de ces événements est de type QUIT  
					return pygame.quit() #On arrête la boucle
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						return pygame.quit()	
				if state == "run":
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_UP:
							direction(maze, "haut", bag)						
						elif event.key == pygame.K_DOWN:
							direction(maze, "bas", bag)					
						elif event.key == pygame.K_LEFT:
							direction(maze, "gauche", bag)
						elif event.key == pygame.K_RIGHT:
							direction(maze, "droite", bag)
				else:
					if event.type == pygame.KEYDOWN:
						running = False			
			state = check_victory(maze, guardian_pos, bag, window, text_lose, text_win, text_esc)	

			pygame.display.flip() #rafraîchissement de l'affichage

if __name__ == '__main__':
	main()
