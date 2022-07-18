import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Game')
pygame.display.set_icon(pygame.image.load('images/flag.png'))

clock = pygame.time.Clock()

font = pygame.font.Font(None, 50)

surface = pygame.Surface((100, 100))
surface.fill('blue')

text_surface = font.render('GAME', False, 'white')

screen.blit(surface, (0, 0))
screen.blit(text_surface, (400 - text_surface.get_width()//2, 50))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    surface.scroll(10, 10)
    pygame.display.update()
    clock.tick(60)
