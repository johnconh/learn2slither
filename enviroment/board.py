import random
import numpy as np
from collections import deque


class Board:
    """
    Board class representing the game environment.
    Manages the snake, apples, and game rules.
    """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    EMPTY = 0
    SNAKE_HEAD = 1
    SNAKE_BODY = 2
    GREEN_APPLE = 3
    RED_APPLE = 4
    WALL = 5

    CELL_REPRO = {
        EMPTY: "0",
        SNAKE_HEAD: "H",
        SNAKE_BODY: "S",
        GREEN_APPLE: "G",
        RED_APPLE: "R",
        WALL: "W"
    }

    def __init__(self, size=10, logger=None):
        """
        Initialize the board with a given size and logger.

        Args:
            size: Size of the board (number of cells in one dimension)
            logger: Logger instance for logging events
        """
        self.size = size
        self.logger = logger
        self.grid = np.zeros((size, size), dtype=int)
        self.snake = deque()
        self.green_apples = []
        self.red_apples = []
        self.direction = None
        self.snake_length = 0
        self.game_over = False
        self.steps_without_eating = 0
        self.max_steps_without_eating = size * 3
        self.reset()

    def reset(self):
        """
        Reset the board to its initial state.
        """
        self.grid.fill(self.EMPTY)
        self.snake.clear()
        self.green_apples.clear()
        self.red_apples.clear()

        start_x = random.randint(3, self.size - 4)
        start_y = random.randint(3, self.size - 4)

        self.direction = random.choice([self.UP, self.RIGHT,
                                        self.DOWN, self.LEFT])
        if self.direction == self.UP:
            positions = [(start_x, start_y), (start_x, start_y + 1),
                         (start_x, start_y + 2)]
        elif self.direction == self.RIGHT:
            positions = [(start_x, start_y), (start_x - 1, start_y),
                         (start_x - 2, start_y)]
        elif self.direction == self.DOWN:
            positions = [(start_x, start_y), (start_x, start_y - 1),
                         (start_x, start_y - 2)]
        else:
            positions = [(start_x, start_y), (start_x + 1, start_y),
                         (start_x + 2, start_y)]

        for i, (x, y) in enumerate(positions):
            self.snake.append((x, y))
            if i == 0:
                self.grid[x, y] = self.SNAKE_HEAD
            else:
                self.grid[x, y] = self.SNAKE_BODY

        self.snake_length = len(self.snake)
        self._place_apples(self.GREEN_APPLE, 2)
        self._place_apples(self.RED_APPLE, 1)
        self.game_over = False
        self.steps_without_eating = 0

    def _place_apples(self, apple_type, count):
        """
        Place apples on the board.

        Args:
            apple_type: Type of apple to place (GREEN_APPLE or RED_APPLE)
            count: Number of apples to place
        """
        apple_placed = 0
        head_x, head_y = self.snake[0]
        while apple_placed < count:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            distance = abs(head_x - x) + abs(head_y - y)
            if self.grid[x, y] == self.EMPTY and distance > 2:
                self.grid[x, y] = apple_type
                if apple_type == self.GREEN_APPLE:
                    self.green_apples.append((x, y))
                else:
                    self.red_apples.append((x, y))
                apple_placed += 1

    def _get_next_head_position(self, action):
        """
        Get the next position of the snake head based on the action.
        """
        head_x, head_y = self.snake[0]

        if action == self.UP:
            return (head_x, head_y - 1)
        elif action == self.RIGHT:
            return (head_x + 1, head_y)
        elif action == self.DOWN:
            return (head_x, head_y + 1)
        else:
            return (head_x - 1, head_y)
    
    def _calculate_distance_fod(self):
        """
        Calculate distance from head to closest green apple.
        Returns Manhattan distance to the closest apple.
        """
        if not self.green_apples:
            return self.size * 2
        
        head_x, head_y = self.snake[0]
        min_distance = float("inf")

        for apple_x, apple_y in self.green_apples:
            distance = abs(head_x - apple_x) + abs(head_y - apple_y)
            if distance < min_distance:
                min_distance = distance

        return min_distance

    def step(self, action):
        """
        Take a step in the environment based on the given action.
        Returns reward, done, info
        """
        if self.game_over:
            return 0, True, {"reason": "Game Over"}
        
        old_distance = self._calculate_distance_fod()
        next_x, next_y = self._get_next_head_position(action)
        self.direction = action
        self.steps_without_eating += 1

        if not (0 <= next_x < self.size and 0 <= next_y < self.size):
            self.game_over = True
            return -30, True, {"reason": "Hit the wall"}

        if self.grid[next_x, next_y] == self.SNAKE_BODY:
            self.game_over = True
            return -30, True, {"reason": "Hit self"}

        self.snake.appendleft((next_x, next_y))
        old_head_x, old_head_y = self.snake[1]
        self.grid[old_head_x, old_head_y] = self.SNAKE_BODY

        if self.grid[next_x, next_y] == self.GREEN_APPLE:
            self.snake_length += 1
            self.green_apples.remove((next_x, next_y))
            self._place_apples(self.GREEN_APPLE, 1)
            self.grid[next_x, next_y] = self.SNAKE_HEAD
            self.steps_without_eating = 0
            return 20, False, {"reason": "Ate green apple"}
        elif self.grid[next_x, next_y] == self.RED_APPLE:
            self.snake_length -= 1
            self.red_apples.remove((next_x, next_y))
            self._place_apples(self.RED_APPLE, 1)
            self.grid[next_x, next_y] = self.SNAKE_HEAD
            self.steps_without_eating = 0

            if self.snake_length <= 0:
                self.game_over = True
                return -20, True, {"reason": "Ate red apple and died"}

            last_x, last_y = self.snake.pop()
            self.grid[last_x, last_y] = self.EMPTY
            if self.snake_length > 0:
                last_x, last_y = self.snake.pop()
                self.grid[last_x, last_y] = self.EMPTY

            return -10, False, {"reason": "Ate red apple"}

        else:
            self.grid[next_x, next_y] = self.SNAKE_HEAD
            last_x, last_y = self.snake.pop()
            self.grid[last_x, last_y] = self.EMPTY

            new_distance = self._calculate_distance_fod()
            distance_reward = 0
            if new_distance < old_distance:
                distance_reward = 1.0
            elif new_distance > old_distance:
                distance_reward = -0.5
            else:
                distance_reward = 0.0
            
            if self.steps_without_eating > self.max_steps_without_eating:
                self.game_over = True
                return -10, True, {"reason": "Too many steps without eating"}

            return distance_reward, False, {"reason": "Moved"}

    def get_snake_vision(self):
        """
        Get the snake's vision in all four directions.
        The snake can only see in the 4 directions from its head.0.
        """
        head_x, head_y = self.snake[0]
        vision = {}
        vision["up"] = self._look_in_direction(head_x, head_y, 0, -1)
        vision["right"] = self._look_in_direction(head_x, head_y, 1, 0)
        vision["down"] = self._look_in_direction(head_x, head_y, 0, 1)
        vision["left"] = self._look_in_direction(head_x, head_y, -1, 0)

        # if self.logger:
        #     self.logger.log(f"Vision: {vision}")
        return vision

    def print_snake_vision_grid(self):
        """
        Print the board showing only what the snake can see in the 4 directions from its head.
        All other cells are hidden (printed as spaces).
        """
        vision = self.get_snake_vision()
        head_x, head_y = self.snake[0]

        vision_grid = [[" " for _ in range(self.size)] for _ in range(self.size)]

        vision_grid[head_x][head_y] = "H"

        def mark_vision(dx, dy, values):
            x, y = head_x, head_y
            for val in values:
                x += dx
                y += dy
                if 0 <= x < self.size and 0 <= y < self.size:
                    vision_grid[x][y] = self.CELL_REPRO[val]
                else:
                    prev_x, prev_y = x - dx, y - dy
                    if 0 <= prev_x < self.size and 0 <= prev_y < self.size:
                        vision_grid[prev_x][prev_y] = self.CELL_REPRO[self.WALL]

        mark_vision(0, -1, vision["up"])
        mark_vision(1, 0, vision["right"])
        mark_vision(0, 1, vision["down"])
        mark_vision(-1, 0, vision["left"])

        for y in range(self.size):
            row = "".join(vision_grid[x][y] for x in range(self.size))
            print(row)

    def _look_in_direction(self, start_x, start_y, dx, dy):
        """
        Look in a specific direction from the snake's head.
        Returns a list of cell types seen.
        """
        x, y = start_x, start_y
        vision = []

        while True:
            x += dx
            y += dy

            if not (0 <= x < self.size and 0 <= y < self.size):
                vision.append(self.WALL)
                break

            vision.append(self.grid[x, y])
        return vision

    def __str__(self):
        """
        Return a string representation of the board for terminal display.
        """
        result = ""
        for i in range(self.size):
            for j in range(self.size):
                result += self.CELL_REPRO[self.grid[i, j]] + ""
            result += "\n"
        return result
