import pygame
import random
import sys
from snake import Snake

CELL_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 10
BACKGROUND = (54, 1, 63)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Board:
	def __init__(self, width=GRID_WIDTH, height=GRID_HEIGHT):
		self.width = width
		self.height = height
		self.pixel_w = self.width * CELL_SIZE
		self.pixel_h = self.height * CELL_SIZE
		self.red_pos = []
		self.green_pos = []
		self.snake = Snake(width, height)
		self.state = []

	def reset(self):
		"""clean new board"""
		self.red_pos = []
		self.green_pos = []
		self.snake = Snake(self.width, self.height)
		self.calculate_pos()
	
	def get_state(self):
		lines = []
		head_x, head_y = self.snake.body[-1]
		for y in range(self.height):
			if y == head_y:
				line = "W" 
				for x in range(self.width):
					if (x, y) == self.snake.body[-1]:
						char = "H"
					elif (x, y) in self.snake.body[:-1]:
						char = "S"
					elif (x, y) in self.green_pos:
						char = "G"
					elif (x, y) in self.red_pos:
						char = "R"
					else:
						char = "0"
					line += char
				line += "W" 
			else:
				line = " " * (head_x + 1)
				pos = (head_x, y)
				if pos in self.snake.body[:-1]:
					char = "S"
				elif pos in self.green_pos:
					char = "G"
				elif pos in self.red_pos:
					char = "R"
				else:
					char = "0"
				line += char
			lines.append(line)
		lines.insert(0, " " * (head_x + 1) + "W")
		lines.append(" " * (head_x + 1) + "W")
		self.state = "\n".join(lines)

	def get_agent_state(self):
		head_x, head_y = self.snake.body[-1]
		def is_unsafe(x, y):
			if not (0 <= x < self.width and 0 <= y < self.height):
				return 1 
			if (x, y) in self.snake.body[:-1]:
				return 1 
			return 0
		up = is_unsafe(head_x, head_y - 1)
		down = is_unsafe(head_x, head_y + 1)
		left = is_unsafe(head_x - 1, head_y)
		right = is_unsafe(head_x + 1, head_y)

		green_apple_up = 0
		green_apple_down = 0
		green_apple_left = 0
		green_apple_right = 0
		for (ax, ay) in self.green_pos:
			if ax == head_x: 
				if ay < head_y: green_apple_up = 1
				if ay > head_y: green_apple_down = 1
			if ay == head_y:
				if ax < head_x: green_apple_left = 1
				if ax > head_x: green_apple_right = 1
		red_apple_up = 0
		red_apple_down = 0
		red_apple_left = 0
		red_apple_right = 0
		for (ax, ay) in self.red_pos:
			if ax == head_x: 
				if ay < head_y: red_apple_up = 1
				if ay > head_y: red_apple_down = 1
			if ay == head_y:
				if ax < head_x: red_apple_left = 1
				if ax > head_x: red_apple_right = 1
		state = (up, down, left, right, green_apple_up, green_apple_down,
		   			green_apple_left, green_apple_right, red_apple_up, red_apple_down,
					red_apple_left, red_apple_right)
		return state

	def random_pos(self):
		x = random.randint(0, self.width - 1)
		y = random.randint(0, self.height - 1)
		return (x, y)

	def calculate_pos(self):
		while len(self.green_pos) < 2:
			self.green_pos.append(self.random_pos())
		if len(self.red_pos) < 1:
			self.red_pos.append(self.random_pos())

	def place_apple(self, window):
		red_apple = self.red_pos[0]
		red_apple_x, red_apple_y = red_apple
		centre_x = (red_apple_x * CELL_SIZE) + (CELL_SIZE // 2)
		centre_y = (red_apple_y * CELL_SIZE) + (CELL_SIZE // 2)
		pygame.draw.circle(window, RED, (centre_x, centre_y), CELL_SIZE // 3)
		for apple in self.green_pos:
			green_apple_x, green_apple_y = apple
			centre_x = (green_apple_x * CELL_SIZE) + (CELL_SIZE // 2)
			centre_y = (green_apple_y * CELL_SIZE) + (CELL_SIZE // 2)
			pygame.draw.circle(window, GREEN, (centre_x, centre_y), CELL_SIZE // 3)

	def draw_snake(self, window):
		for pos in self.snake.body:
			x, y = pos
			rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(window, BLUE, rect)
	
	def init_board(self):
		pygame.init()
		window = pygame.display.set_mode((self.pixel_h, self.pixel_w))
		self.calculate_pos()
		return window
	def update_direction(self, action):
		if action == "UP":
			self.snake.direction = (0, -1)
		elif action == "DOWN":
			self.snake.direction = (0, 1)
		elif action == "LEFT":
			self.snake.direction = (-1, 0)
		elif action == "RIGHT":
			self.snake.direction = (1, 0)

	def step(self, action):
		self.update_direction(action)
		result = self.snake.move(self.green_pos, self.red_pos)
		reward = 0
		done = False
		if result == 1 : reward = -3  # Small penalty to encourage finding food quickly
		elif result == 2 : reward = 100  # Green apple (good)
		elif result == 3 : reward = -20  # Red apple (bad)
		elif result == 4 or result == 5 or result == 6:
			reward = -100  # Death penalty
			done = True

		next_state = self.get_agent_state()
		return next_state, reward, done

# def main():
# 	board = Board()
# 	window = board.init_board()
# 	clock = pygame.time.Clock()
# 	running = True
# 	while running:
# 		# Handle events separately
# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				running = False
		
# 		#runs once per frame, outside event loop
# 		window.fill(BACKGROUND) 
# 		for x in range(board.width):
# 			for y in range(board.height):
# 				rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
# 				pygame.draw.rect(window, WHITE, rect, 1)
# 		board.calculate_pos()
# 		board.place_apple(window)
# 		board.draw_snake(window)
# 		board.get_agent_state()
# 		print(10*"-" + "GAME STATE" + 10*"-")
# 		print(board.state)
# 		print(30*"-")
		
# 		pygame.display.flip()
		
# 		# Control game speed 
# 		clock.tick(10)

# 	pygame.quit()
# 	sys.exit()

# if __name__ == "__main__":
# 	main()