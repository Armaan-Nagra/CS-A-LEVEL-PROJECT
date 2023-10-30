import pygame
from settings import *
import random

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
        self.stop1 = None
        self.stop2 = None
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
        if self.stops == 1:
            self.stop1 = random.randint(100,800)
            self.stops = 0
        if self.stops == 2:
            self.stop1 = random.randint(100,300)
            self.stop2 = random.randint(400,800)
            self.stops = 0
        self.stop_move(gd)

    def stop_move(self,gd):
        if self.stop2 == None:
            if ((self.stop1 - 1) <= self.x <= (self.stop1 + 1)):
                stop_time = pygame.time.get_ticks()
                if stop_time <= 5000: 
                    self.shoot(gd)
                else:
                    self.move(gd)
                print(stop_time)
            else:
                self.move(gd)
        if self.stop2 != None:
            if ((self.stop1 - 1) <= self.x <= (self.stop1 + 1)):
                stop1_time = pygame.time.get_ticks()
                print(stop1_time)
                if stop1_time <= 5000: 
                    self.shoot(gd)
                else:
                    self.move(gd)
            if ((self.stop2 - 1) <= self.x <= (self.stop2 + 1)):
                stop2_time = pygame.time.get_ticks()
                print(stop2_time)
                if stop2_time <= 5000: 
                    self.shoot(gd)
                else:
                    self.move(gd)
            else:
                self.move(gd)

            

        
    
