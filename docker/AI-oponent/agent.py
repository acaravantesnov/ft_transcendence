import random
import json
from replay_buffer import ReplayBuffer
import numpy as np
import pytorch

class Agent:
    def __init__(self, side, replay_buffer):
        # self.side = side
        self.replay_buffer = replay_buffer
        # sefl.discount_factor = 0.95
        # self.epsilon = 0.1
        #
        # self.model = ...

    def Q_a(self, state, action):
        return self.model(np.array(ReplayBuffer.state_dict_to_vector(state)).reshape(1, -1), np.array([action]).reshape(1, -1))
    
    def Q_max(self, state):
        rewards = np.array([self.Q_a(state, action) for action in [[1, 0, 0], [0, 1, 0], [0, 0, 1]]])
        return np.argmax(rewards), np.max(rewards)
    
    def decide_action(self, state):
        # # With probability epsilon, choose a random action
        # if random.random() < self.epsilon:
        #     action =  random.choice([-5, 0, 5])
        # else:
        #   best_action, best_Q = self.Q_max(state)
        #   action = [-5, 0, 5][best_action]
        # self.replay_buffer.add(state, action)
        # for i in range(5):
        #   self.train_step(64)
        # return action

        # Randomly choose an action: -5 (up), 5 (down), or 0 (stop)
        action = random.choice([-5, 0, 5])
        self.replay_buffer.add(state, action)
        return action

    def train_step(self, batch_size):
        # Sample a batch from the replay buffer
        states, actions, rewards, next_states = self.replay_buffer.sample(batch_size)
        # states.shape = (batch_size, 7)
        # actions.shape = (batch_size, 3)
        # rewards.shape = (batch_size, 1)
        # Update the model
        # ...
        pass

