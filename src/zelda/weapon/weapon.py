import pygame
from zelda.config.settings import TILESIZE, weapon_data


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups) -> None:
        super().__init__(groups)
        direction = player.status.split("_")[0]
        self.player = player

        # graphics
        self.image = pygame.image.load(weapon_data[
                                self.player.weapon]['graphic'].replace('full', direction)).convert_alpha()
        self.get_weapon_direction(direction)
 
    def get_weapon_direction(self, direction):
        if direction == "right":
            self.rect = self.image.get_rect(
                midleft=self.player.rect.midright + pygame.math.Vector2(0, TILESIZE/4))

        elif direction == "left":
            self.rect = self.image.get_rect(
                midright=self.player.rect.midleft + pygame.math.Vector2(0, TILESIZE/4))

        elif direction == "up":
            self.rect = self.image.get_rect(
                midbottom=self.player.rect.midtop + pygame.math.Vector2(-TILESIZE/4, 0))

        elif direction == "down":
            self.rect = self.image.get_rect(
                midtop=self.player.rect.midbottom + pygame.math.Vector2(-TILESIZE/4, 0))
