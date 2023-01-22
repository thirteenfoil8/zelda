import pygame
from zelda.config.settings import TILESIZE, magic_data
from zelda.entity.player.player import Player
from random import randint


class Magic(pygame.sprite.Sprite):
    def __init__(self, player: Player, animation_player, groups) -> None:
        super().__init__(groups)
        self.visible_sprites = groups[0]
        self.attack_sprites = groups[1]
        self.sprite_type = 'magic'
        self.player = player
        self.magic = magic_data[self.player.magic]
        self.style = self.player.magic
        self.strength = self.magic["strength"]
        self.cost = self.magic["cost"]
        self.image = pygame.image.load(magic_data[
            self.player.magic]['graphic']).convert_alpha()
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(
            midleft=self.player.rect.midright + pygame.math.Vector2(0, TILESIZE/4))
        self.direction = self.get_magic_direction()
        self.animation_player = animation_player

    def get_magic_direction(self):
        if self.player.status.split('_')[0] == "right":
            direction = pygame.math.Vector2(1, 0)

        elif self.player.status.split('_')[0] == "left":
            direction = pygame.math.Vector2(-1, 0)

        elif self.player.status.split('_')[0] == "up":
            direction = pygame.math.Vector2(0, -1)

        else:
            direction = pygame.math.Vector2(0, 1)
        return direction

    def heal(self):
        if self.player.energy >= self.cost:
            if self.player.health + self.strength > self.player.stats['health']:
                self.player.health = self.player.stats['health']
            else:
                self.player.health += self.strength
            self.player.energy -= self.cost
            self.animation_player.create_particles(
                'aura', self.player.rect.center, self.visible_sprites)
            self.animation_player.create_particles(
                'heal', self.player.rect.center + pygame.math.Vector2(0, -60), self.visible_sprites)

    def spell(self, spell_type):
        if self.player.energy >= self.cost:
            self.player.energy -= self.cost
        self.display_magic(spell_type)           
    
    def display_magic(self, spell_type):
        for tile in range(1, 6):
                if self.direction.x:
                    offset_x = self.direction.x * tile * TILESIZE
                    x = self.player.rect.centerx + offset_x + \
                        randint(-TILESIZE // 3, TILESIZE//3)
                    y = self.player.rect.centery + \
                        randint(-TILESIZE // 3, TILESIZE//3)
                    self.animation_player.create_particles(
                        spell_type, (x, y), [self.visible_sprites, self.attack_sprites])
                else:
                    offset_y = self.direction.y * tile * TILESIZE
                    x = self.player.rect.centerx + \
                        randint(-TILESIZE // 3, TILESIZE//3)
                    y = self.player.rect.centery + offset_y + \
                        randint(-TILESIZE // 3, TILESIZE//3)
                    self.animation_player.create_particles(
                        spell_type, (x, y), [self.visible_sprites, self.attack_sprites])
                    pass

    def cast(self):
        if self.style == 'heal':
            self.heal()
        elif self.style == 'flame':
            self.spell('flame')
