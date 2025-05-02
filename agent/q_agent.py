import random
import numpy as np
import json
import os
from agent.state_encoder import StateEncoder

class QAgent:
    """
    QAgent class representing a Q-learning agent for the game.
    Manages the Q-table and learning process.
    """

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, board_size=10, logger=None,
                 learning_rate=0.1, discount_factor=0.9, 
                 exploration_rate=1.0, exploration_decay=0.995,
                 exploration_min=0.01):
        """
        Initialize the QAgent with given parameters.

        Args:
            board_size: Size of the board (number of cells in one dimension)
            learning_rate: Learning rate for Q-learning
            discount_factor: Discount factor for future rewards
            exploration_rate: Initial exploration rate for epsilon-greedy policy
            exploration_decay: Decay rate for exploration over time
        """
        self.board_size = board_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.exploration_min = exploration_min

        self.encoder = StateEncoder()
        self.q_table = {}
    
    def _get_state_key(self, state):
        """
        Convert the state dictionary to a string key for the Q-table.
        Uses the state encoder to create a compact representation.
        """
        return self.encoder.encode(state)

    def _get_q_value(self, state_key, action):
        """
        Choose an action based on the current state.
        Uses epsilon-greedy strategy for exploration vs exploitation.
        """
        state_key = self._get_state_key(state_key)

        if random.random < self.exploration_rate:
            return random.randint(0, 3)
        else:
            self.q_table[state_key] = [0, 0, 0, 0]
            return random.randint(0, 3)

    def update(self, state, action, reward, next_state, done):
        """
        Update the Q-values based on the action taken and reward received.
        Implements the Q-learning update formula.
        """
        state_key = self._get_state_key(state)
        next_state_key = self._get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = [0, 0, 0, 0]
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = [0, 0, 0, 0]
        
        current_q = self.q_table[state_key][action]
        max_next_q = max(self.q_table[next_state_key]) if not done else 0

        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        self.q_table[state_key][action] = new_q

        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay
    
    def save_model(self, filepath):
        """
        Save the Q-table and agent parameters to a file.
        """

        model_data = {
            "q_table": self.q_table,
            "learning_rate": self.learning_rate,
            "discount_factor": self.discount_factor,
            "exploration_rate": self.exploration_rate,
            "exploration_decay": self.exploration_decay,
            "exploration_min": self.exploration_min,
            "board_size": self.board_size
        }
        with open(filepath, 'w') as f:
            json.dump(model_data, f)

    def load_model(self, filepath):
        """
        Load the Q-table and agent parameters from a file.
        """
        if not os.path.exists(filepath):
            if self.logger:
                self.logger.log(f"Model file {filepath} does not exist.")
            return False
        
        try:
            with open(filepath, 'r') as f:
                model_data = json.load(f)
                self.q_table = model_data["q_table"]
                self.learning_rate = model_data["learning_rate"]
                self.discount_factor = model_data["discount_factor"]
                self.exploration_rate = model_data["exploration_rate"]
                self.exploration_decay = model_data["exploration_decay"]
                self.exploration_min = model_data["exploration_min"]
                
                load_board_size = model_data.get("board_size", 10)
                if load_board_size != self.board_size:
                    if self.logger:
                        self.logger.log(f"Warning: Loaded model has board size {load_board_size}, "
                                  f"but current board size is {self.board_size}")
                if self.logger:
                    self.logger.log(f"Successfully loaded model from {filepath}")
            return True
        except Exception as e:
            if self.logger:
                self.logger.log(f"Error loading model from {filepath}: {e}")
            return False
      

        