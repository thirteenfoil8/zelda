import pygame
from zelda.config.settings import TILESIZE, magic_data


class Magic(pygame.sprite.Sprite):
    def __init__(self, player, groups) -> None:
        super().__init__(groups)
        self.player = player
        self.magic = magic_data[self.player.magic]
        self.style = self.player.magic
        self.strength = self.magic["strength"]
        self.cost = self.magic["cost"]
        # graphics
        self.image = pygame.image.load(magic_data[
            self.player.magic]['graphic']).convert_alpha()
        self.rect = self.image.get_rect(
            midleft=self.player.rect.midright + pygame.math.Vector2(0, TILESIZE/4))
