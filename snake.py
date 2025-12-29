import random

GRID_WIDTH = 10
GRID_HEIGHT = 10

class Snake:
	def __init__(self, board_width, board_height):
		self.board_width = board_width
		self.board_height = board_height
		self.body = []
		self.direction = (0, 1) # (0, 1) up, (0, -1) bottom, (-1, 0) left, (1, 0) right 
		self.init_snake()

	def init_snake(self):
		while len(self.body) < 3:
			self.body = []

			head_x = random.randint(0, self.board_width - 1)
			head_y = random.randint(0, self.board_height - 1)
			self.body.append((head_x, head_y))

			dir_x, dir_y = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

			valid = True
			for i in range(1, 3):
				new_x = head_x + (dir_x * i)
				new_y = head_y + (dir_y * i)

				if 0 <= new_x < self.board_width and 0 <= new_y < self.board_height:
					self.body.append((new_x, new_y))
				else:
					valid = False
					break # try again this pos can't be valid

	def test_rand_move(self):
		self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
		self.move(green_apple=[], red_apple=[])

	def move(self, green_apple, red_apple):
		"""This function apply the movement of the snake and return values
		depending of what happende : 1 : alive, 2 : green apple has been eaten, 
		3 : red apple has been eaten, 4 dead because of wall, 5 dead because
		len reached 0, 6 : hit itself"""
		current_head = self.body[-1]
		head_x, head_y = current_head
		
		dir_x, dir_y = self.direction

		new_head_x = head_x + dir_x
		new_head_y = head_y + dir_y
		#check walls
		if 0 <= new_head_x < self.board_width and 0 <= new_head_y < self.board_height:
			#check collision with body
			if (new_head_x, new_head_y) in self.body[:-1]:
				return 6
			self.body.append((new_head_x, new_head_y))
			if (new_head_x, new_head_y) in green_apple:
				green_apple.remove((new_head_x, new_head_y))
				return 2
			else:
				self.body.pop(0)
			if (new_head_x,new_head_y) in red_apple:
				red_apple.remove((new_head_x, new_head_y))
				if len(self.body) > 0:
					self.body.pop(0) 
					if len(self.body) == 0:
						return 5
					return 3
			return 1
		else:
			return 4
