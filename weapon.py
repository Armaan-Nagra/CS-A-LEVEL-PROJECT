import pygame
from settings import *
import time
from functions import *

class weapon():
    def __init__(self,gtype,gbullets,gdelay):
        self.type = gtype
        self.shot_delay = gdelay
        self.last_shot = 0
        self.bullets = gbullets

        

    def draw_hitbox(self,gd,colour):
        pygame.mouse.set_visible(False)
        pygame.draw.rect(gd,colour, [self.x + 6, self.y ,5,2])
        pygame.draw.rect(gd,colour, [self.x - 8, self.y ,5,2])
        pygame.draw.rect(gd,colour, [self.x, self.y + 6 ,2,5])
        pygame.draw.rect(gd,colour, [self.x , self.y - 8 ,2,5])


        
    def shoot_effects(self,event,sound,visual,gd,x,y):
        self.x = x
        self.y = y
        if event == 1 and self.bullets > 0:
            now = pygame.time.get_ticks()
            if now - self.last_shot >= self.shot_delay:
                sound.play()
                gd.blit(visual,(self.x,self.y))
                self.bullets -= 1
                
                self.last_shot = pygame.time.get_ticks()
            

    def display_HUD(self,image,gd,ix,iy,bx,by):
        gd.blit(image,(ix,iy))
        display_text(black,bx,by,str(self.bullets),level_font)
        
            




                
