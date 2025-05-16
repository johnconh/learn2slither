import pygame
import random
from enum import Enum
from collections import namedtuple
import json
import os
import time
pygame.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLUE_LIGHT = (0, 171, 197)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 21)
    
font = pygame.font.Font(None, 30)
big_font = pygame.font.Font(None, 50)

SCORE_FILE = "score.json"
BLOCK_SIZE = 20

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple("Point", 'x, y')

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
    
    def draw(self, screen):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=8)

        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake Game")
        button_w, button_h = 200, 50
        button_x = (self.w - button_w) // 2
        button_y = self.h - button_h - 50
        self.retry_button = Button("Retry", button_x, button_y, button_w, button_h)
        self.clock = pygame.time.Clock()
        self.game_active = True
        self.scores = self.load_scores()
        self.reset()

    def load_scores(self):
        try:
            if os.path.exists(SCORE_FILE):
                with open(SCORE_FILE, 'r') as f:
                    return json.load(f)
            else:
                return []
        except:
            return []
    
    def save_scores(self, score, game_time):
        self.scores.append({
            "score": score,
            "time":  game_time
        })

        self.scores.sort(key=lambda x: (-x["score"], x["time"]))

        self.scores = self.scores[:10]

        try:
            with open(SCORE_FILE, 'w') as f:
                json.dump(self.scores, f)
        except Exception as e:
            print(f"Error saving scores: {e}")

    def reset(self):
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
        self.speed = 5
        self.maxspeed = 42
        self.star_time = time.time()
        self.game_active = True

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if not self.game_active and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.retry_button.is_clicked(mouse_pos):
                    self.reset()
                    return False, self.score
 
            if self.game_active and event.type == pygame.KEYDOWN:
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

        if not self.game_active:
            self.show_gameover()
            return False, self.score

        self._move(self.direction)
        self.snake.insert(0, self.head)

        if self._is_collision():
            self.game_active = False
            game_time = round(time.time() - self.star_time, 1)
            self.save_scores(self.score, game_time)
            self.current_time = game_time
            return True, self.score

        self._update_ui()
        self.clock.tick(self.speed)
        return False, self.score

    def _is_collision(self):
        if self.head.x > self.w-BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h-BLOCK_SIZE or self.head.y < 0:
            return True
        
        if self.head in self.snake[1:]:
            return True
        
        if self.head in self.green_apples:
            self.score += 1
            self.green_apples.remove(self.head)
            self._place_green_apples(1)
            self.speed = min(self.speed + 1, self.maxspeed)
            return False
        elif self.head == self.red_apple:
            if len (self.snake) == 4:
                return True
            self.snake.pop()
            self.snake.pop()
            self.score -= 1
            self._place_red_apple()
            self.speed = min(self.speed + 1, self.maxspeed)
            return False

        self.snake.pop()
        return False
    
    def show_gameover(self):
        self.display.fill(BLACK)
        gameover = big_font.render("Game Over", True, WHITE)
        self.display.blit(gameover, (self.w/2 - gameover.get_width()/2, 50))

        score_text = font.render(f"Score: {self.score}", True, WHITE)
        time_text = font.render(f"Time: {self.current_time} sec", True, WHITE)

        self.display.blit(score_text, (self.w/2 - score_text.get_width()/2, 120))
        self.display.blit(time_text, (self.w/2 - time_text.get_width()/2, 150))

        if self.scores:
            high_score_text = font.render("HIGH SCORES", True, WHITE)
            self.display.blit(high_score_text, (self.w/2 - high_score_text.get_width()/2, 200))
            for i, score in enumerate(self.scores[:5]):
                score_text = font.render(f"{i+1}. {score['score']} ({score['time']} sec)", True, WHITE)
                self.display.blit(score_text, (self.w/2 - score_text.get_width()/2, 230 + i*30))

        mouse_pos = pygame.mouse.get_pos()
        self.retry_button.update(mouse_pos)
        self.retry_button.draw(self.display)
        pygame.display.flip()

    def _update_ui(self):
        self.display.fill(BLACK)

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

def main():
    game = SnakeGame()

    while True:
        game.play_step()

if __name__ == "__main__":
    main()
