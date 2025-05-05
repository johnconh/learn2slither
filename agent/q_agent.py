import random
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

    OP_ACT = {
        UP: DOWN,
        RIGHT: LEFT,
        DOWN: UP,
        LEFT: RIGHT
    }

    def __init__(self, board_size=10, logger=None,
                 learning_rate=0.1, discount_factor=0.95,
                 exploration_rate=1.0, exploration_decay=0.995,
                 exploration_min=0.05):
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
        self.logger = logger

        self.encoder = StateEncoder()
        self.q_table = {}

    def _get_state_key(self, state):
        """
        Convert the state dictionary to a string key for the Q-table.
        Uses the state encoder to create a compact representation.
        """
        return self.encoder.encode(state)

    def choose_action(self, state_key, current_direction):
        """
        Choose an action based on the current state.
        Uses epsilon-greedy strategy for exploration vs exploitation.
        """
        state_key = self._get_state_key(state_key)

        valid_actions = [a for a in range(4) if a != self.OP_ACT[current_direction]]

        if state_key not in self.q_table:
            self.q_table[state_key] = [0, 0, 0, 0]

        if random.random() < self.exploration_rate:
            return random.choice(valid_actions)
        
        q_values = self.q_table.get(state_key, {})
        valid_q_values = [(action, q_values[action]) for action in valid_actions]
        best_action = max(valid_q_values, key=lambda a: q_values[a])

        return best_action

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

        if done:
            max_next_q = 0
        else:
            next_direction = action
            valid_next_actions = [a for a in range(4) if a != self.OP_ACT[next_direction]]
            valid_next_q_values = [self.q_table[next_state_key][a] for a in valid_next_actions]
            max_next_q = max(valid_next_q_values) if valid_next_q_values else 0
        
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
                        self.logger.log(
                            "Warning: Loaded model "
                            f"has board size {load_board_size}, "
                            f"but current board size is {self.board_size}")
                if self.logger:
                    self.logger.log("Successfully loaded "
                                    f"model from {filepath}")
            return True
        except Exception as e:
            if self.logger:
                self.logger.log(f"Error loading model from {filepath}: {e}")
            return False
