import pygame
from bullet import Bullet
from BulletConfig import BULLET_CONFIG

class BulletFactory:
    bullet_images = {}

    @staticmethod
    def load_images():
        BulletFactory.bullet_images = {
            "spaceship": [pygame.transform.scale(
                pygame.image.load(f"Image/bullet/spaceship_bullet/bullet{i}.png"), (10, 30)) for i in range(2)],
            "enemy1": pygame.transform.scale(
                pygame.image.load("Image/bullet/enemy_bullet/bullet.png"), (6, 16)),
            "enemy2": pygame.transform.scale(
                pygame.image.load("Image/bullet/enemy_bullet/bullet2.png"), (8, 45)),
            "boss1": pygame.transform.scale(
                pygame.image.load("Image/bullet/enemy_bullet/bullet.png"), (20, 35)),
            "boss2": pygame.transform.scale(
                pygame.image.load("Image/bullet/enemy_bullet/bullet2.png"), (25, 160)),
            "boss2-1": pygame.transform.scale(
                pygame.image.load("Image/bullet/enemy_bullet/bullet2.png"), (20, 20)), 
            "boss3": pygame.transform.scale(
                pygame.image.load("Image/bullet/enemy_bullet/bullet3.png"), (40, 60)), 
            "boss3-1": pygame.transform.scale(
                pygame.image.load("Image/bullet/enemy_bullet/bullet3-1.png"), (70, 70)), 
            
        }

    @staticmethod
    def create(bullet_type, x, y, speedx_override=None, speedy_override=None):
        cfg = BULLET_CONFIG[bullet_type]

        if speedx_override is not None:
            cfg["speedx"] = speedx_override
        if speedy_override is not None:
            cfg["speedy"] = speedy_override

        bullet = Bullet(x, y, cfg["speedx"], cfg["speedy"], cfg["damage"])

        if cfg.get("animation", False):
            bullet.animation = BulletFactory.bullet_images["spaceship"]
            bullet.image = bullet.animation[0]
            bullet.rect = bullet.image.get_rect(center=(bullet.x, bullet.y))
            bullet.is_animation = True
        else:
            bullet.image = BulletFactory.bullet_images[bullet_type]
            bullet.rect = bullet.image.get_rect(center=(bullet.x, bullet.y))
            bullet.is_animation = False

        return bullet
