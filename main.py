import pygame
from settings import *
from events import *
from functions import *
from button import *
import json
from weapon import *
from player import *
from enemy import *
import random
from powerups import *

width, height, gameDisplay, clock = initialise_pygame_display()

player1 = player(0,1500,10000)
gun = weapon("uzi",101,150,gunshot_sound)
grenade = weapon("grenade",5,500,grenade_sound)
powerups = powerups(player1, gun,random.randint(800,1100),-100,300, gameDisplay)

soldier_spritesheet = []
soldier_spritesheet.append(run1)
soldier_spritesheet.append(run2)
soldier_spritesheet.append(shooting_soldier)
soldier_spritesheet.append(white_shoot)

tank_spritesheet = []
tank_spritesheet.append(tank1)
tank_spritesheet.append(tank2)
tank_spritesheet.append(tank_shoot)
tank_spritesheet.append(tank_white) 


soldiers = pygame.sprite.Group()
tanks = pygame.sprite.Group()
for x in range(5):  
    direction = random.getrandbits(1)
    if direction == 1:
        enemy_soldier = enemy(random.randint(-1000,-150),random.randint(250,600),100,soldier_spritesheet,random.randint(1,2),direction,2,75,player1,"soldier",100,200,-0.5)
    else:
        enemy_soldier = enemy(random.randint(1000,2000),random.randint(250,600),100,soldier_spritesheet,random.randint(1,2),direction,2,75,player1,"soldier",100,200,-0.5)
    soldiers.add(enemy_soldier) 

direction = random.getrandbits(1)
# direction = 0
if direction == 1:
    enemy_tank = enemy(random.randint(-1000,-250),random.randint(250,600),500,tank_spritesheet,random.randint(1,2),direction,2,75,player1,"tank",320,200,-1)
else:
    enemy_tank = enemy(random.randint(1000,2000),random.randint(250,600),500,tank_spritesheet,random.randint(1,2),direction,2,75,player1,"tank",320,200,-1)
tanks.add(enemy_tank) 

gamestate = "start"
while gamestate != "end": #loops until the user wants to exit the game.
    events = get_events() #the variable events contains the dictionary of events returned by get_events()z
    if events["quit"] == 1 or events["esc"] == 1: # if user presses the x on the top right of display or presses esc key
        gamestate = "end" #the gamestate is equal to "end" and the loop stops and the user leaves
    elif gamestate == "start": 
        play_music(background_music) #play_music function is called which creates the background music 
        draw_cover(main_background) #this function draws the cover of the game onto the screen
        gamestate = can_proceed(events) # this function returns whether the display should proceed onto the next screen by listening for space key    

    elif gamestate == "name":
        #global name
        draw_messages_and_title(gameDisplay)
        name = ask_name(gameDisplay)
        display_text(black,50,715,"Enter Name:",base_font)
        b = button(300,850,100,350,gameDisplay,dark_green,"name", "menu", "SUBMIT", 90, white, events)
        gamestate = b.name(name)


    elif gamestate == "menu":
        display_menu_texts() # displays title and exit game writing
        player1.change_name(name)
        display_name_score(name) # displays name of player and their highest score

        # code below creates 2 classes for the buttons 
        play = button(350,400,300,300,gameDisplay,orange,"menu","play","PLAY", 60, white,events)
        lb = button(550,150,150,350,gameDisplay,yellow,"menu","leaderboard","LEADERBOARD",45,black,events)

        # the functions below makes sure gamestate is assigned a value based on the precedence of the button clicked
        # not the order of code
        gamestate = precedence(lb.redirect(), play.redirect(),"menu")
    elif gamestate == "leaderboard":
        display_leaderboard()   
        mm = button(550,750,200,400,gameDisplay,navy_blue,"leaderboard","menu","BACK TO MAIN MENU",45,white,events)
        gamestate = mm.redirect()
        

    elif gamestate == "play":
        background_music.stop()
        
        #if player has no health, game is over
        if getattr(player1,'health') <= 0:
            gamestate = "loss"

        #I find the first soldier from the soldiers group if there is any 
        try:
            first_soldier = soldiers.sprites()[0]
        except:
            no_soldiers = True

        #if all soldiers are killed, player wins
        if no_soldiers == True and first_soldier.get_tanks_left() == 0:
            gamestate = "win"

        #display the background
        gameDisplay.fill(white)
        scroll_background(gameDisplay)
        powerups.update(first_soldier.get_soldiers_left(),events["x"],events["y"],events["left-click"])
        soldiers.update(gameDisplay)
        tanks.update(gameDisplay)

        #display information about the player
        player1.health_bar(gameDisplay)
        gun.display_HUD(uzi,gameDisplay,750,800,775,925)
        grenade.display_HUD(grenade_image,gameDisplay,875,800,915,925)
         
        #weapon effects
        gun.shoot_effects(events["left-click"], black_cross,gameDisplay,events["x"],events["y"],events["x"] - 25,events["y"]-25,[soldiers,tanks])
        grenade.shoot_effects(events["right-click"], grenade_visual, gameDisplay,events["x"],events["y"],events["x"] - 125,events["y"] - 125,[soldiers,tanks])
        gun.draw_hitbox(gameDisplay,black,4,10)
        
        #declares how many enemies are allowed at any one time on the screen
        if first_soldier.get_soldiers_killed() >= 10 and first_soldier.get_soldiers_killed() <=29:
            max_soldiers = 10 
        if first_soldier.get_soldiers_killed() >= 30:
            max_soldiers = first_soldier.get_soldiers_left() 

        #the two main if statements below make sure that the right amount of tanks and enemies are visible at any one time
        if len(soldiers) < max_soldiers and first_soldier.get_soldiers_left() >=0:
            direction = random.getrandbits(1)
            if direction == 1:
                enemy_soldier = enemy(random.randint(-1500,-150),random.randint(250,600),100,soldier_spritesheet,random.randint(1,2),direction,2,75,player1,"soldier",100,200,-0.5)
            else:
                enemy_soldier = enemy(random.randint(1000,1500),random.randint(250,600),100,soldier_spritesheet,random.randint(1,2),direction,2,75,player1,"soldier",100,200,-0.5)
            soldiers.add(enemy_soldier)
        
        if len(tanks) < max_tanks and first_soldier.get_tanks_left() !=0:  
            direction = random.getrandbits(1)
            #direction = 1
            if direction == 1:
                enemy_tank = enemy(random.randint(-1000,-250),random.randint(250,600),300,tank_spritesheet,random.randint(1,2),direction,2,75,player1,"tank",320,200,-1)
            else:
                enemy_tank = enemy(random.randint(1000,2000),random.randint(250,600),300,tank_spritesheet,random.randint(1,2),direction,2,75,player1,"tank",320,200,-1)
            tanks.add(enemy_tank) 

        #displays the amount of soldiers and tanks left
        show_soldiers(first_soldier.get_soldiers_left(),soldier_headshot,50,800,gameDisplay)
        show_tanks(first_soldier.get_tanks_left(),tank_small,170,820,gameDisplay)
        
         
  
    pygame.display.update()# this line updates the display so that when a change happens in the loop it is displayed.
    clock.tick(120)
pygame.quit()
quit()  

