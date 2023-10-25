import pygame
from settings import *

class enemy(pygame.sprite.Sprite):
    def __init__(self,gx,gy,ghealth,gspritesheet,gstops,gdirection,gspeed,gcooldown):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.x = gx
        self.y = gy
        self.health = ghealth
        self.spritesheet = gspritesheet
        self.stops = gstops
        self.direction = gdirection
        self.offscreen = False
        self.last_time = pygame.time.get_ticks()
        self.cooldown = gcooldown
        if self.direction:
            self.speed = gspeed
        else:
            self.speed = gspeed * -1

    def move(self,gd):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= self.cooldown:
            self.frame += 1
            self.last_time = current_time
            if self.frame >= 2:
                self.frame = 0
        self.x += self.speed 
        if self.direction:
            gd.blit(pygame.transform.flip(self.spritesheet[self.frame],self.direction,False),(self.x,self.y))
        else:
            gd.blit(pygame.transform.flip(self.spritesheet[self.frame],False,False),(self.x,self.y))


    def shoot(self,gd):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= self.cooldown:
            self.last_time = current_time
            gd.blit(self.spritesheet[3],(self.x,self.y))
        else:
            gd.blit(self.spritesheet[2],(self.x,self.y))
 
    
    def update(self,gd):
        if self.x<= 500:
            self.move(gd)
        else:
            self.shoot(gd)
            
            

        
    
