import pygame
import random
import time
import argparse
import sys
from snake import Snake
from board import Board
from agent import Agent


CELL_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 10
BACKGROUND = (54, 1, 63)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


def parse_arguments():
	parser = argparse.ArgumentParser(description="Learn2Slither - Snake AI")
		
	parser.add_argument("-sessions", type=int, default=100, help="Number of training sessions")
	parser.add_argument("-visual", type=str, choices=["on", "off"], default="on", help="visual (on/off)")
	parser.add_argument("-load", type=str, help="path to the model to load(ex: models/100sess.txt)")
	parser.add_argument("-save", type=str, help="path to the save directory (ex: models/test.txt)")
	parser.add_argument("-dontlearn", action="store_true", help="no learning")
	parser.add_argument("--step-by-step", action="store_true", help="wait for an input between each step")
	parser.add_argument("-max-steps", type=int, default=1000, help="max steps per session to avoid infinite loops")
		
	return parser.parse_args()

def main():
	args = parse_arguments()
		
	agent = Agent()
	board = Board()
		
	if args.load:
		agent.load_model(args.load)

		
	if args.dontlearn:
		agent.explo_rate = 0 # no luck based move at all

	visual_mode = (args.visual == "on")
		
	if visual_mode:
		window = board.init_board()
	else:
		pass

	print(f"launching {args.sessions} sessions...")

	for session in range(1, args.sessions + 1):
		board.reset() 

		state = board.get_agent_state()
		done = False
		total_reward = 0
		steps = 0
		
		while not done and steps < args.max_steps:
			if visual_mode:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()

			action = agent.choose_action(state)
			next_state, reward, done = board.step(action)
			
			if not args.dontlearn:
				agent.learn(state, action, reward, next_state)
			
			state = next_state
			total_reward += reward
			steps += 1
			
			if visual_mode:
				window.fill((54, 1, 63))
				
				for x in range(board.width):
					for y in range(board.height):
						rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) 
						pygame.draw.rect(window, (255, 255, 255), rect, 1)

				board.calculate_pos()
				board.place_apple(window)
				board.draw_snake(window)
				pygame.display.flip()
				
				if args.step_by_step:
					waiting = True
					while waiting:
						for event in pygame.event.get():
							if event.type == pygame.KEYDOWN: waiting = False
							if event.type == pygame.QUIT: sys.exit()
				else:
					time.sleep(0.05) 

		if not args.dontlearn:
			agent.update_exploration()
		
		print(f"Session {session}/{args.sessions} - Steps: {steps} - Reward: {total_reward} - Epsilon: {agent.explo_rate:.2f}, length : {len(board.snake.body)}")

	if args.save:
		agent.save_model(args.save)

	if visual_mode:
		pygame.quit()

if __name__ == "__main__":
	main()