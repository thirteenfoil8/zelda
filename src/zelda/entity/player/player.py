import pygame
from zelda.utils.support import import_folder
from zelda.config.settings import weapon_data, magic_data
from zelda.entity.entity import Entity

IMAGE_PATH = 'src/zelda/assets/graphics/test/player.png'


class Player(Entity):
    def __init__(self, pos, groups, obstacles_sprites, create_attack, destroy_weapon, create_magic, destroy_magic):
        super().__init__(groups)
        self.image = pygame.image.load(IMAGE_PATH).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        # graphics setup
        self.import_player_assets()
        self.status = 'down'

        # attack
        self.create_attack = create_attack
        self.destroy_weapon = destroy_weapon
        self.attacking = False
        self.attack_cooldown = 200
        self.attack_time = None
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # Magic
        self.create_magic = create_magic
        self.destroy_magic = destroy_magic
        self.magic_attacking = False
        self.magic_time = None
        self.magic_cooldown = 200
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # Defense
        self.vulnerable = True
        self.hurt_time = None
        self.invincibility_duration = 500

        # Stats
        self.stats = {'health': 100, 'energy': 60,
                      'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140,
                          'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100,
                             'attack': 100, 'magic': 100, 'speed': 100}

        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 0
        self.speed = self.stats['speed']

        self.obstacle_sprites = obstacles_sprites

    def input(self):
        if not self.attacking and not self.magic_attacking:
            keys = pygame.key.get_pressed()
            # movement
            self.movement_input(keys=keys)
            # action
            self.action_input(keys=keys)

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status and 'attack' not in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def import_player_assets(self):
        character_path = 'src/zelda/assets/graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def movement_input(self, keys):
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

    def action_input(self, keys):
        if keys[pygame.K_SPACE]:
            self.attack_time = pygame.time.get_ticks()
            self.attacking = True
            self.create_attack()
        if keys[pygame.K_LSHIFT]:
            self.magic_time = pygame.time.get_ticks()
            self.magic_attacking = True
            self.create_magic()
        if keys[pygame.K_q] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            self.weapon_index += 1
            if self.weapon_index > len(weapon_data)-1:
                self.weapon_index = 0

            self.weapon = list(weapon_data.keys())[self.weapon_index]

        if keys[pygame.K_e] and self.can_switch_magic:
            self.can_switch_magic = False
            self.magic_switch_time = pygame.time.get_ticks()
            self.magic_index += 1
            if self.magic_index > len(magic_data)-1:
                self.magic_index = 0

            self.magic = list(magic_data.keys())[self.magic_index]

    def get_full_weapon_damage(self):
        return self.stats['attack'] + weapon_data[self.weapon]['damage']

    def get_full_magic_damage(self):
        return self.stats['magic'] + magic_data[self.magic]['strength']
    
    def energy_recovery(self):
        if self.energy <= self.stats["energy"]:
            self.energy += 0.01 * self.stats["magic"]
        else:
            self.energy = self.stats["energy"]

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_weapon()

        if self.magic_attacking:
            if current_time - self.magic_time >= self.magic_cooldown:
                self.magic_attacking = False
                self.destroy_magic()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.vulnerable = True

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move()
        self.energy_recovery()
