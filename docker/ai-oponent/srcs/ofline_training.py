import os
import torch
import numpy as np
from replay_buffer import ReplayBuffer
from agent import Agent  # Ensure this imports your modified Agent class
from config import BUFFER_SIZE

def main():
    batch_size = 512
    num_epochs = 1500  # Set the number of epochs you want to train for

    # Initialize the replay buffer and agent
    replay_buffer = ReplayBuffer(buffer_size=BUFFER_SIZE)
    agent = Agent(side="left", replay_buffer=replay_buffer)

    # Ensure the replay buffer is loaded
    if replay_buffer.size() < batch_size:
        print("Replay buffer is too small to start training. Please ensure it is loaded correctly.")
        return

    print(f"Starting offline training for {num_epochs} epochs...")
    for epoch in range(num_epochs):
        loss_per_epoch = 0
        for i in range(50):
          agent.train_step(batch_size)
          loss_per_epoch += agent.loss_per_step
        agent.update_target_model()
        loss_per_epoch /= 50
        
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss_per_epoch:.4f}")

    # Save the trained model
    agent.save_model()
    print("Training completed and model saved.")

if __name__ == "__main__":
    main()
