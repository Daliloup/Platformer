import tmx
import pygame
from sys import exit

pygame.display.init()
screen = pygame.display.set_mode((1024, 512))

map = tmx.TileMap.load('Levels/Level_1/map.tmx')
t = map.tilesets[0]

tile_layer = map.layers[1]

for i, tile in enumerate(tile_layer.tiles):
    if not tile.gid:
        continue
    print(((i % 64)*64, (i//64-1)*64), tile.gid)


class Tileset:
    def __init__(self, tileset: tmx.Tileset):
        self.tileset_img = pygame.image.load(
            tileset.image.source
        ).convert_alpha()
        self.tiles = {}
        for i in range(tileset.tilecount):
            print(i)
            self.tiles[i] = self.tileset_img.subsurface(64*i, 0, 64, 64)


tileset = Tileset(t)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('white')
    for i in range(len(tileset.tiles)):
        screen.blit(tileset.tiles[i], (64*i, 0))

    pygame.display.update()
