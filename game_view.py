import pygame
from Config import *

class GameView:
    def draw(self, model, surface):
        model.background.draw(surface)
        model.spaceship_group.draw(surface)
        model.spaceship_group.sprite.bullet_group.draw(surface)
        model.enemy_group.draw(surface)
        model.enemy_bullet_group.draw(surface)
        model.animation_group.draw(surface)
        model.boss_group.draw(surface)
        #model.power_group.draw(surface)
        model.progress.draw(surface)
        model.mileage_group.draw(surface)          #新增

        # Boss HP
        if model.boss_group:
            model.boss_group.sprite.draw_hp(surface)
            model.boss_group.sprite.bullet_group.draw(surface)

        # Text & Money & Lives
        if not model.run:
            if model.is_pass:
                self.draw_text(surface, "：「您 的 餐 點 到 囉 !」", 40, RED, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-80)
                self.draw_text(surface, ":「今 天 餐 好 像 特 別 早 到 ！ 」", 40, RED, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-40)
                self.draw_text(surface, "按 R 接 下 個 訂 單", 28, WHITE, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            else:
                self.draw_text(surface, ":「你 也 是 78 歲 ?」", 48, RED, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-80)
                self.draw_text(surface, "按 R 重啟", 28, WHITE, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            self.draw_text(surface, "Press Q to return the initial menu", 26, WHITE, False, SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50)

        self.draw_text(surface, "預 估 交 保 金 額", 24, WHITE, False, 100, SCREEN_HEIGHT-65)
        self.draw_text(surface, f"{str(model.money).zfill(5)}萬", 24, WHITE, False, 80, SCREEN_HEIGHT-40)
        self.draw_text(surface, f"訂 單 {model.user.level}", 24, WHITE, False, SCREEN_WIDTH-65, 0)

        for i in range(model.spaceship_group.sprite.lives):
            surface.blit(LIVES_ICON, (i*40+15, 10))

    def draw_text(self, surface, text, size, color, bold, x, y):
        font = pygame.font.Font("Font/BoutiqueBitmap9x9_Bold_1.9.ttf", size=size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surface.blit(text_surface, text_rect)
