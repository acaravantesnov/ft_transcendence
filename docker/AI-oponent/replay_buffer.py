import pickle
from collections import deque
import random
import numpy as np
import os

class ReplayBuffer:
    def __init__(self, buffer_size, buffer_path="replay_buffer.pkl"):
        self.buffer = deque(maxlen=buffer_size)
        self.prev_state = None
        self.prev_action = None
        self.buffer_path = buffer_path
        self.load_buffer()

    def add(self, state, action):
        if self.prev_state is None or self.prev_action is None:
            self.prev_state = state
            self.prev_action = action
            return
        prev_state = self.prev_state
        prev_action = self.prev_action
        reward = self.calculate_reward(prev_state, state, prev_action)
        self.buffer.append((prev_state, prev_action, reward, state, action))
        self.prev_state = state
        self.prev_action = action
        print(" [ReplayBuffer] Buffer size: ", len(self.buffer))

        # # Mirror state
        # mirrored_state = self.mirror_state(state)
        # mirrored_prev_state = self.mirror_state(prev_state)
        # mirrored_prev_action = state['right_paddle']['speed']
        # mirrored_reward = self.calculate_reward(mirrored_prev_state, mirrored_state, mirrored_prev_action)
        # self.buffer.append((mirrored_prev_state, mirrored_prev_action, mirrored_reward, mirrored_state, mirrored_prev_action))
        # print(" [ReplayBuffer] Buffer size: ", len(self.buffer))
        # # print(" [ReplayBuffer] Added to buffer: ", mirrored_prev_state, mirrored_prev_action, mirrored_reward, mirrored_state, mirrored_prev_action)
    
    def size(self):
        return len(self.buffer)

    def mirror_state(self, state):
        mirrored_state = {
            'ball_position': {
                'x': 800 - state['ball_position']['x'],
                'y': state['ball_position']['y']
            },
            'ball_speed': {
                'x': -state['ball_speed']['x'],
                'y': state['ball_speed']['y']
            },
            'left_paddle': {
                'x': 30,
                'y': state['right_paddle']['y'],
                'speed': state['right_paddle']['speed']
            },
            'right_paddle': {
                'x': 760,
                'y': state['left_paddle']['y'],
                'speed': state['left_paddle']['speed']
            },
            'scores': {
                'left': state['scores']['right'],
                'right': state['scores']['left']
            },
            'game_over': {
                'ended': state['game_over']['ended'],
                'winner': state['game_over']['winner']
            }
        }
        return mirrored_state

    def calculate_reward(self, prev_state, state, prev_action):
        reward = 0
        # if state['scores']['left'] > prev_state['scores']['left']:
        #     reward += 15
        if state['scores']['right'] > prev_state['scores']['right']:
            reward -= 30
        if reward == 0: 
            if state['ball_speed']['x'] > 0 and prev_state['ball_speed']['x'] < 0:
                reward += 10
                # distance_ball_to_paddle = abs(state['left_paddle']['y'] + 75 - state['ball_position']['y']) / 75.0
                # reward += 10 * abs(1 - distance_ball_to_paddle) ** 0.5
                # if abs(state['ball_speed']['y']) > abs(prev_state['ball_speed']['y']):
                #     reward += 5
        if prev_action != 0:
            reward -= 0.2
        return reward

    @staticmethod
    def state_dict_to_vector(state):
        return [state['ball_position']['x'] / 800.0, state['ball_position']['y'] / 600.0, state['ball_speed']['x'], state['ball_speed']['y'], state['left_paddle']['y'] / 600.0]

    def get_batch(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, _ = zip(*batch)
        states_vector = [ReplayBuffer.state_dict_to_vector(state) for state in states]
        next_states_vector = [ReplayBuffer.state_dict_to_vector(state) for state in next_states]
        actions_vector = [[1, 0, 0] if action < 0 else [0, 1, 0] if action == 0 else [0, 0, 1] for action in actions]
        return np.array(states_vector), np.array(actions_vector), np.array(rewards), np.array(next_states_vector)

    def save_buffer(self):
        with open(self.buffer_path, "wb") as f:
            pickle.dump(self.buffer, f)
        print(" [ReplayBuffer] Buffer saved to ", self.buffer_path)

    def load_buffer(self):
        if os.path.exists(self.buffer_path):
            with open(self.buffer_path, "rb") as f:
                buffer_copy = pickle.load(f)
            print(" [ReplayBuffer] Buffer loaded from ", self.buffer_path)
            print(" [ReplayBuffer] Recalculating rewards...")
            for prev_state, prev_action, _, state, action in buffer_copy:
                reward = self.calculate_reward(prev_state, state, prev_action)
                self.buffer.append((prev_state, prev_action, reward, state, action))
        else:
            print(" [ReplayBuffer] No buffer found at ", self.buffer_path)
