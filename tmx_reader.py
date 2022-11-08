import pytmx
import pygame

map = pytmx.TiledMap('Levels/Level_1/map.tmx')


def get_properties(map):
    d = dict()
    for property in map.properties:
        d[property.name] = property.value
    return d


def get_tilesets(map):
    for tileset in map.tilesets:
        pass


class Tileset:
    def __init__(self, tileset) -> None:
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

    def __getitem__(self, id):
        try:
            return self.images[id]
        except KeyError:
            return


def display_tileset(screen, tileset, y):
    for i in range(tileset.tilecount):
        screen.blit(tileset[i], (i*64, y))


def main() -> None:
    pygame.init()

    # General
    screen = pygame.display.set_mode((1024, 512))
    pygame.display.set_caption('Game')

    clock = pygame.time.Clock()
    FPS = 60
    pressed_keys = set()

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

        screen.fill((255, 255, 255))

        # for i in range(len(map.tilesets)):
        #     display_tileset(screen, Tileset(map.tilesets[i]), i*64)

        clock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    print(map.layers)
    print('\n', map.layers, sep='')
