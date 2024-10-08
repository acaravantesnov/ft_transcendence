import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from .replay_buffer import ReplayBuffer
import os

#model2
# class DQNet(nn.Module):
#     def __init__(self, input_dim, output_dim):
#         super(DQNet, self).__init__()

#         self.fc1 = nn.Linear(input_dim, 128)
#         self.fc2 = nn.Linear(128, 32) #64, 16
#         self.fc3 = nn.Linear(32, output_dim)

#         self.bn0 = nn.BatchNorm1d(input_dim)
#         # self.bn1 = nn.BatchNorm1d(64)
    
#     def forward(self, x):
#         x = self.bn0(x)
#         x = torch.nn.functional.tanh(self.fc1(x))
#         # x = self.bn1(x)
#         x = torch.nn.functional.tanh(self.fc2(x))
#         return self.fc3(x)

#model3(2) : 50, 26
#model3(3) : 50, 21
#model3(7) : 60, 30

class DQNet(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQNet, self).__init__()

        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 32)
        self.fc3 = nn.Linear(32, 32)
        self.fc4 = nn.Linear(32, output_dim)

        # self.bn0 = nn.BatchNorm1d(input_dim)
        self.bn1 = nn.BatchNorm1d(128)
        self.bn2 = nn.BatchNorm1d(32)
        self.bn3 = nn.BatchNorm1d(32)

        #self.out_multiplier = nn.Parameter(torch.tensor(30.0))
    
    def forward(self, x):
        x = self.fc1(x)
        # x = self.bn1(x)
        x = torch.nn.functional.leaky_relu(x)
        x = self.fc2(x)
        # x = self.bn2(x)
        # x = torch.nn.functional.leaky_relu(x)
        # x = self.fc3(x)
        # x = self.bn3(x)
        x = torch.nn.functional.leaky_relu(x)
        x = self.fc4(x)
        # x = torch.nn.functional.tanh(x)
        # x = x * 20.0
        return x

class Agent:
    def __init__(self, side, replay_buffer, input_dim=5, output_dim=3, discount_factor=0.85, epsilon=0.0, lr=0.0002, batch_size=256, model_path="./TranscendenceApp/ai_oponent/model.pt", tau=0.4, tau_decay=0.995, tau_min=0.1):
        self.side = side
        self.replay_buffer = replay_buffer
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.batch_size = batch_size
        self.action_space = [-3, 0, 3]
        self.tau = tau
        self.tau_decay = tau_decay
        self.tau_min = tau_min

        self.model = DQNet(input_dim, output_dim)
        self.target_model = DQNet(input_dim, output_dim)
        
        if os.path.exists(model_path):
            print(" [Agent] Loading model from: ", model_path)
            self.model.load_state_dict(torch.load(model_path))
        else:
            print(" [Agent] No model found at: ", model_path)

        self.target_model.load_state_dict(self.model.state_dict())
        self.target_model.eval()
        self.model.eval()

        self.optimizer = optim.Adam(self.model.parameters(), lr=lr, weight_decay=0.00003)
        self.loss_fn = nn.MSELoss()

        self.loss_per_step = 0

    def update_target_model(self):
        for target_param, param in zip(self.target_model.parameters(), self.model.parameters()):
            target_param.data.copy_(self.tau * param.data + (1.0 - self.tau) * target_param.data)
        self.tau = max(self.tau * self.tau_decay, self.tau_min)

    def Q_a(self, state, action):
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        q_values = self.model(state_tensor)
        return q_values[0, action]

    def Q_max(self, state):
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        self.model.eval()
        q_values = self.model(state_tensor)
        max_action = torch.argmax(q_values).item()
        max_q_value = torch.max(q_values).item()
        print(" [Agent] Q_values: ", q_values)
        print(" [Agent] Q_max: ", max_action, max_q_value)
        return max_action, max_q_value

    def decide_action(self, state):
        if random.random() < self.epsilon or self.replay_buffer.size() < self.batch_size:
            action = random.choice(self.action_space)
        else:
            best_action, _ = self.Q_max(ReplayBuffer.state_dict_to_vector(state))
            action = self.action_space[best_action]
        self.replay_buffer.add(state, action)

        # if self.replay_buffer.size() >= self.batch_size:
        #   print(" [Agent] Training step, with buffer size: ", self.replay_buffer.size())
        #   for i in range(50):
        #     self.train_step(self.batch_size)
        #   self.update_target_model()
        return action

    def train_step(self, batch_size):
        if self.replay_buffer.size() < batch_size:
            return

        self.model.train()
        states, actions, rewards, next_states = self.replay_buffer.get_batch(batch_size)
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int64)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)

        # current_q_values = torch.sum(self.model(states) * actions, dim=1)
        # next_q_values = self.target_model(next_states).max(1)[0].detach()
        # target_q_values = rewards + (self.discount_factor * next_q_values)


        # Double DQN: current Q-values and next Q-values using both networks
        current_q_values = torch.sum(self.model(states) * actions, dim=1)
        next_state_actions = self.model(next_states).detach().max(1)[1].unsqueeze(1)
        # print(self.target_model(next_states).shape)
        # print(next_state_actions[0:3])
        # print()
        next_q_values = self.target_model(next_states).gather(1, next_state_actions).squeeze(1)
        target_q_values = rewards + (self.discount_factor * next_q_values)

        loss = self.loss_fn(current_q_values, target_q_values)
        self.loss_per_step = loss.item()
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def save_model(self):
        torch.save(self.model.state_dict(), model_path)
        print(" [Agent] Model saved")
