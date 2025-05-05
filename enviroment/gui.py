import pygame
import time
import sys


class GUI:
    """
    GUI class for displaying the game.
    Uses pygame to render the board, snake, and apples.
    """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GRAY = (200, 200, 200)

    def __init__(self, board, speed=100, cell_size=40):
        """
        Initialize the GUI.

        Args:
            board_size: Size of the board (number of cells).
            speed: Speed of the game (in milliseconds).
            cell_size: Size of each cell in pixels.
        """
        self.board = board
        self.speed = speed
        self.cell_size = cell_size

        self.window_width = self.board.size * self.cell_size
        self.window_height = self.board.size * self.cell_size
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption("Learn2Slither")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

    def update(self):
        """
        Update the display.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill(self.GRAY)

        for x in range(0, self.window_width, self.cell_size):
            pygame.draw.line(self.screen, self.BLACK,
                             (x, 0), (x, self.window_height))
        for y in range(0, self.window_height, self.cell_size):
            pygame.draw.line(self.screen, self.BLACK,
                             (0, y), (self.window_width, y))

        for x in range(self.board.size):
            for y in range(self.board.size):
                cell_value = self.board.grid[x, y]

                if cell_value == self.board.SNAKE_HEAD:
                    self._draw_cell(x, y, self.BLUE)
                elif cell_value == self.board.SNAKE_BODY:
                    self._draw_cell(x, y, self.BLUE)
                elif cell_value == self.board.GREEN_APPLE:
                    self._draw_circle(x, y, self.GREEN)
                elif cell_value == self.board.RED_APPLE:
                    self._draw_circle(x, y, self.RED)
        pygame.display.flip()

        self.clock.tick(1000/self.speed)

    def _draw_cell(self, x, y, color):
        """
        Draw a filled cell at the given position.
        """
        rect = pygame.Rect(
            x * self.cell_size + 1,
            y * self.cell_size + 1,
            self.cell_size - 2,
            self.cell_size - 2
        )
        pygame.draw.rect(self.screen, color, rect)

    def _draw_circle(self, x, y, color):
        """
        Draw a filled circle at the given position.
        """
        center = (
            x * self.cell_size + self.cell_size // 2,
            y * self.cell_size + self.cell_size // 2
        )
        radius = self.cell_size // 2 - 2
        pygame.draw.circle(self.screen, color, center, radius)

    def wait_for_key(self):
        """
        Wait for a key press or mouse click.
        """
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.KEYDOWN or
                        event.type == pygame.MOUSEBUTTONDOWN):
                    waiting = False
            time.sleep(0.1)

    def close(self):
        """
        Close the GUI.
        """
        pygame.quit()
