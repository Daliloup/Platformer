import pygame
from sys import exit
from math import ceil, copysign

g = 190
a = [True]


class Character(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, coordinates: tuple, ):
        super().__init__()
        self.image = image

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
        self.is_landed = True

    def update(self, dt, group):

        self.vx += self.ax * dt
        self.vy += self.ay * dt

        # Collisions
        x_offset = ceil(self.vx * dt)
        y_offset = ceil(self.vy * dt)
        # X collision
        self.rect.x += x_offset

        collision_sprites = pygame.sprite.spritecollide(self, group, False)
        for sprite in collision_sprites:
            if self.rect.bottom == sprite.rect.top and self.is_landed:
                continue
            self.vx = 0
            if self.rect.right >= sprite.rect.left and self.rect.left < sprite.rect.left:
                self.rect.right = sprite.rect.left
            else:
                self.rect.left = sprite.rect.right

        # Y Collision
        self.rect.y += y_offset

        collision_sprites = pygame.sprite.spritecollide(self, group, False)
        self.is_landed = False
        for sprite in collision_sprites:
            if abs(self.rect.x - sprite.rect.x) == 50:
                continue
            self.vy = 0
            if self.rect.bottom >= sprite.rect.top and self.rect.top < sprite.rect.top:
                self.rect.bottom = sprite.rect.top
                self.is_landed = True
            else:
                self.rect.top = sprite.rect.bottom
                self.is_landed = False

    def jump(self):
        if not self.is_landed:
            return

        self.vy = -200


class Grass(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, coordinates):
        super().__init__()

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates


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
    # character_right = pygame.image.load(
    #     'graphics/sprites/character/right.png'
    #     ).convert()
    # character_left = pygame.image.load(
    #     'graphics/sprites/character/left.png'
    #     ).convert()

    map = {
        grass: (
            (0, 300),
            (0, 350),
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
            )
        }

    spawnpoint = ((375, 200))

    player = Character(
        character_idle,
        spawnpoint
        )

    player_group = pygame.sprite.GroupSingle()
    player_group.add(player)

    pressed_keys = [None]

    grass_group = pygame.sprite.Group()

    for tile, positions in map.items():
        for coord in positions:
            grass_group.add(Grass(grass, coord))

    while True:
        screen.blit(sky_bg, (0, 0))

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

        grass_group.draw(screen)

        player.update(clock.tick(60)/1000, grass_group)
        player_group.draw(screen)
 
        pygame.display.update()


if __name__ == "__main__":
    main()
