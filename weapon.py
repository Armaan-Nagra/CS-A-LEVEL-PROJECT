import pygame
import time
from functions import *
from settings import enemies_killed, enemies_left

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

    def check_collision(self, sprite_group):
        global enemies_killed
        global enemies_left
        for x in sprite_group:
            if x.rect.collidepoint(self.pos) and self.type == "uzi":
                x.kill()
                enemies_killed = enemies_killed + 1
                enemies_left = enemies_left - 1
            if self.type == "grenade" and x.rect.colliderect(self.rect):
                x.kill()
                enemies_killed = enemies_killed + 1

    def get_enemies_killed(self):
        return enemies_killed

    def get_enemies_left(self):
        return enemies_left

        
    def shoot_effects(self,event,sound,visual,gd,x,y,ex,ey,sprite_group):
        self.x = x
        self.y = y
        self.ex = ex
        self.ey = ey
        self.pos = (self.x, self.y)
        if self.type == "grenade":
            self.rect = visual.get_rect()
            self.rect.x = self.ex
            self.rect.y = self.ey 
        if event == 1 and self.bullets > 0:
            now = pygame.time.get_ticks()
            if now - self.last_shot >= self.shot_delay:
                sound.play()
                gd.blit(visual,(self.ex,self.ey))
                self.bullets -= 1
                self.check_collision(sprite_group)
                self.last_shot = pygame.time.get_ticks()


    def display_HUD(self,image,gd,ix,iy,bx,by):
        gd.blit(image,(ix,iy))
        display_text(black,bx,by,str(self.bullets),level_font)
        
            




                
