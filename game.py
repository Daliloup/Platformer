import pygame
import pytmx
from sys import exit
from math import ceil


# Gravitational force
g = 270


class Level:
    def __init__(self,
                 screen: pygame.Surface,
                 map: pytmx.TiledMap,
                 spawnpoint: tuple[int]) -> None:

        self.screen = screen
        self.spawnpoint = spawnpoint
        self.bottom = 512

        # Loads the images
        self.background_img = pygame.image.load(
            map.properties['Background']
        ).convert()

        self.heart = pygame.image.load(
            'graphics/icons/heart.png'
        ).convert_alpha()

        # A list of all the tilesets used
        self.tilesets = [Tileset(i) for i in map.tilesets]

        # A list of layers to be drawn on the screen
        self.layers = []

        # Camera keeps the elements in field of view
        self.camera = Camera(
            0,
            0,
            map.width*map.tilewidth,
            map.height*map.tileheight
        )

        # Creates the pygame layers
        for layer in map.layers:
            if not isinstance(layer, pytmx.pytmx.TiledTileLayer):
                continue

            new_layer = pygame.sprite.Group()
            for tile in layer.tiles():
                tileset_pos = tile[2][1][0]//64
                coord = (tile[0]*32, tile[1]*32)
                new_layer.add(Tile(self.tilesets[0][tileset_pos], coord))

            self.layers.append(new_layer)

        # Initiates the player
        self.player = Character(
            self.spawnpoint,
            self.get_character_spritesheets()
        )

        # Creates a layer for the player
        self.player_layer = pygame.sprite.GroupSingle(self.player)
        self.layers.append(self.player_layer)

    def get_character_spritesheets(self) -> dict[str: 'Spritesheet']:
        character_spritesheets = {}
        character_spritesheets['running'] = Spritesheet(
            "graphics/sprites/character/running.png",
            2
        )
        character_spritesheets['idle'] = Spritesheet(
            "graphics/sprites/character/running.png",
            10
        )
        return character_spritesheets

    def update(self, dt: int, input: tuple):
        self.player.update(dt, input, self.layers[0])

        if self.player.rect.top > self.bottom:
            self.player.hp -= 1
            self.reinitialize(False)

        if self.player.hp == 0:
            self.reinitialize()

        self.camera.update(self.player, self.layers)
        self.screen.blit(self.background_img, (0, 0))
        for layer in self.layers:
            layer.draw(self.screen)

        for i in range(self.player.hp):
            self.screen.blit(self.heart, (15+25*i, 15))

    def reinitialize(self, heal=True):
        self.player.x, self.player.y = self.spawnpoint
        self.player.rect.topleft = self.spawnpoint

        self.player.landed = False
        self.camera.x = 0
        if heal:
            self.player.hp = 3
        for layer in self.layers:
            for sprite in layer:
                if sprite != self.player:
                    sprite.rect.x, sprite.rect.y = sprite.x, sprite.y


class Tileset:
    def __init__(self, tileset: pytmx.TiledTileset) -> None:
        tileset_img = pygame.image.load(
            'Levels/Level_1/' + tileset.source
        ).convert_alpha()
        self.images = []
        self.tilecount = tileset.tilecount
        self.firstgid = tileset.firstgid

        w = tileset.tilewidth
        h = tileset.tileheight
        for i in range(tileset.tilecount - tileset.columns + 1):
            for j in range(tileset.columns):
                self.images.append(tileset_img.subsurface(w*j, h*i, w, h))

    def __getitem__(self, id: int) -> 'Tile':
        try:
            return self.images[id]
        except IndexError:
            return


class Tile(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, coordinates: tuple[int], dmg=0):
        super().__init__()

        self.image = image

        # Absolute coordinates (in map)
        self.x, self.y = coordinates
        self.dmg = dmg

        # Relative coordinates (on screen)
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates


class Spritesheet():
    def __init__(self, source: str, keyframe: int) -> None:
        image = pygame.image.load(source)
        self.sprites = []

        for i in range(4):
            self.sprites.append(image.subsurface(32*i, 0, 32, 32))

        self.current = 0
        self.keyframe = keyframe

    def get_curr_sprite(self) -> pygame.Surface:
        return self.sprites[self.current]

    def next(self) -> None:
        if self.current < len(self.sprites) - 1:
            self.current += 1
        else:
            self.current = 0


