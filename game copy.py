import pygame
from sys import exit

g = 60
a = [True]


class Character:
    def __init__(self, coordinates: tuple, **sprites: pygame.Surface):
        self.x, self.y = coordinates
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

        self.vx = 0
        self.vy = 0

        self.ax = 0
        self.ay = g

        self.idle_sprite = sprites.get('idle')
        self.runR_sprite = sprites.get('runR')
        self.runL_sprite = sprites.get('runL')

        self.current_sprite = self.idle_sprite

        self.can_jump = True

    def update(self, screen, dt, tiles):

        self.vx += self.ax * dt
        self.vy += self.ay * dt

        if self.vx > 0:
            self.current_sprite = self.runR_sprite
        elif self.vx < 0:
            self.current_sprite = self.runL_sprite
        else:
            self.current_sprite = self.idle_sprite

        x_offset = self.vx * dt
        if self.rect.move(x_offset, 0).collidelist(tiles) == -1:
            self.x += x_offset
            self.rect.x = self.x

        y_offset = self.vy * dt
        collision_idx = self.rect.move(0, y_offset).collidelist(tiles)
        if collision_idx == -1:
            self.y += y_offset
            self.rect.y = self.y
        else:
            self.y = tiles[collision_idx].y - 50
            self.rect.y = self.y
            self.can_jump = True

        screen.blit(self.current_sprite, (self.x, self.y))

    def jump(self):
        if not self.can_jump:
            return
        
        self.vy = -90
        self.can_jump = False


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption('Game')
    pygame.display.set_icon(pygame.image.load('graphics/Icon/flag.png'))

    clock = pygame.time.Clock()

    grass = pygame.image.load('graphics/sprites/platforms/grass.png').convert()
    sky_bg = pygame.image.load('graphics/sprites/background/sky.png').convert()

    character_idle = pygame.image.load(
        'graphics/sprites/character/idle.png'
        ).convert()
    character_right = pygame.image.load(
        'graphics/sprites/character/right.png'
        ).convert()
    character_left = pygame.image.load(
        'graphics/sprites/character/left.png'
        ).convert()

    player = Character(
        (375, 200),
        idle=character_idle,
        runR=character_right,
        runL=character_left
        )

    pressed_keys = [None]

    tiles = []

    for i in range(16):
        tiles.append(pygame.Rect(50*i, 350, 50, 50))
        screen.blit(grass, (50*i, 350))

    while True:
        screen.blit(sky_bg, (0, 0))

        for i in range(16):
            screen.blit(grass, (50*i, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                else:
                    pressed_keys.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key != pygame.K_SPACE:
                    pressed_keys.remove(event.key)

        match pressed_keys[-1]:
            case(None):
                player.vx = 0
            case(pygame.K_d):
                player.vx = 200
            case(pygame.K_q):
                player.vx = -200

        player.update(screen, clock.tick(60)/1000, tiles)
        pygame.display.update()


if __name__ == "__main__":
    main()
