import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((400, 200))

print(pygame.event.get())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.time.set_timer()
    pygame.display.update()