class Character(pygame.sprite.Sprite):
    def __init__(self,
                 spawnpoint: tuple,
                 spritesheets: dict[str, Spritesheet]) -> None:

        # Initializes the sprite class
        super().__init__()

        # Animation Part
        self.state = 'idle'
        self.spritesheets = spritesheets
        self.spritesheet = spritesheets[self.state]
        self.image = self.spritesheet.get_curr_sprite()
        self.keyframe = 0

        # Rectangle (Hitbox)
        self.x, self.y = spawnpoint
        self.rect = self.image.get_rect()
        self.rect.topleft = spawnpoint

        # Velocity
        self.vx = 0
        self.vy = 0

        # Acceleration
        self.ax = 0
        self.ay = g

        # Parameters
        self.hp = 3
        self.iframes = 0  # Invincibility frames
        self.landed = True

    def update(self,
               dt: float,
               input: list,
               group: pygame.sprite.Group) -> None:

        self.keyframe += 1
        if self.keyframe == self.spritesheet.keyframe:
            self.spritesheet.next()
            self.image = self.spritesheet.get_curr_sprite()
            self.keyframe = 0

        # Input
        if self.landed and pygame.K_SPACE in input:
            self.jump()

        if pygame.K_d in input:
            self.vx = 200

        elif pygame.K_q in input:
            self.vx = -200

        else:
            self.vx = 0

        # State handler
        if self.landed and self.vx != 0:
            new_state = 'running'
        else:
            new_state = 'idle'

        if new_state != self.state:
            self.keyframe = 0
            self.state = new_state
            self.spritesheet = self.spritesheets[new_state]

        if self.iframes:
            self.iframes -= 1

        # Velocity
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        # Collisions
        dx = ceil(self.vx * dt)
        dy = ceil(self.vy * dt)

        # X collision
        self.x += dx
        self.rect.x += dx
        collision_sprites = pygame.sprite.spritecollide(self, group, False)
        for sprite in collision_sprites:
            if sprite == self:
                continue
            if (self.rect.bottom == sprite.rect.top and self.landed):
                continue

            if sprite.dmg and self.iframes == 0:
                self.hp -= sprite.dmg
                self.iframes = 60

            self.vx = 0
            if (self.rect.right >= sprite.rect.left) and \
               (self.rect.left < sprite.rect.left):
                self.rect.right = sprite.rect.left
                self.x = sprite.x - 50
            else:
                self.rect.left = sprite.rect.right
                self.x = sprite.x + sprite.rect.width

        # Y Collision
        self.y += dy
        self.rect.y += dy
        collision_sprites = pygame.sprite.spritecollide(self, group, False)
        self.landed = False
        for sprite in collision_sprites:
            if (abs(self.rect.x - sprite.rect.x) ==
                    self.rect.width//2 - sprite.rect.width//2):
                continue

            if sprite.dmg and self.iframes == 0:
                self.hp -= sprite.dmg
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

    def jump(self) -> None:
        if not self.landed:
            return

        self.vy = -250


class Camera():
    def __init__(self, xmin: int, ymin: int, xmax: int, ymax: int, x=0, y=0):
        self.xmin = xmin
        self.xmax = xmax

        self.ymin = ymin
        self.ymax = ymax

        self.x = x
        self.y = y

        self.rect = pygame.Rect(200, 100, 400, 200)

    def update(self,
               target: pygame.sprite.Sprite,
               layers: list[pytmx.TiledTileLayer]) -> None:

        dx = target.rect.centerx - 512
        dy = 0
        if (self.x <= self.xmin and dx < 0) or \
           (self.x+1024 >= self.xmax and dx > 0):
            dx = 0
        elif (self.y <= self.ymin and dy < 0) or \
             (self.y+512 >= self.ymax and dy > 0):
            dy = 0

        self.x += dx
        self.y += dy
        for layer in layers:
            for tile in layer:
                tile.rect.x -= dx
                tile.rect.y -= dy


def main() -> None:
    pygame.init()

    # General
    screen = pygame.display.set_mode((1024, 512))
    pygame.display.set_caption('Game')

    # Loads level
    level = Level(
        screen,
        pytmx.TiledMap('Levels/Level_1/map.tmx'),
        (512, 256)
    )

    clock = pygame.time.Clock()
    FPS = 60
    pressed_keys = set()

    while True:
        # Event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                pressed_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                pressed_keys.remove(event.key)

        level.update(clock.tick(FPS)/1000, pressed_keys)
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
    exit(0)
