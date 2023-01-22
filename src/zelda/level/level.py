import pygame
from zelda.config.settings import TILESIZE
from zelda.level.tile import Tile
from zelda.player.player import Player
from zelda.camera.camera import YSortCameraGroup
from zelda.utils.support import import_csv_layout, import_folder
from zelda.weapon.weapon import Weapon
from zelda.ui.interface import UI


class Level:
    def __init__(self):

        # Display Surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # User Interface
        self.ui = UI()

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
                            surface = self.select_object(
                                layout, col_index, row_index, graphics['grass'])
                            Tile(pos=(x, y), groups=[
                                 self.visible_sprites], sprite_type='grass', surface=surface)
                        if style == "object":
                            # Object tile
                            surface = self.select_object(
                                layout, col_index, row_index, graphics['object'])
                            Tile(pos=(x, y), groups=[
                                 self.visible_sprites, self.obstacles_sprites], sprite_type='object',
                                 surface=surface)

        self.player = Player(pos=(2000, 1400), groups=[self.visible_sprites],
                             obstacles_sprites=self.obstacles_sprites,
                             create_attack=self.create_attack, destroy_weapon=self.destroy_weapon)

    def create_attack(self):
        self.current_attack = Weapon(
            player=self.player, groups=[self.visible_sprites])

    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def select_object(self, layout, col_index, row_index, object):
        image_number = int(layout[row_index][col_index])
        if image_number > len(object):
            image_number = image_number % len(object)
        return object[image_number]

    def run(self):
        # Update and draw game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
        # debug(self.player.status)
