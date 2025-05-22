import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font(None, 30)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')


WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


class FoodType(Enum):
    GREEN = 1
    RED = 2


class Snake:
    def __init__(self, board_size, visual, step_by_step, speed):
        self.w = 800
        self.visual = visual == "on"
        self.step_by_step = step_by_step
        self.speed = speed
        self.num_cells = board_size
        self.block_size = self.w // self.num_cells
        self.w = self.block_size * self.num_cells
        self.h = self.block_size * self.num_cells

        if self.visual:
            self.display = pygame.display.set_mode((self.w, self.h))
            pygame.display.set_caption('Snake')
            self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(
            random.randint(
                0,
                (self.w - self.block_size) // self.block_size
            ) * self.block_size,
            random.randint(
                0,
                (self.h - self.block_size) // self.block_size
            ) * self.block_size
        )
        self.snake = [self.head,
                      Point(self.head.x-self.block_size, self.head.y),
                      Point(self.head.x-(2*self.block_size), self.head.y)]
        self.score = 0
        self.foods = []
        self._place_foods()
        self.frame_iteration = 0

    def _place_foods(self):
        green_count = sum(
            1 for _,
            food_type in self.foods if food_type == FoodType.GREEN
        )
        red_count = sum(
            1 for _,
            food_type in self.foods if food_type == FoodType.RED
        )

        for _ in range(2 - green_count):
            self._place_food(FoodType.GREEN)
        if red_count < 1:
            self._place_food(FoodType.RED)

    def _place_food(self, food_type):
        while True:
            x = random.randint(
                0,
                (self.w - self.block_size) // self.block_size
            ) * self.block_size
            y = random.randint(
                0,
                (self.h - self.block_size) // self.block_size
            ) * self.block_size
            food_point = Point(x, y)

            if food_point in self.snake or any(fp == food_point for fp,
                                               _ in self.foods):
                continue
            else:
                self.foods.append((food_point, food_type))
                break

    def _distance_to_closest_green(self, head):
        green_foods = [p for p, t in self.foods if t == FoodType.GREEN]
        if not green_foods:
            return 0
        return min(abs(head.x - f.x) + abs(head.y - f.y) for f in green_foods)

    def play_step(self, action):
        self.frame_iteration += 1

        if self.visual:
            self._update_ui()
            self.clock.tick(self.speed)
        if not self.visual or (self.visual and self.step_by_step):
            self._get_snake_vision()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        old_distance = self._distance_to_closest_green(self.head)
        self._move(action)
        self.snake.insert(0, self.head)
        new_distance = self._distance_to_closest_green(self.head)
        reward = 0
        game_over = False

        if old_distance > new_distance:
            reward += 1
        else:
            reward -= 1

        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        food_eaten = False
        for i, (food_point, food_type) in enumerate(self.foods):
            if self.head == food_point:
                food_eaten = True
                if food_type == FoodType.GREEN:
                    self.score += 1
                    reward = 10
                elif food_type == FoodType.RED:
                    if len(self.snake) == 0:
                        game_over = True
                        reward = -15
                        return reward, game_over, self.score
                    else:
                        self.snake.pop()
                        self.score -= 1
                        reward = -5
                self.foods.pop(i)
                self._place_food(food_type)
                break

        if not food_eaten:
            self.snake.pop()

        if self.step_by_step:
            pause = True
            if self.visual:
                while pause:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            pause = False
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
            else:
                input("Press Enter to continue...")
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if (
            pt.x > self.w - self.block_size or pt.x < 0 or
            pt.y > self.h - self.block_size or pt.y < 0
        ):
            return True
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(
                self.display, BLUE1,
                pygame.Rect(pt.x, pt.y, self.block_size, self.block_size)
            )
            inner_size = self.block_size * 0.6
            offset = (self.block_size - inner_size) / 2
            pygame.draw.rect(self.display,
                             BLUE2,
                             pygame.Rect(pt.x + offset, pt.y + offset,
                                         inner_size, inner_size))

        for food_point, food_type in self.foods:
            color = GREEN if food_type == FoodType.GREEN else RED
            pygame.draw.rect(
                self.display,
                color,
                pygame.Rect(food_point.x, food_point.y,
                            self.block_size, self.block_size)
            )

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN,
                      Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        if not self.visual or (self.visual and self.step_by_step):
            print(new_dir.name)

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += self.block_size
        elif self.direction == Direction.LEFT:
            x -= self.block_size
        elif self.direction == Direction.DOWN:
            y += self.block_size
        elif self.direction == Direction.UP:
            y -= self.block_size

        self.head = Point(x, y)

    def _get_snake_vision(self):
        head_x, head_y = (
            int(self.head.x // self.block_size),
            int(self.head.y // self.block_size)
        )

        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }

        vision = [
            [" " for _ in range(self.num_cells + 2)]
            for _ in range(self.num_cells + 2)
        ]
        vision[head_y + 1][head_x + 1] = "H"

        for (dx, dy) in directions.items():
            x, y = head_x, head_y
            while True:
                x += dx
                y += dy

                vis_x, vis_y = x + 1, y + 1
                if (
                    vis_x < 0 or vis_x >= len(vision[0]) or
                    vis_y < 0 or vis_y >= len(vision)
                ):
                    break

                if (
                    x < 0 or x >= self.num_cells or
                    y < 0 or y >= self.num_cells
                ):
                    vision[vis_y][vis_x] = "W"
                    break
                elif (
                    Point(x * self.block_size, y * self.block_size) in
                    self.snake
                ):
                    vision[vis_y][vis_x] = "S"
                else:
                    vision[vis_y][vis_x] = "0"

                for food_point, food_type in self.foods:
                    if (
                        food_point.x // self.block_size == x and
                        food_point.y // self.block_size == y
                    ):
                        vision[vis_y][vis_x] = (
                            "G" if food_type == FoodType.GREEN else "R"
                        )

        for row in vision:
            print(" ".join(row))
        print("\n")

    def get_state(self):
        """
        Converts the current game state into
        a feature vector for the neural network.

        Returns:
            numpy.array: A binary feature vector (15 elements) representing:
                - Danger detection (straight, right, left) - 3 elements
                - Current direction (left, right, up, down) - 4 elements
                - Food direction relative to head (green apple) - 4 elements
                - Food direction relative to head (red apple) - 4 elements

        The agent can only use information visible
        from the snake's head position.
        """
        point_l = Point(self.head.x - self.block_size, self.head.y)
        point_r = Point(self.head.x + self.block_size, self.head.y)
        point_u = Point(self.head.x, self.head.y - self.block_size)
        point_d = Point(self.head.x, self.head.y + self.block_size)

        dir_l = self.direction == Direction.LEFT
        dir_r = self.direction == Direction.RIGHT
        dir_u = self.direction == Direction.UP
        dir_d = self.direction == Direction.DOWN

        green_foods = [food for food, food_type in self.foods
                       if food_type == FoodType.GREEN]
        red_foods = [food for food, food_type in self.foods
                     if food_type == FoodType.RED]

        def manhattan(p1, p2):
            """Calculate Manhattan distance between two points."""
            return abs(p1.x - p2.x) + abs(p1.y - p2.y)

        closest_green = (
            min(green_foods, key=lambda f: manhattan(self.head, f))
            if green_foods else Point(0, 0)
        )
        red_food = red_foods[0] if red_foods else Point(0, 0)

        state = [
            (dir_r and self.is_collision(point_r)) or
            (dir_l and self.is_collision(point_l)) or
            (dir_u and self.is_collision(point_u)) or
            (dir_d and self.is_collision(point_d)),

            (dir_u and self.is_collision(point_r)) or
            (dir_d and self.is_collision(point_l)) or
            (dir_l and self.is_collision(point_u)) or
            (dir_r and self.is_collision(point_d)),

            (dir_d and self.is_collision(point_r)) or
            (dir_u and self.is_collision(point_l)) or
            (dir_r and self.is_collision(point_u)) or
            (dir_l and self.is_collision(point_d)),

            dir_l,
            dir_r,
            dir_u,
            dir_d,

            closest_green.x < self.head.x,
            closest_green.x > self.head.x,
            closest_green.y < self.head.y,
            closest_green.y > self.head.y,

            red_food.x < self.head.x,
            red_food.x > self.head.x,
            red_food.y < self.head.y,
            red_food.y > self.head.y,
        ]

        state_array = np.array(state, dtype=int)
        return state_array
