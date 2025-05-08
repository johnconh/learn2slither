import pygame
import random
from enum import Enum
from collections import namedtuple
pygame.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLUE_LIGHT = (0, 171, 197)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
    
font = pygame.font.Font(None, 30)

BLOCK_SIZE = 20
SPEED = 10

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple("Point", 'x, y')

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.direction =  Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.green_apples = []
        self.red_apple = None
        self._place_green_apples(2)
        self._place_red_apple()

    def _place_green_apples(self, count):
        for _ in range(count):
            while True:
                x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
                y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
                point = Point(x, y)
                if point not in self.snake and point not in self.green_apples:
                    self.green_apples.append(point)
                    break
    
    def _place_red_apple(self):
        while True:
            x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
            point = Point(x, y)
            if point not in self.snake and point not in self.green_apples:
                self.red_apple = point
                break

    def play_step(self):
        self._handle_event()
        self._move(self.direction)
        self.snake.insert(0, self.head)
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        self._update_ui()
        self.clock.tick(SPEED)
        return game_over, self.score

    def _handle_event(self,):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    if self.direction != Direction.UP:
                        self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    if self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    if self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT

    def _is_collision(self):
        if self.head.x > self.w-BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h-BLOCK_SIZE or self.head.y < 0:
            return True
        
        if self.head in self.snake[1:]:
            return True
        
        if self.head in self.green_apples:
            self.score += 1
            self.green_apples.remove(self.head)
            while len(self.green_apples) < 2:
                self._place_green_apples(1)
            return False
        elif self.head == self.red_apple:
            if len (self.snake) == 4:
                return True
            self.snake.pop()
            self.snake.pop()
            self.score -= 1
            self._place_red_apple()
            return False

        self.snake.pop()
        return False

    def _update_ui(self):
        self.display.fill(GRAY)

        for x in range(0, self.w, BLOCK_SIZE):
            pygame.draw.line(self.display, BLACK, (x, 0), (x, self.h))

        for y in range(0, self.h, BLOCK_SIZE):
            pygame.draw.line(self.display, BLACK, (0, y), (self.w, y))

        for point in self.snake:
            pygame.draw.rect(self.display, BLUE, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE_LIGHT, pygame.Rect(point.x+4, point.y+4, 12, 12))

        for apple in self.green_apples:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(apple.x, apple.y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.red_apple.x, self.red_apple.y, BLOCK_SIZE, BLOCK_SIZE))

        font = pygame.font.Font(None, 30)
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, (5, 5))
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        self.head = Point(x, y)

if __name__ == "__main__":
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break
    print('Final Score', score)
    pygame.quit()

