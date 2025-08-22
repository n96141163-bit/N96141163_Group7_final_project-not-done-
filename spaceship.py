import pygame

import Glo
from Config import *

from attack_strategy import NormalAttack, DoubleAttack, TripleAttack


spaceship_images = {
    "normal": pygame.transform.scale(
    pygame.image.load("Image/spaceship.png"), (90, 100)), 
    "double": pygame.transform.scale(
    pygame.image.load("Image/spaceship_double.png"), (90, 60)), 
    "triple": pygame.transform.scale(
    pygame.image.load("Image/spaceship_triple.png"), (90, 60))
    }


ATTACK_STRATEGY_MAP = {
    "normal": lambda: (NormalAttack(), spaceship_images["normal"]),
    "double_shoot": lambda: (DoubleAttack(), spaceship_images["double"]),
    "triple_shoot": lambda: (TripleAttack(), spaceship_images["triple"])
}


class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship_images["normal"]
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH/2, SCREEN_HEIGHT))
        self.lives = 10
        self.max_lives = 10
        self.speed = 10
        self.attack_strategy = NormalAttack()
        self.bullet_group = pygame.sprite.Group()
        self.bullet_ready = True
        self.bullet_time = 0
        self.bullet_delay = 400
        self.shoot_sound = pygame.mixer.Sound("Sound/shoot0.mp3")

    def get_user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_KP6]:
            self.rect.x += self.speed
        if keys[pygame.K_KP4]:
            self.rect.x -= self.speed
        if keys[pygame.K_KP8]:
            self.rect.y -= self.speed
        if keys[pygame.K_KP5]:
            self.rect.y += self.speed

        if keys[pygame.K_SPACE] and self.bullet_ready:
            self.bullet_ready = False
            self.shoot()
            self.bullet_time = pygame.time.get_ticks()
        if keys[pygame.K_KP0] and self.bullet_ready:
            self.bullet_ready = False
            Glo.SPEED_RATE += 0.2
            print(Glo.SPEED_RATE)
            self.bullet_time = pygame.time.get_ticks()
        if keys[pygame.K_KP_ENTER] and self.bullet_ready:
            self.bullet_ready = False
            if Glo.SPEED_RATE > 1:
                Glo.SPEED_RATE -= 0.2
            self.bullet_time = pygame.time.get_ticks()
            print(Glo.SPEED_RATE)
        
            

    def shoot(self):
        self.attack_strategy.shoot(self)


    def constrain_movement(self):
        if self.rect.right > SCREEN_WIDTH+30:
            self.rect.right = SCREEN_WIDTH+30
        if self.rect.left < -30:
            self.rect.left = -30
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def recharge_bullet(self):
        if not self.bullet_ready:
            now = pygame.time.get_ticks()
            if now - self.bullet_time >= self.bullet_delay:
                self.bullet_ready = True

    def apply_power(self, power):
        '''
        if power.type == "heal":
            self.lives = min(self.lives + 1, self.max_lives)
            return
        
        if power.type in ATTACK_STRATEGY_MAP:
            strategy, img = ATTACK_STRATEGY_MAP[power.type]()
            self.attack_strategy = strategy
            self.attack_strategy.activate()
            self.change_image(img)'''
        pass

    def check_status(self):
        if self.attack_strategy.is_expired():
            self.attack_strategy = NormalAttack()
            self.change_image(spaceship_images["normal"])

    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.bullet_group.update()
        self.recharge_bullet()
        self.check_status()

    def reset(self):
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH/2, SCREEN_HEIGHT))
        self.lives = self.max_lives
        self.bullet_group.empty()
        self.attack_strategy = NormalAttack()
        self.change_image(spaceship_images["normal"])


    def change_image(self, new_image):
        self.image = new_image


