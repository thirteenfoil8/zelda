import pygame
from zelda.config.settings import WORLD_MAP, TILESIZE
from zelda.level.tile import Tile
from zelda.player.player import Player
from zelda.camera.camera import YSortCameraGroup
from zelda.utils.support import import_csv_layout, import_folder
from random import choice


class Level:
    def __init__(self):

        # Display Surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # Sprite Setup
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('src/zelda/assets/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('src/zelda/assets/map/map_Grass.csv'),
            'object': import_csv_layout('src/zelda/assets/map/map_LargeObjects.csv')
        }
        graphics = {
            'grass': import_folder('src/zelda/assets/graphics/grass'),
            'object': import_folder('src/zelda/assets/graphics/objects')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            # Boundary tile
                            Tile(pos=(x, y), groups=[
                                 self.obstacles_sprites], sprite_type='invisible')
                        if style == "grass":
                            randow_grass_image = choice(graphics['grass'])
                            Tile(pos=(x, y), groups=[
                                 self.visible_sprites], sprite_type='grass', surface=randow_grass_image)
                        if style == "object":
                            # Object tile
                            randow_object_image = choice(graphics['object'])
                            Tile(pos=(x, y), groups=[
                                 self.visible_sprites, self.obstacles_sprites], sprite_type='object',
                                 surface=randow_object_image)

        self.player = Player(pos=(2000, 1400), groups=[
                             self.visible_sprites], obstacles_sprites=self.obstacles_sprites)

    def run(self):
        # Update and draw game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
