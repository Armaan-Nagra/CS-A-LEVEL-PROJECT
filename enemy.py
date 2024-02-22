import pygame
from settings import *
import random
from settings import soldiers_killed, soldiers_left, tanks_left, tanks_shot


class enemy(pygame.sprite.Sprite):
    def __init__(self,gx,gy,ghealth,gspritesheet,gstops,gdirection,gspeed,gcooldown,gplayer,gtype,gw,gh,gdamage):
        pygame.sprite.Sprite.__init__(self)

        self.x = gx
        self.y = gy
        self.health = ghealth
        self.spritesheet = gspritesheet
        self.stops = gstops
        self.direction = gdirection
        if self.direction == 1:
            self.speed = gspeed
        if self.direction == 0:
            self.speed = gspeed * -1
        self.cooldown = gcooldown
        self.player = gplayer
        self.type = gtype
        self.w = gw
        self.h = gh
        self.damage = gdamage

        # self.offscreen = False
        self.moving = True

        self.stop1 = None
        self.stop2 = None
        self.stop1_time = None
        self.stop2_time = None        
        self.stop1_passed = False
        self.stop2_passed = False

        self.last_time = pygame.time.get_ticks()
        self.rect = self.spritesheet[0].get_rect()
        self.frame = 0
        self.rect.x = 0
        self.rect.y = 0
        

    def move(self,gd): #method responsible for moving enemy
        current_time = pygame.time.get_ticks()
        #checks if enough time has passed to move onto the next "movement" animation for the enemy
        if current_time - self.last_time >= self.cooldown:  #change the frame if enough time has passed
            self.frame += 1
            self.last_time = current_time
            if self.frame >= 2:
                self.frame = 0
        self.x += self.speed #change the x co-ordinate of the enemy respective to speed
        
        #draw the enemy in the right orientation, with the correct frame at the correct co-ordinate
        if self.direction == 1:
            gd.blit(pygame.transform.flip(self.spritesheet[self.frame],True ,False),(self.x,self.y))
        else:
            gd.blit(pygame.transform.flip(self.spritesheet[self.frame],False,False),(self.x,self.y))


    def shoot(self,gd):
        current_time = pygame.time.get_ticks()
        #display the "flashing" animation when shooting
        if current_time - self.last_time >= self.cooldown:
            self.last_time = current_time
            #if enemy moving from left to right
            if self.direction == 1:
                gd.blit(self.spritesheet[3],(self.x,self.y))
            #if enemy moving from right to left
            if self.direction == 0:
                gd.blit(pygame.transform.flip(self.spritesheet[3],True,False),(self.x,self.y))
            #decrease health of player
            self.player.change_health(self.damage)

        else:
            #display the "normal" shooting animation
            if self.direction == 1:
                gd.blit(self.spritesheet[2],(self.x,self.y))
            if self.direction == 0:
                gd.blit(pygame.transform.flip(self.spritesheet[2],True,False),(self.x,self.y))
 
    
    def update(self,gd):
        global tanks_left,tanks_shot,soldiers_killed,soldiers_left #declare the 4 variables as global

        self.rect.x = self.x
        self.rect.y = self.y

        #if the enemy's health is less than or equal to 0
        if self.health <=0:
            if self.type == "tank":
                tanks_left -=1
                tanks_shot += 1
            if self.type == "soldier":
                soldiers_killed += 1
                soldiers_left -= 1
            self.kill() #remove sprite object from sprite group
            
        #if the enemy stops once to shoot
        if self.stops == 1:
            #randomly pick where to stop on the x-axis
            self.stop1 = random.randint(100,800) 
            self.stops = 0 #reset stop count
        
        #if the enemy stops twice to shoot
        if self.stops == 2:
            #pick two random x co-ordinate to stop at
            self.stop1 = random.randint(100,300)
            self.stop2 = random.randint(400,800)
            self.stops = 0 #reset stop count

        if self.moving == True:
            self.move(gd)
        self.stop_move(gd)
        self.spawn_back()
        

    def stop_move(self,gd):
        if self.stop2 == None: #if enemy stops once
            #check if enemy is at the x co-ordinate where it was supposed to stop
            if ((self.stop1 - 1) <= self.x and self.x <= (self.stop1 + 1)) and self.stop1_passed == False:
                self.moving = False
                self.stop1_passed = True

            if self.stop1_passed:
                if self.stop1_time is None:
                    self.stop1_time = pygame.time.get_ticks()  
                elapsed_time = pygame.time.get_ticks() - self.stop1_time
                #stop to shoot for 2500 ms
                if elapsed_time <= 2500:
                    self.shoot(gd)
                else:
                    self.moving = True
                #I am decreasing the x co-ordinate by the scroll speed because the enemy will technically "stop" when shooting and the background is moving
                self.x -= scroll_speed
            
        if self.stop2 != None: #if enemy stops twice
            if ((self.stop1 - 1) <= self.x and self.x <= (self.stop1 + 1)) and self.stop1_passed == False:
                self.moving = False
                self.stop1_passed = True

            if self.stop1_passed:
                if self.stop1_time is None:
                    self.stop1_time = pygame.time.get_ticks()  
                elapsed_time1 = pygame.time.get_ticks() - self.stop1_time
                if elapsed_time1 <= 2500:  
                    self.shoot(gd)
                else:
                    self.moving = True
                    self.stop1_passed = None
                self.x -= scroll_speed
                

            if ((self.stop2 - 2) <= self.x and self.x <= (self.stop2 + 2)) and self.stop2_passed == False:
                self.moving = False
                self.stop2_passed = True

            if self.stop2_passed:
                if self.stop2_time is None:
                    self.stop2_time = pygame.time.get_ticks()  
                elapsed_time2 = pygame.time.get_ticks() - self.stop2_time
                if elapsed_time2 <= 2500: 
                    self.shoot(gd)  
                else:
                    self.moving = True 
                    self.stop2_passed = None
                self.x -= scroll_speed
    
    
    def spawn_back(self): #this method spawns the enemies back if the player did not eliminate them when they were moving from one side to the other
        #if enemy is moving from left to right and its x position is greater than or equal to 1000
        if self.direction == 1 and self.x>= 1000:
            self.x = random.randint(-500,0-(self.w+50)) 
            self.y = random.randint(250,600)
            self.stops = random.randint(1,2)
            self.stop1 = None
            self.stop2 = None
            self.stop1_passed = False
            self.stop2_passed = False
            self.stop1_time = None
            self.stop2_time = None
        #if enemy is moving from right to left and the right side of its sprite picture is less than or equal to 0
        if self.direction == 0 and (self.x<= (-self.w - 100)) :
            self.x = random.randint(1000,1500)
            self.y = random.randint(250,600)
            self.stops = random.randint(1,2)
            self.stop1 = None
            self.stop2 = None
            self.stop1_passed = False   
            self.stop2_passed = False
            self.stop1_time = None
            self.stop2_time = None    


    def change_health(self,amount):
        self.health -= amount

    def get_soldiers_killed(self):
        return soldiers_killed

    def get_soldiers_left(self):
        return soldiers_left
    
    def get_tanks_shot(self):
        return tanks_shot

    def get_tanks_left(self):
        return tanks_left


    def reset_enemies(self): #reset the attributes related to the enemy when player plays again
        global soldiers_killed,soldiers_left,tanks_shot,tanks_left
        soldiers_killed = 0 
        tanks_shot = 0
        tanks_left = 5
        soldiers_left = 40

