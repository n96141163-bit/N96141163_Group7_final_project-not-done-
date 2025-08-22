import pygame
from enemy import Enemy


class EnemyFactory:
    enemy_images = {}

    @staticmethod
    def load_images():
        EnemyFactory.enemy_images = {
            "enemy1": [pygame.transform.scale(
                pygame.image.load(f"Image/enemy/enemy1/enemy{i}.png"), (60, 70)) for i in range(5)],
            
            "enemy2": [pygame.transform.scale(
                pygame.image.load(f"Image/enemy/enemy2/enemy{i}.png"), (40, 70)) for i in range(5)],
            
            "mileage": [pygame.transform.scale(
                pygame.image.load(f"Image/enemy/lamp0.png"), (50, 20))],
            
            }
          
          
                

    @staticmethod
    def create(enemy_type, x, y, bullet_group):
        if enemy_type == "enemy1":
            return Enemy(x, y, animation=EnemyFactory.enemy_images[enemy_type], 
                         bullet_group=bullet_group, bullet_type=enemy_type, value=100, speedy_range=(2, 3))
        elif enemy_type == "enemy2":
            return Enemy(x, y, animation=EnemyFactory.enemy_images[enemy_type], 
                         bullet_group=bullet_group, bullet_type=enemy_type, value=200, speedy_range=(8, 9))
        elif enemy_type == "mileage":
            return Enemy(x, y, animation=EnemyFactory.enemy_images[enemy_type], 
                         bullet_group=bullet_group, bullet_type=enemy_type, value=200, speedx_range=(0,0), speedy_range=(10, 10))