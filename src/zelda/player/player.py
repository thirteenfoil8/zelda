import pygame
from zelda.utils.support import import_folder

IMAGE_PATH = 'src/zelda/assets/graphics/test/player.png'


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(IMAGE_PATH).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        # graphics setup
        self.import_player_assets()

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5

        # attack
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        # Stats
        self.stats = {'health': 100, 'energy': 60,
                      'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140,
                          'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100,
                             'attack': 100, 'magic': 100, 'speed': 100}

        self.obstacle_sprites = obstacles_sprites

    def import_player_assets(self):
        character_path = 'src/zelda/assets/graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'top_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        print(self.animations)

    def input(self):

        keys = pygame.key.get_pressed()
        # movement
        self.movement_input(keys=keys)
        # action
        self.action_input(keys=keys)

    def movement_input(self, keys):
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def action_input(self, keys):
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attack_time = pygame.time.get_ticks()
            self.attacking = True
            print('attack')
        if keys[pygame.K_LSHIFT] and not self.attacking:
            self.attack_time = pygame.time.get_ticks()
            self.attacking = True
            print('magic')

    def move(self, speed=5):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def update(self):
        self.input()
        self.cooldowns()
        self.move()
