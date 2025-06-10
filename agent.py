import torch
import random
from collections import deque
from model import QNet, QTrainer


MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        """
        Initializes the reinforcement learning agent.

        Sets up the Q-network, memory buffer, and training parameters
        for the Deep Q-Learning algorithm.
        """
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = QNet(19, 512, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def remember(self, state, action, reward, next_state, done):
        """
        Stores an experience tuple in the replay memory buffer.

        Args:
            state: Current state representation
            action: Action taken in the current state
            reward: Reward received after the action
            next_state: State reached after the action
            done: Boolean indicating if the episode ended

        Uses a deque with maximum capacity
        to automatically remove old experiences
        when the buffer is full.
        """
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        """
        Trains the Q-network using a batch of
        experiences from memory (experience replay).

        Samples a random batch from memory if enough experiences are available,
        otherwise uses all stored experiences. This helps break correlations
        between consecutive experiences and improves training stability.
        """
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        """
        Trains the Q-network immediately with the current experience.

        Args:
            state: Current state representation
            action: Action taken in the current state
            reward: Reward received after the action
            next_state: State reached after the action
            done: Boolean indicating if the episode ended

        This immediate training helps the agent learn from recent experiences.
        """
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, sessions, dontlearn=False):
        """
        Selects an action using epsilon-greedy strategy.

        Args:
            state: Current state representation
            sessions: Total number of training sessions planned
            dontlearn: If True, disables exploration (pure exploitation)

        Returns:
            list: One-hot encoded action [straight, right, left]
                - [1, 0, 0]: Go straight
                - [0, 1, 0]: Turn right
                - [0, 0, 1]: Turn left

        Uses epsilon-greedy exploration vs exploitation:
        - High epsilon (early training): More random actions (exploration)
        - Low epsilon (late training): More Q-network decisions (exploitation)
        """
        if dontlearn:
            self.epsilon = 0
        else:
            self.epsilon = max(0, (80 * (sessions - self.n_games)) / sessions)
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move
