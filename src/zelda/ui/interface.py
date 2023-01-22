import pygame
from zelda.config.settings import UI_FONT, UI_FONT_SIZE, HEALTH_BAR_WIDTH, HEALTH_COLOR, BAR_HEIGHT, TEXT_COLOR
from zelda.config.settings import ENERGY_BAR_WIDTH, ENERGY_COLOR, ITEM_BOX_SIZE, UI_BG_COLOR, UI_BORDER_COLOR
from zelda.config.settings import UI_BORDER_COLOR_ACTIVE, weapon_data, magic_data


class UI:
    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(
            10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing bars
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface,
                         UI_BORDER_COLOR, bg_rect, 3)

    def selection_box(self, left, top, has_switch):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switch:
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, player):
        bg_rect = self.selection_box(16, 630, not player.can_switch_weapon)
        weapon_surf = pygame.image.load(weapon_data[
            player.weapon]['graphic']).convert_alpha()
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, player):
        bg_rect = self.selection_box(
            16 + ITEM_BOX_SIZE, 630, not player.can_switch_magic)
        magic_surf = pygame.image.load(magic_data[
            player.magic]['graphic']).convert_alpha()
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         text_rect.inflate(20, 20), 3)

    def display(self, player):
        self.show_bar(
            player.health, player.stats["health"], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(
            player.energy, player.stats["energy"], self.energy_bar_rect, ENERGY_COLOR)

        self.weapon_overlay(player)
        self.magic_overlay(player)

        self.show_exp(player.exp)
