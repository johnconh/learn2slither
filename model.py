import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import numpy as np


class QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        """
        Initializes the Q-Network architecture.

        Args:
            input_size (int): Size of the input layer (state representation)
            hidden_size (int): Number of neurons in the hidden layer
            output_size (int): Size of the output layer (number of actions)

        Creates a simple feedforward neural network with one hidden layer.
        """
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """
        Defines the forward pass of the neural network.

        Args:
            x: Input tensor containing the state representation

        Returns:
            Q-values for each possible action (3 actions in this case)

        Architecture:
        Input -> Linear Layer -> ReLU Activation -> Linear Layer -> Output
        """
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def save(self, file_name):
        """
        Saves the trained model's state dictionary to a file.

        Args:
            file_name (str): Path where the model should be saved

        Creates the directory if it doesn't exist and
        saves all model parameters
        (weights and biases) that can be later loaded to restore the model.
        """
        model_folder = os.path.dirname(file_name)
        if model_folder:
            if not os.path.exists(model_folder):
                os.makedirs(model_folder)
        torch.save(self.state_dict(), file_name)

    def load(self, file_name):
        """
        Loads a previously saved model's state dictionary.

        Args:
            file_name (str): Path to the saved model file

        Restores all model parameters (weights and biases) from the saved file,
        allowing the model to continue from a previously trained state.
        """
        self.load_state_dict(torch.load(file_name))


class QTrainer:
    def __init__(self, model, lr, gamma):
        """
        Initializes the Q-learning trainer.

        Args:
            model: The Q-network to be trained
            lr (float): Learning rate for the optimizer
            gamma (float): Discount factor for future rewards

        Sets up the optimizer (Adam) and loss function (MSE) for training
        the Q-network using the Q-learning algorithm.
        """
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        """
        Trains the Q-network using the Q-learning algorithm.

        Args:
            state: Current state of the environment
            action: Action taken in the current state
            reward: Reward received after taking the action
            next_state: State reached after taking the action
            done: Boolean indicating if the episode has ended

        The function implements the Bellman equation:
        Q(s,a) = reward + gamma * max(Q(s',a'))
        where s' is the next state and a' are possible actions in s'
        """
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(np.array(action), dtype=torch.float)
        reward = torch.tensor(np.array(reward), dtype=torch.float)
        done = torch.tensor(done, dtype=torch.bool)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new += self.gamma * torch.max(self.model(next_state[idx]))
            target[idx][torch.argmax(action).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()
