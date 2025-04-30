import os
import pygame

os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"
pygame.init()

screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Ventana de prueba Pygame")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 50))
    pygame.draw.circle(screen, (0, 255, 0), (200, 200), 50)
    pygame.display.flip()

pygame.quit()
