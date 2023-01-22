import pygame
from zelda.config.settings import TILESIZE
from zelda.level.tile import Tile
from zelda.entity.player.player import Player
from zelda.entity.ennemy.ennemy import Enemy
from zelda.camera.camera import YSortCameraGroup
from zelda.utils.support import import_csv_layout, import_folder
from zelda.weapon.weapon import Weapon
from zelda.weapon.magic import Magic
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
        self.current_magic = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # User Interface
        self.ui = UI()

        # Sprite Setup
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('src/zelda/assets/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('src/zelda/assets/map/map_Grass.csv'),
            'object': import_csv_layout('src/zelda/assets/map/map_LargeObjects.csv'),
            'entities': import_csv_layout('src/zelda/assets/map/map_Entities.csv')
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
                                 self.visible_sprites, self.obstacles_sprites, self.attackable_sprites], sprite_type='grass', surface=surface)
                        if style == "object":
                            # Object tile
                            surface = self.select_object(
                                layout, col_index, row_index, graphics['object'])
                            Tile(pos=(x, y), groups=[
                                 self.visible_sprites, self.obstacles_sprites], sprite_type='object',
                                 surface=surface)
                        if style == "entities":
                            if col == '394':
                                self.player = Player(pos=(2000, 1400), groups=[self.visible_sprites],
                                                     obstacles_sprites=self.obstacles_sprites,
                                                     create_attack=self.create_attack, destroy_weapon=self.destroy_weapon,
                                                     create_magic=self.create_magic, destroy_magic=self.destroy_magic)
                            else:
                                monster_name = self.select_monster(
                                    layout, col_index, row_index)
                                Enemy(monster_name, (x, y), groups=[
                                      self.visible_sprites, self.attackable_sprites], obstacle_sprites=self.obstacles_sprites, damage_player=self.player_damage_logic)

    def create_attack(self):
        self.current_attack = Weapon(
            player=self.player, groups=[self.visible_sprites, self.attack_sprites])

    def create_magic(self):
        self.current_magic = (
            Magic(player=self.player, groups=[self.visible_sprites, self.attack_sprites]))
        self.current_magic.strength += self.player.stats['magic']

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprites in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprites, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprites in collision_sprites:
                        if target_sprites.sprite_type == 'grass':
                            target_sprites.kill()
                        else:
                            target_sprites.get_damage(
                                self.player, attack_sprites.sprite_type)

    def player_damage_logic(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particules

    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def destroy_magic(self):
        if self.current_magic:
            self.current_magic.kill()
        self.current_magic = None

    def select_object(self, layout, col_index, row_index, object):
        image_number = int(layout[row_index][col_index])
        if image_number > len(object):
            image_number = image_number % len(object)
        return object[image_number]

    def select_monster(self, layout, col_index, row_index):
        monster_number = layout[row_index][col_index]
        if monster_number == '390':
            monster_name = "bamboo"
        elif monster_number == '391':
            monster_name = "spirit"
        elif monster_number == '392':
            monster_name = "raccoon"
        else:
            monster_name = "squid"
        return monster_name

    def run(self):
        # Update and draw game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        # debug(self.player.status)
