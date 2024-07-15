from collections import deque
import random
import numpy as np

class ReplayBuffer:
    def __init__(self, buffer_size):
        self.buffer = deque(maxlen=buffer_size)
        self.prev_state = None
        self.prev_action = None

    def add (self, state, action):
        if self.prev_state is None or self.prev_action is None:
            self.prev_state = state
            self.prev_action = action
            return
        prev_state = self.prev_state
        prev_action = self.prev_action
        reward = self.calculate_reward(prev_state, state, prev_action)
        self.buffer.append((prev_state, prev_action, reward, state, action))
        with open("state.txt", "w") as f:
            f.write(f"{prev_state}, {prev_action}, {reward}")
        self.prev_state = state
        self.prev_action = action
        print(" [ReplayBuffer] Buffer size: ", len(self.buffer))
        #print(" [ReplayBuffer] Added to buffer: ", prev_state, prev_action, reward, state, action)
        # Save state to file

        # # Mirror state
        # mirrored_state = self.mirror_state(state)
        # mirrored_prev_state = self.mirror_state(prev_state)
        # mirrored_prev_action = state['right_paddle']['speed']
        # mirrored_reward = self.calculate_reward(mirrored_prev_state, mirrored_state, mirrored_prev_action)
        # self.buffer.append((mirrored_prev_state, mirrored_prev_action, mirrored_reward, mirrored_state, mirrored_prev_action))
        # print(" [ReplayBuffer] Buffer size: ", len(self.buffer))
        # # print(" [ReplayBuffer] Added to buffer: ", mirrored_prev_state, mirrored_prev_action, mirrored_reward, mirrored_state, mirrored_prev_action)
        # with open("state.txt", "a") as f:
        #     f.write(f"{mirrored_prev_state}, {mirrored_prev_action}, {mirrored_reward}")

    def size(self):
        return len(self.buffer)

    def mirror_state(self, state):
        # {'ball_position': {'x': 108, 'y': 540.9999999999999}, 'ball_speed': {'x': -2, 'y': -3.666666666666667}, 'left_paddle': {'x': 30, 'y': 0, 'speed': -5}, 'right_paddle': {'x': 760, 'y': 425, 'speed': 0}, 'scores': {'left': 1, 'right': 2}, 'game_over': {'ended': False, 'winner': None}} 
        # screen_size = {'width': 800, 'height': 600}
        # paddle_size = {'width': 10, 'height': 100}
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

        # Reward for scoring a point
        if state['scores']['left'] > prev_state['scores']['left']:
            reward += 15

        # Penalty for opponent scoring a point
        if state['scores']['right'] > prev_state['scores']['right']:
            reward -= 30

        # Reward for bouncing ball on own paddle
        if reward == 0: #Only if no one scored
          if state['ball_speed']['x'] > 0 and prev_state['ball_speed']['x'] < 0:
              reward += 3

        # A bit of penalty for moving paddle
        if prev_action != 0:
            reward -= 0.1

        return reward

    def state_dict_to_vector(state):
        return [state['ball_position']['x'] / 800.0, state['ball_position']['y'] / 600.0, state['ball_speed']['x'], state['ball_speed']['y'], state['left_paddle']['y'] / 600.0, state['right_paddle']['y'] / 600.0, state['right_paddle']['speed'] / 5.0]

    def get_batch(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, _ = zip(*batch)
        states_vector = []
        for state in states:
            states_vector.append(ReplayBuffer.state_dict_to_vector(state))
        next_states_vector = []
        for state in next_states:
            next_states_vector.append(ReplayBuffer.state_dict_to_vector(state))
        actions_vector = []
        for action in actions:
            if action == -5:
                actions_vector.append([1, 0, 0])
            elif action == 0:
                actions_vector.append([0, 1, 0])
            elif action == 5:
                actions_vector.append([0, 0, 1])
        return np.array(states_vector), np.array(actions_vector), np.array(rewards), np.array(next_states_vector)
