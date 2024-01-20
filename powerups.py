import pygame
import random 
from settings import *

class powerups():
    def __init__(self,gplayer,gweapon):
        self.player = gplayer
        self.weapon = gweapon
        self.type = None 
        self.x = random.randint(800,1100)
        self.y = -100
        self.first = random.randint(30,40)
        self.second = random.randint(10,29) 
        self.third = random.randint(1,9) 
        self.powerups_list = [self.first,self.second,self.third]
        self.powerups_spritesheet = {
            "health": health_boost,
            "ammo": health_boost,
            "damage": health_boost
        }
        self.moving = False
        self.shot = False
        self.message_x = 0
        self.message_y = 0
        self.message_photo = None
        self.show_message = False
        self.opacity = 300
        self.size = None
    
    def update(self,soldiers,gd,x,y,left_click):
        for powerup in self.powerups_list:
            if powerup == soldiers and self.moving==False:
                self.type = random.choice(["health","ammo","damage"])
                self.powerups_list.remove(powerup)
                self.moving = True
        if self.moving:
            self.shot = False
            self.draw(self.type,gd)
            self.move() 
            self.check_collision(x,y,left_click)
        if self.show_message == True:
            self.visual_effect(self.message_x,self.message_y,self.gd,self.opacity)
            self.message_y-=0.5
            self.opacity -=1.5
            if self.opacity <= 5:
                self.show_message = False
            


    def draw(self,type,gd):
        self.gd = gd
        if self.type != None and self.shot == False:
            gd.blit(self.powerups_spritesheet[self.type],(self.x,self.y))



    def move(self):
        if self.y <= 300:
            self.y+=5
        if self.y >= 300:
            self.x -= scroll_speed
        if self.x <= -100:
            self.x = random.randint(800,1100)
            self.y = -100
            self.moving = False
    
    def check_collision(self,mouse_x,mouse_y,mouse_left):
        image_rect = self.powerups_spritesheet[self.type].get_rect()
        if mouse_left and self.shot == False:
            if mouse_x > self.x and mouse_x < self.x +100:
                if mouse_y > self.y and mouse_y < self.y +100:
                    self.use_power_up(self.gd)
                    self.shot = True
                    self.x = random.randint(800,1100)
                    self.y = -100
                    self.moving = False
    
    def use_power_up(self,gd):
        if self.type == "health":
            self.player.change_health(50)
            slurp.play()
            self.message_x = 0
            self.message_y = 25
            self.message_photo = hearts
            self.show_message = True
            self.size = (1000,200)

        if self.type == "ammo":
            self.weapon.change_bullets(20)
            chaching.play()
            self.message_x = 750
            self.message_y = 780
            self.message_photo = add_ammo
            self.show_message = True
            self.size = (100,100)

        if self.type == "damage":
            self.weapon.more_damage(red,machine_gun)
    
    def visual_effect(self,x,y,gd,opacity):
        temp = pygame.Surface(self.size).convert()
        temp.blit(gd, (-self.message_x, -self.message_y))
        temp.blit(self.message_photo, (0, 0))
        temp.set_alpha(opacity)        
        gd.blit(temp, (self.message_x,self.message_y))
        