import pygame
from Config import *



class InitMenu:
    def __init__(self, user):
        self.run = True
        self.image = pygame.image.load("Image/init_menu.png")
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        '''
        self.image = pygame.image.load("Image/menu_add0.png")
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH-300, SCREEN_HEIGHT-400))
        '''
        self.user = user

    def draw(self, surface):
        
        # (1)---畫出初起畫面有的文字、圖片---
        surface.blit(self.image,(0,0))
        self.draw_text(surface,"瘋 狂 外 送", 82, RED, True, SCREEN_WIDTH/2, 250)
        self.draw_text(surface,"按 P 開 始 送 餐", 32, BLACK, True, SCREEN_WIDTH/2, 350)
        self.draw_text(surface,f"- 訂 單 {self.user.level} -", 28, WHITE, True, SCREEN_WIDTH/2, 560) 
        self.draw_text(surface, f"預 估 交 保 金 額 : {self.user.money}萬", 24, WHITE, True, 160, 50)
        #self.draw_text(surface, f"{str(s).zfill(5)}", 24, WHITE, False, 50, 35)
        #surface.blit(pygame.transform.scale(pygame.image.load(f"Image/level{self.user.level}.jpg"),(SCREEN_WIDTH, SCREEN_HEIGHT)))
        #surface.blit(pygame.transform.scale(pygame.image.load(f"Image/level{self.user.level}.jpg"), (300,150)),(325-150,600))

        pass

    def draw_text(self, surface, text, size, color, bold, x, y):
        font = pygame.font.Font("Font/BoutiqueBitmap9x9_Bold_1.9.ttf", size=size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surface.blit(text_surface, text_rect)