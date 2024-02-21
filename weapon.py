import pygame
import time
from functions import *
from settings import *

class weapon(pygame.sprite.Sprite):
    def __init__(self,gtype,gbullets,gdelay,gsound):
        self.type = gtype
        self.shot_delay = gdelay
        self.last_shot = 0
        self.bullets = gbullets
        self.uzi_damage = 100
        self.more_damage_active = False
        self.current_bullets = 0
        self.font_colour = black
        self.sound = gsound

    def draw_hitbox(self,gd,colour,w,h):
        pygame.mouse.set_visible(False)
        pygame.draw.rect(gd,colour, [self.x + 8, self.y - (w/2) ,h,w])
        pygame.draw.rect(gd,colour, [self.x - 8 - h, self.y - (w/2) ,h,w])
        pygame.draw.rect(gd,colour, [self.x - (w/2), self.y + 8 ,w,h])
        pygame.draw.rect(gd,colour, [self.x - (w/2), self.y - 8 -h,w,h])

    def check_collision(self, sprite_group):
        #iterate through each sprite object in the group
        if self.more_damage_active == True:
            self.current_bullets = self.bullets
            self.bullets += 15
            self.uzi_damage = 250
            self.more_damage_active = False
        if self.bullets <= self.current_bullets:
            self.uzi_damage = 100
            self.font_colour = black
            self.sound = gunshot_sound

        for x in sprite_group:
            if x.rect.collidepoint(self.pos) and self.type == "uzi":
                x.change_health(self.uzi_damage)

            if self.type == "grenade" and x.rect.colliderect(self.rect):
                x.change_health(500)

        
    def shoot_effects(self,event,visual,gd,x,y,ex,ey,sprite_group):
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
                self.sound.play()
                gd.blit(visual,(self.ex,self.ey))
                self.bullets -= 1
                for x in sprite_group:
                    self.check_collision(x)
                self.last_shot = pygame.time.get_ticks()


    def display_HUD(self,image,gd,ix,iy,bx,by):
        gd.blit(image,(ix,iy))
        display_text(self.font_colour,bx,by,str(self.bullets),level_font)
    
    def change_bullets(self,amount):
        self.bullets += amount

    def more_damage(self,font_colour,sound):
        self.more_damage_active = True
        self.font_colour = font_colour
        self.sound = sound
    
    def reset_weapon(self):
        self.current_bullets = 0
        if self.type == "uzi":
            self.bullets = 100
            self.uzi_damage = 100
            self.font_colour = black
            self.sound = gunshot_sound
        if self.type == "grenade":
            self.bullets = 5
            self.sound = grenade_sound
        self.last_shot = 0
        self.more_damage_active = False
            




                
