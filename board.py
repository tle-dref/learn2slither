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


def main():
	board = Board()
	window = board.init_board()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			window.fill(BACKGROUND) 
			for x in range(board.width):
				for y in range(board.height):
					rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
					pygame.draw.rect(window, WHITE, rect, 1)
			board.place_apple(window)
			board.draw_snake(window)
			board.calculate_pos()
			pygame.display.flip()

	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()