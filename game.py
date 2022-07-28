import pygame
from sys import exit
from time import time


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption('Game')
    pygame.display.set_icon(pygame.image.load('graphics/Icon/flag.png'))

    clock = pygame.time.Clock()

    grass = pygame.image.load('graphics/sprites/platforms/grass.png').convert()
    sky_bg = pygame.image.load('graphics/sprites/background/sky.png').convert()

    character_idle = pygame.image.load('graphics/sprites/character/idle.png').convert()
    character_right = pygame.image.load('graphics/sprites/character/right.png').convert()
    character_left = pygame.image.load('graphics/sprites/character/left.png').convert()

    character_x = 375
    character_y = 300

    pressed_keys = [None]

    while True:
        screen.blit(sky_bg, (0, 0))

        for i in range(16):
            screen.blit(grass, (50*i, 350))

        dt = clock.tick(60)/1000

        character = character_idle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                pressed_keys.append(event.key)
            elif event.type == pygame.KEYUP:
                pressed_keys.remove(event.key)

        match pressed_keys[-1]:
            case(None):
                character = character_idle
            case(pygame.K_d):
                character = character_right
                character_x += 200 * dt
            case(pygame.K_q):
                character = character_left
                character_x -= 200 * dt

        screen.blit(character, (character_x, character_y))
        pygame.display.update()


if __name__ == "__main__":
    main()
