import tmx
import pygame

map = tmx.TileMap.load('Levels/Level_1/map.tmx')


def get_properties(map):
    d = dict()
    for property in map.properties:
        d[property.name] = property.value
    return d


def get_tilesets(map):
    for tileset in map.tilesets:
        


map_properties = get_properties(map)
get_tilesets(map)


print(map_properties)
