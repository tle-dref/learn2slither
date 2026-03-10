import pygame
import random
import sys
from snake import Snake
from config import *


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
		"""calulate the state from the head perspecive but stop at any 'obstacle'"""
		head_x, head_y = self.snake.body[-1]
		def look(dx, dy):
			wall, body, green_apple, red_apple = 0, 0, 0, 0
			curr_x, curr_y = head_x + dx, head_y + dy
			while 0 <= curr_x < self.width and 0 <= curr_y < self.height:
				if (curr_x, curr_y) in self.snake.body:
					body = 1
					break 
				if (curr_x, curr_y) in self.green_pos:
					green_apple = 1
					break 
				if (curr_x, curr_y) in self.red_pos:
					red_apple = 1
					break 
				curr_x += dx
				curr_y += dy
			else:
				wall = 1
			return wall, body, green_apple, red_apple

		# UP (0, -1)
		w_u, b_u, g_u, r_u = look(0, -1)
		# DOWN (0, 1)
		w_d, b_d, g_d, r_d = look(0, 1)
		# LEFT (-1, 0)
		w_l, b_l, g_l, r_l = look(-1, 0)
		# RIGHT (1, 0)
		w_r, b_r, g_r, r_r = look(1, 0)
		
		def is_unsafe(x, y):
			if not (0 <= x < self.width and 0 <= y < self.height): return 1
			if (x, y) in self.snake.body[:-1]: return 1
			return 0
		
		# Direction actuelle du serpent
		dir_up = 1 if self.snake.direction == (0, -1) else 0
		dir_down = 1 if self.snake.direction == (0, 1) else 0
		dir_left = 1 if self.snake.direction == (-1, 0) else 0
		dir_right = 1 if self.snake.direction == (1, 0) else 0
		
		state = (
			is_unsafe(head_x, head_y - 1), 
			is_unsafe(head_x, head_y + 1),
			is_unsafe(head_x - 1, head_y),
			is_unsafe(head_x + 1, head_y),
			dir_up, dir_down, dir_left, dir_right,
			g_u, g_d, g_l, g_r,
			r_u, r_d, r_l, r_r,
			# w_u, w_d, w_l , w_r, b_u, b_d, b_l, b_r #TEST
		)
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
		for apple in self.red_pos:
			apple_x, apple_y = apple
			center_x = (apple_x * CELL_SIZE) + (CELL_SIZE // 2)
			center_y = (apple_y * CELL_SIZE) + (CELL_SIZE // 2)
			pygame.draw.circle(window, BAD_APPLE, (center_x, center_y), CELL_SIZE // 2.5)
			pygame.draw.circle(window, (255, 100, 180), (center_x, center_y), CELL_SIZE // 4)

		for apple in self.green_pos:
			apple_x, apple_y = apple
			center_x = (apple_x * CELL_SIZE) + (CELL_SIZE // 2)
			center_y = (apple_y * CELL_SIZE) + (CELL_SIZE // 2)
			pygame.draw.circle(window, GOOD_APPLE, (center_x, center_y), CELL_SIZE // 2.5)
			pygame.draw.circle(window, (200, 255, 200), (center_x, center_y), CELL_SIZE // 4)

	def draw_snake(self, window):
		for i, pos in enumerate(self.snake.body):
			x, y = pos
			rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
			
			inner_rect = rect.inflate(-4, -4)
			
			if i == len(self.snake.body) - 1: 
				pygame.draw.rect(window, WHITE, inner_rect, border_radius=5)
				pygame.draw.rect(window, SNAKE, inner_rect, 2, border_radius=5)
			else: 
				pygame.draw.rect(window, SNAKE, inner_rect, border_radius=2)
				center_rect = inner_rect.inflate(-20, -20)
				pygame.draw.rect(window, BACKGROUND, center_rect, border_radius=2)
	
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
		
		if result == 1 : 
			reward = 0  # No penalty for living
		elif result == 2 : reward = 100  # Green apple
		elif result == 3 : reward = -20  # Red apple
		elif result == 4 or result == 5 or result == 6:
			reward = -100  # Death penalty
			done = True

		if done or len(self.snake.body) == 0:
			return (1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), reward, True
		
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