import pygame
from sys import exit
from math import ceil

g = 270
a = [True]


class Character(pygame.sprite.Sprite):
    def __init__(self, coordinates: tuple, **sprites):
        super().__init__()
        self.sprites = sprites
        self.image = sprites['idle']

        # Rectangle (Hitbox)
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates

        # Velocity
        self.vx = 0
        self.vy = 0

        # Acceleration
        self.ax = 0
        self.ay = g

        # Status (landed or not)
        self.landed = True

    def update(self, dt, input, group):

        # Input
        if self.landed and pygame.K_SPACE in input:
            self.jump()

        if pygame.K_d in input:
            self.vx = 200
            self.image = self.sprites['runR']
        elif pygame.K_q in input:
            self.vx = -200
            self.image = self.sprites['runL']
        else:
            self.vx = 0
            self.image = self.sprites['idle']

        # Velocity
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        # Collisions
        x_offset = ceil(self.vx * dt)
        y_offset = ceil(self.vy * dt)

        # X collision
        self.rect.x += x_offset
        collision_sprites = pygame.sprite.spritecollide(self, group, False)
        for sprite in collision_sprites:
            if (self.rect.bottom == sprite.rect.top and self.landed):
                continue

            self.vx = 0
            if (self.rect.right >= sprite.rect.left and
                    self.rect.left < sprite.rect.left):
                self.rect.right = sprite.rect.left
            else:
                self.rect.left = sprite.rect.right

        # Y Collision
        self.rect.y += y_offset
        collision_sprites = pygame.sprite.spritecollide(self, group, False)
        self.landed = False
        for sprite in collision_sprites:
            if abs(self.rect.x - sprite.rect.x) == 50:
                continue

            self.vy = 0
            if (self.rect.bottom >= sprite.rect.top and
                    self.rect.top < sprite.rect.top):
                self.rect.bottom = sprite.rect.top
                self.landed = True
            else:
                self.rect.top = sprite.rect.bottom

    def jump(self):
        if not self.landed:
            return

        self.vy = -250


class Block(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, coordinates):
        super().__init__()

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates


def main() -> None:
    pygame.init()

    # General
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption('Game')
    pygame.display.set_icon(pygame.image.load('graphics/Icon/flag.png'))

    clock = pygame.time.Clock()
    FPS = 60
    pressed_keys = set()

    # Sprites
    grass = pygame.image.load('graphics/sprites/platforms/grass.png').convert()
    dirt = pygame.image.load('graphics/sprites/platforms/dirt.png').convert()
    sky_bg = pygame.image.load('graphics/sprites/background/sky.png').convert()
    character_idle = pygame.image.load(
        'graphics/sprites/character/idle.png'
        ).convert()
    character_runR = pygame.image.load(
        'graphics/sprites/character/runR.png'
        ).convert()
    character_runL = pygame.image.load(
        'graphics/sprites/character/runL.png'
        ).convert()

    character_sprites = dict(
        idle=character_idle,
        runR=character_runR,
        runL=character_runL
        )

    # Level
    map = {
        grass: (
            (0, 300),
            (100, 250),
            (50, 350),
            (100, 350),
            (150, 350),
            (200, 350),
            (250, 350),
            (300, 350),
            (300, 200),
            (350, 350),
            (400, 350),
            (450, 350),
            (600, 350),
            (650, 350),
            (700, 350),
            (750, 350)
            ),
        dirt: (
            (0, 350),
        )
        }

    spawnpoint = ((375, 200))

    player = Character(
        spawnpoint,
        **character_sprites
        )

    player_group = pygame.sprite.GroupSingle()
    player_group.add(player)

    static_blocks = pygame.sprite.Group()

    for tile, positions in map.items():
        for coord in positions:
            static_blocks.add(Block(tile, coord))

    while True:
        # Event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                pressed_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                pressed_keys.remove(event.key)

        screen.blit(sky_bg, (0, 0))
        static_blocks.draw(screen)

        player.update(clock.tick(FPS)/1000, pressed_keys, static_blocks)
        player_group.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
