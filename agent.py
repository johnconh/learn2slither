import torch
import random
import numpy as np
from collections import deque
from snakeAI import Direction, Point, FoodType
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
        self.model = QNet(15, 512, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        """
        Converts the current game state into
        a feature vector for the neural network.

        Args:
            game: The Snake game environment instance
        Returns:
            numpy.array: A binary feature vector (15 elements) representing:
                - Danger detection (straight, right, left) - 3 elements
                - Current direction (left, right, up, down) - 4 elements
                - Food direction relative to head (green apple) - 4 elements
                - Food direction relative to head (red apple) - 4 elements

        The agent can only use information visible
        from the snake's head position.
        """
        head = game.snake[0]
        block_size = game.block_size
        point_l = Point(head.x - block_size, head.y)
        point_r = Point(head.x + block_size, head.y)
        point_u = Point(head.x, head.y - block_size)
        point_d = Point(head.x, head.y + block_size)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        green_foods = [food for food, food_type in game.foods
                       if food_type == FoodType.GREEN]
        red_foods = [food for food, food_type in game.foods
                     if food_type == FoodType.RED]

        def manhattan(p1, p2):
            """Calculate Manhattan distance between two points."""
            return abs(p1.x - p2.x) + abs(p1.y - p2.y)

        closest_green = (min(green_foods, key=lambda f: manhattan(head, f))
                         if green_foods else Point(0, 0))
        red_food = red_foods[0] if red_foods else Point(0, 0)

        state = [
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            dir_l,
            dir_r,
            dir_u,
            dir_d,

            closest_green.x < head.x,
            closest_green.x > head.x,
            closest_green.y < head.y,
            closest_green.y > head.y,

            red_food.x < head.x,
            red_food.x > head.x,
            red_food.y < head.y,
            red_food.y > head.y,
        ]
        return np.array(state, dtype=int)

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
