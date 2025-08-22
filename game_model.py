import pygame
import random
import Glo
from Config import *
from LevelConfig import LEVELS
from background import Background
from spaceship import Spaceship
from enemy_factory import EnemyFactory
from animation import Explosion, Heal
from progress import Progress
from boss import Boss1, Boss2, Boss3
from power import Power

EnemyFactory.load_images()

class GameModel:
    def __init__(self, user):
        self.user = user
        self.level = user.level
        self.config = LEVELS[user.level]

        self.background = Background(self.config["background"], 10 * Glo.SPEED_RATE)
        self.spaceship_group = pygame.sprite.GroupSingle(Spaceship())
        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.animation_group = pygame.sprite.Group()
        self.boss_group = pygame.sprite.GroupSingle()
        self.power_group = pygame.sprite.Group()
        
        self.mileage_group = pygame.sprite.Group()           #新增2項
        self.mile_ctr = 0
        

        self.enemy_generator_time = 0
        self.enemy_generator_delay = random.randint(*self.config["enemy_delay"])

        self.run = False
        self.wait = False
        self.is_pass = False

        self.money = 0
        self.game_time = 0
        self.start_time = pygame.time.get_ticks()
        self.boss_time = self.config["boss_time"]
        self.progress = Progress(SCREEN_WIDTH - 50, 60, self.game_time, self.boss_time)
        self.power_probability = 0.8

    # ------------------ 更新邏輯 ------------------
    def update(self):
        self.check_for_state()
        self.background.update()
        self.spaceship_group.update()
        self.enemy_group.update()
        self.enemy_bullet_group.update()
        self.animation_group.update()
        self.boss_group.update()
        self.power_group.update()
        
        self.mileage_group .update()    #新增

        self.game_time = pygame.time.get_ticks() - self.start_time
        self.progress.update(self.game_time)

        self.enemy_generator()
        self.check_for_collisions()
        #self.check_for_state()
        self.boss_appear()

    def enemy_generator(self):
        now = pygame.time.get_ticks()
        if now - self.enemy_generator_time > self.enemy_generator_delay/Glo.SPEED_RATE:
            enemy_type = random.choice(self.config["enemies"])
            if enemy_type == "enemy1":
                enemy = EnemyFactory.create(enemy_type, random.choice([i for i in range(150, SCREEN_WIDTH-150) if not 300 <= i <= 350]), 0, self.enemy_bullet_group)
            elif enemy_type == "enemy2":
                enemy = EnemyFactory.create(enemy_type, random.choice([i for i in range(0, SCREEN_WIDTH) if not 150 <= i <= 500]), 0, self.enemy_bullet_group)
            self.enemy_group.add(enemy)
            enemy_type = "mileage"
            if enemy_type == "mileage":
                enemy = EnemyFactory.create(enemy_type, SCREEN_WIDTH-160, 0, self.enemy_bullet_group)
                self.mileage_group.add(enemy)
                print("lamp")
            self.enemy_generator_time = now
            self.enemy_generator_delay = random.randint(*self.config["enemy_delay"])

    def check_for_collisions(self):
        ship = self.spaceship_group.sprite
        # Spaceship 子彈
        for bullet in getattr(ship, "bullet_group", []):
            enemies_hit = pygame.sprite.spritecollide(bullet, self.enemy_group, True)
            for enemy in enemies_hit:
                self.money += enemy.value
                bullet.kill()
                self.animation_group.add(Explosion(enemy.rect.centerx, enemy.rect.centery, 50))
                if self.power_probability >= random.random():
                    self.power_group.add(Power(enemy.rect.centerx, enemy.rect.centery))

            bosses_hit = pygame.sprite.spritecollide(bullet, self.boss_group, False)
            for boss in bosses_hit:
                boss.hp -= bullet.damage
                bullet.kill()
                self.animation_group.add(
                    Explosion(boss.rect.centerx + random.randint(-60, 60),
                              boss.rect.centery + random.randint(-60, 60), 150)
                )

        # Enemy 與子彈
        for enemy in self.enemy_group.sprites():
            if pygame.sprite.spritecollide(enemy, self.spaceship_group, False):
                enemy.kill()
                ship.lives -= 1
                self.animation_group.add(Explosion(ship.rect.centerx, ship.rect.centery, 70))
                self.animation_group.add(Explosion(enemy.rect.centerx, enemy.rect.centery, 50))
            for bullet in enemy.bullet_group:
                if pygame.sprite.spritecollide(bullet, self.spaceship_group, False):
                    bullet.kill()
                    self.animation_group.add(Explosion(ship.rect.centerx, ship.rect.centery, 70))
                    ship.lives -= 1

        # Boss 子彈
        for bullet in getattr(self.boss_group.sprite, "bullet_group", []):
            if pygame.sprite.spritecollide(bullet, self.spaceship_group, False):
                bullet.kill()
                self.animation_group.add(Explosion(ship.rect.centerx, ship.rect.centery, 70))
                ship.lives -= 1

        # Power
        for power in self.power_group.sprites():
            '''
            if pygame.sprite.spritecollide(power, self.spaceship_group, False):
                ship.apply_power(power)
                if power.type == "heal":
                    self.animation_group.add(Heal(ship.rect.centerx, ship.rect.centery, 100))
                power.kill()
                '''
            pass
                
        
                

    def check_for_state(self):
        ship = self.spaceship_group.sprite
        if ship.lives <= 0:
            self.game_over()

        boss = self.boss_group.sprite
        if (boss and boss.hp <= 0):
            self.money += boss.value
            boss.kill()
            self.game_pass()
            
        for mileage in self.mileage_group.sprites():
            if mileage.rect.top > SCREEN_HEIGHT-30:
                mileage.kill()
                self.mile_ctr += 1
                print(self.mile_ctr)
                print(self.config["dest_mileage"])   
                if self.mile_ctr >= self.config["dest_mileage"]:
                    self.game_pass()
        

    def boss_appear(self):
        if self.game_time >= self.boss_time and not self.boss_group:
            boss_class = globals()[self.config["boss"]]
            self.boss_group.add(boss_class(SCREEN_WIDTH / 2, 0))

    # ------------------ 控制方法 ------------------
    def reset(self):
        self.run = True
        self.wait = False
        self.is_pass = False
        self.spaceship_group.sprite.reset()
        self.enemy_group.empty()
        self.enemy_bullet_group.empty()
        self.boss_group.empty()
        self.animation_group.empty()
        self.power_group.empty()
        self.money = 0
        self.start_time = pygame.time.get_ticks()
        self.mileage_group.empty()
        

    def game_over(self):
        self.run = False
        self.wait = True
        self.user.money += self.money

    def game_pass(self):
        self.run = False
        self.wait = True
        self.is_pass = True
        self.user.money += self.money
        
        ###
        self.user.level_up()


    def play_BGM(self):
        pygame.mixer.init()
        pygame.mixer.music.load("Sound/bg_music.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)
