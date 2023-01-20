import pygame
from zelda.config.settings import WORLD_MAP, TILESIZE
from zelda.level.tile import Tile
from zelda.player.player import Player
from zelda.camera.camera import YSortCameraGroup
from zelda.utils.support import import_csv_layout


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
            'boundary': import_csv_layout('src/zelda/assets/map/map_FloorBlocks.csv')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(WORLD_MAP):
                for col_index, col in enumerate(row):
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                if style == "boundary":
                    Tile(pos=(x, y), groups=[
                         self.visible_sprites, self.obstacles_sprites],sprite_type='invisible')
        #         if col == "x":
        #             Tile(pos=(x, y), groups=[
        #                  self.visible_sprites, self.obstacles_sprites])
        #         if col == "p":
        #             self.player = Player(pos=(x, y), groups=[self.visible_sprites],
        #                                  obstacles_sprites=self.obstacles_sprites)
        self.player = Player(pos=(2000, 1430), groups=[
                             self.visible_sprites], obstacles_sprites=self.obstacles_sprites)

    def run(self):
        # Update and draw game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
