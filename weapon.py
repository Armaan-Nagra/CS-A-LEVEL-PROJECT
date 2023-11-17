import pygame
from settings import *
import time
from functions import *

class weapon(pygame.sprite.Sprite):
    def __init__(self,gtype,gbullets,gdelay):
        self.type = gtype
        self.shot_delay = gdelay
        self.last_shot = 0
        self.bullets = gbullets
        

        

    def draw_hitbox(self,gd,colour,w,h):
        pygame.mouse.set_visible(False)
        pygame.draw.rect(gd,colour, [self.x + 8, self.y - (w/2) ,h,w])
        pygame.draw.rect(gd,colour, [self.x - 8 - h, self.y - (w/2) ,h,w])
        pygame.draw.rect(gd,colour, [self.x - (w/2), self.y + 8 ,w,h])
        pygame.draw.rect(gd,colour, [self.x - (w/2), self.y - 8 -h,w,h])


        
    def shoot_effects(self,event,sound,visual,gd,x,y,ex,ey,sprite_group):
        self.x = x
        self.y = y
        self.ex = ex
        self.ey = ey
        self.rect = visual.get_rect()
        if event == 1 and self.bullets > 0:
            now = pygame.time.get_ticks()
            if now - self.last_shot >= self.shot_delay:
                sound.play()
                gd.blit(visual,(self.ex,self.ey))
                self.bullets -= 1
                self.last_shot = pygame.time.get_ticks() 

                weapon_sprite = pygame.sprite.Sprite()
                weapon_sprite.rect = pygame.Rect(self.x, self.y, 100, 100)
                hits = pygame.sprite.spritecollide(weapon_sprite, sprite_group, True)
                for enemy_hit in hits:  
                    print(f"Hit detected at {weapon_sprite.rect.center} on enemy at {enemy_hit.rect.center}")
                    enemy_hit.kill()


    def display_HUD(self,image,gd,ix,iy,bx,by):
        gd.blit(image,(ix,iy))
        display_text(black,bx,by,str(self.bullets),level_font)
        
            




                
