import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Game')
pygame.display.set_icon(pygame.image.load('images/flag.png'))
clock = pygame.time.Clock()

surface = pygame.Surface((100, 100))
surface.fill('blue')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(surface, (0, 0))

    pygame.display.update()
    clock.tick(60)
