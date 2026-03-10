import pygame
import random
import time
import argparse
import sys
import pickle
from snake import Snake
from board import Board
from agent import Agent
from config import *


def parse_arguments():
	parser = argparse.ArgumentParser(description="Learn2Slither - Snake AI")
		
	parser.add_argument("-sessions", type=int, default=100, help="Number of training sessions")
	parser.add_argument("-visual", type=str, choices=["on", "off"], default="on", help="visual (on/off)")
	parser.add_argument("-load", type=str, help="path to the model to load(ex: models/100sess.txt)")
	parser.add_argument("-save", type=str, help="path to the save directory (ex: models/test.txt)")
	parser.add_argument("-size", type=int, default=10, help="board size (default 10)")
	parser.add_argument("-dontlearn", action="store_true", help="no learning")
	parser.add_argument("--step-by-step", action="store_true", help="wait for an input between each step")
	parser.add_argument("-max-steps", type=int, default=700, help="max steps per session to avoid infinite loops")
	parser.add_argument("-stat", action="store_true", help="display statistics at the end (best length and average)")
	parser.add_argument("-debug", action="store_true", help="enable debug mode with cli agent state display")
	return parser.parse_args()

def main():
	args = parse_arguments()
		
	agent = Agent()
	board = Board(width=args.size, height=args.size)
		
	if args.load:
		agent.load_model(args.load)

		
	if args.dontlearn:
		agent.explo_rate = 0

	visual_mode = (args.visual == "on")
		
	if visual_mode:
		window = board.init_board()
	else:
		pass

	print(f"launching {args.sessions} sessions...")

	history = {
		'rewards': [],
		'lengths': [],
		'steps': [],
		'epsilons': []
	}

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
			board.get_state()
			if args.debug:
				print(board.state)
		
			board.calculate_pos()
			if not args.dontlearn:
				agent.learn(state, action, reward, next_state, done)
			
			state = next_state
			total_reward += reward
			steps += 1
			
			if visual_mode:
				window.fill(BACKGROUND)
				
				for x in range(board.width):
					for y in range(board.height):
						rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) 
						pygame.draw.rect(window, GRID_COLOR, rect, 1)

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
					time.sleep(1.0 / GAME_SPEED) 

		if not args.dontlearn:
			agent.update_exploration()
		
		history['rewards'].append(total_reward)
		history['lengths'].append(len(board.snake.body))
		history['steps'].append(steps)
		history['epsilons'].append(agent.explo_rate)
		
		print(f"Session {session}/{args.sessions} - Steps: {steps} - Reward: {total_reward} - Epsilon: {agent.explo_rate:.2f}, length : {len(board.snake.body)}")
	
	if args.stat:
		best_length = max(history['lengths'])
		avg_length = sum(history['lengths']) / len(history['lengths']) if history['lengths'] else 0
		print("\n" + "="*50)
		print("STATISTICS")
		print("="*50)
		print(f"Best length: {best_length}")
		print(f"Average length: {avg_length:.2f}")
		print("="*50 + "\n")
	
	if args.save:
		agent.save_model(args.save)

	if visual_mode:
		pygame.quit()

if __name__ == "__main__":
	main()