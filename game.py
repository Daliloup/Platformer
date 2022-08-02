import pygame
from sys import exit
from math import ceil

g = 270
a = [True]


class Character(pygame.sprite.Sprite):
    def __init__(self, coordinates: tuple, sprites):
        super().__init__()
        self.sprites = sprites
        self.image_idx = 2
        self.image = sprites[self.image_idx]

        # Rectangle (Hitbox)
        self.x, self.y = coordinates
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates

        # Velocity
        self.vx = 0
        self.vy = 0

        # Acceleration
        self.ax = 0
        self.ay = g

        # Status (landed or not)
        self.HP = 3
        self.iframes = 0
        self.landed = True

    def update(self, dt, input, group):

        # Input
        if self.landed and pygame.K_SPACE in input:
            self.jump()

        if pygame.K_d in input:
            self.vx = 200
            if self.image_idx != 4:
                self.image_idx += 1
        elif pygame.K_q in input:
            self.vx = -200
            if self.image_idx != 0:
                self.image_idx -= 1
        else:
            self.vx = 0
            if self.image_idx > 2:
                self.image_idx -= 1
            elif self.image_idx < 2:
                self.image_idx += 1
        
        self.image = self.sprites[self.image_idx]

        if self.iframes:
            self.iframes -= 1

        # Velocity
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        # Collisions
        x_offset = ceil(self.vx * dt)
        y_offset = ceil(self.vy * dt)

        # X collision
        self.x += x_offset
        self.rect.x += x_offset
        collision_sprites = pygame.sprite.spritecollide(self, group, False)
        for sprite in collision_sprites:
            if sprite == self:
                continue
            if (self.rect.bottom == sprite.rect.top and self.landed):
                continue

            if sprite.dmg and self.iframes == 0:
                self.HP -= sprite.dmg
                self.iframes = 60

            self.vx = 0
            if (self.rect.right >= sprite.rect.left and
                    self.rect.left < sprite.rect.left):
                self.rect.right = sprite.rect.left
                self.x = sprite.x - 50
            else:
                self.rect.left = sprite.rect.right
                self.x = sprite.x + sprite.rect.width

        # Y Collision
        self.y += y_offset
        self.rect.y += y_offset
        collision_sprites = pygame.sprite.spritecollide(self, group, False)
        self.landed = False
        for sprite in collision_sprites:
            if abs(self.rect.x - sprite.rect.x) == 50:
                continue

            if sprite.dmg and self.iframes == 0:
                self.HP -= sprite.dmg
                self.iframes = 60

            self.vy = 0
            if (self.rect.bottom >= sprite.rect.top and
                    self.rect.top < sprite.rect.top):
                self.rect.bottom = sprite.rect.top
                self.y = sprite.y - sprite.rect.height
                self.landed = True
            else:
                self.rect.top = sprite.rect.bottom
                self.y = sprite.y + sprite.rect.height

    def jump(self):
        if not self.landed:
            return

        self.vy = -250


class Block(pygame.sprite.Sprite):
    def __init__(self, image, coordinates, dmg=0):
        super().__init__()

        self.image = image

        self.x, self.y = coordinates
        self.dmg = dmg

        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates


class Camera():
    def __init__(self):
        self.sprites = []
        self.x = 200
        self.y = 100
        self.rect = pygame.Rect(200, 100, 400, 200)

    def add(self, sprite):
        self.sprites.append(sprite)

    def update(self, target):
        x_offset = target.rect.centerx - 400
        y_offset = 0
        if self.x <= 200 and x_offset < 0:
            x_offset = 0

        self.x += x_offset
        self.y += y_offset
        for sprite in self.sprites:
            sprite.rect.x -= x_offset
            sprite.rect.y -= y_offset


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
    heart = pygame.image.load(
        'graphics/sprites/icons/heart.png').convert_alpha()
    grass = pygame.image.load('graphics/sprites/platforms/grass.png').convert()
    dirt = pygame.image.load('graphics/sprites/platforms/dirt.png').convert()
    spike = pygame.image.load(
        'graphics/sprites/obstacles/spike.png').convert_alpha()

    sky_bg = pygame.image.load('graphics/sprites/background/sky.png').convert()

    character_idle = pygame.image.load(
        'graphics/sprites/character/idle.png'
        ).convert()
    character_runR = [
        pygame.image.load('graphics/sprites/character/runR_1.png').convert(),
        pygame.image.load('graphics/sprites/character/runR_2.png').convert()
    ]
    character_runL = [
        pygame.image.load('graphics/sprites/character/runL_1.png').convert(),
        pygame.image.load('graphics/sprites/character/runL_2.png').convert()
    ]

    character_sprites = [
        *character_runL,
        character_idle,
        *character_runR
    ]



    # Level
    map = {
        grass: (
            (0, 300),
            (50, 350),
            (100, 250),
            (100, 350),
            (150, 350),
            (200, 350),
            (250, 350),
            (300, 200),
            (300, 350),
            (350, 150),
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
        ),
        spike: (
            (750, 325),
        )
        }

    block_dmg = {
        spike: 1,
        grass: 0,
        dirt: 0
    }

    spawnpoint = ((375, 200))

    player = Character(
        spawnpoint,
        character_sprites
        )

    camera = Camera()

    player_group = pygame.sprite.GroupSingle(player)
    camera.add(player)

    static_objects = pygame.sprite.Group()

    for tile, positions in map.items():
        for coord in positions:
            new_block = Block(tile, coord, block_dmg[tile])
            camera.add(new_block)
            static_objects.add(new_block)

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
        if player.HP == 0:
            continue

        screen.blit(sky_bg, (0, 0))

        player.update(clock.tick(FPS)/1000, pressed_keys, static_objects)
        if player.HP == 0:
            player.x, player.y = spawnpoint
            player.rect.topleft = spawnpoint
            player.landed = False
            camera.x = 200
            player.HP = 3
            for sprite in camera.sprites:
                if sprite != player:
                    sprite.rect.x, sprite.rect.y = sprite.x, sprite.y

        camera.update(player)

        if not player.iframes % 2:
            player_group.draw(screen)
        static_objects.draw(screen)

        for i in range(player.HP):
            screen.blit(heart, (15+25*i, 15))

        pygame.display.update()


if __name__ == "__main__":
    main()
