import random
import pickle
import os

class Agent:
	def __init__(self):
		self.q_table = {}

		self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]
		self.lr = 0.2  # Initial learning rate
		self.min_lr = 0.05 # Minimum learning rate
		self.lr_decay = 0.9998 # Decay per session - slower
		self.discount_factor = 0.9  # Discount factor for future rewards
		self.explo_rate = 1.0 
		self.explo_decay = 0.9995  # Decay per session - slower
		self.min_explo = 0.05  # Keep more exploration

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
		
	def learn(self, state, action, reward, next_state, done):
		# Bellman Formula
		current_q = self.get_q_value(state, action) #get current score

		# Find the maximum Q-value for the next state
		if done:
			target = reward
		else:
			max_future_q = max(self.get_q_value(next_state, next_action) 
							for next_action in self.actions)
			target = reward + (self.discount_factor * max_future_q)

		# new Q = old Q + Alpha * (target - old Q)
		new_q = current_q + self.lr * (target - current_q)
		self.q_table[(state, action)] = new_q

	def update_exploration(self):
		if self.explo_rate > self.min_explo:
				self.explo_rate *= self.explo_decay
		if self.lr > self.min_lr:
			self.lr *= self.lr_decay


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