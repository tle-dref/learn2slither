import random
import pickle
import os

class Agent:
	def __init__(self):
		self.q_table = {}

		self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]
		self.lr = 0.1 # (Alpha)
		self.discount_factor = 0.9 # (Gamma) importance of future
		self.explo_rate = 1.0 # (Epsilon) luck based move probability at start
		self.explo_decay = 0.995 # factor by which we decay the luck based move
		self.min_explo = 0.01 # keep a percent of luck based move

	def get_q_value(self, state, action):
		return self.q_table.get((state, action), 0.0) # if situatation is unknown, ret 0
	
	def choose_action(self, state):
		# Epsilon Greedy
		# if rand is less that our rate we choose a luck based move
		if random.random() < self.explo_rate:
			return random.choice(self.actions)
		# else we think
		else :
			best_score = -float('inf')
			best_action = random.choice(self.actions)

			for action in self.actions:
				score = self.get_q_value(state, action)
				if score > best_score:
					best_score = score
					best_action = action
			return best_action
		
	def learn(self, state, action, reward, next_state):
		# Bellman Formula
		current_q = self.get_q_value(state, action) #get current score

		# Find the maximum Q-value for the next state
		max_future_q = max(self.get_q_value(next_state, next_action) 
						   for next_action in self.actions)
		
		# new Q = old Q + Alpha * (reward + Gamma * future - old Q)
		new_q = current_q + self.lr * (reward + (self.discount_factor * max_future_q) - current_q)
		self.q_table[(state, action)] = new_q

	def update_exploration(self):
		if self.explo_rate > self.min_explo:
				self.explo_rate *= self.explo_decay


	def save_model(self, filepath):
		with open(filepath, 'wb') as f:
			pickle.dump(self.q_table, f)
		print(f"model saved in : {filepath}")

	def load_model(self, filepath):
		if os.path.exists(filepath):
			with open(filepath, 'rb') as f:
				self.q_table = pickle.load(f)
			print(f"model loaded from : {filepath}")
		else:
			print("can't find the model.")