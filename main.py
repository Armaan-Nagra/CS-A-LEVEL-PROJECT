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
from timer import *

width, height, gameDisplay, clock = initialise_pygame_display()

player1 = player(0,0,100)
gun = weapon("uzi",101,150,gunshot_sound)
grenade = weapon("grenade",5,500,grenade_sound)
powerups = powerups(player1, gun,random.randint(800,1100),-100,300, gameDisplay)
timer = PausableTimer()


spawn_initial_enemies(soldier_spritesheet,tank_spritesheet,player1,soldier_spritesheet,tank_spritesheet)

gamestate = "start"
while gamestate != "end": #loops until the user wants to exit the game.
    events = get_events() #the variable events contains the dictionary of events returned by get_events()
    if events["quit"] == 1 or events["esc"] == 1: # if user presses the x on the top right of display or presses esc key
        gamestate = "end" #the gamestate is equal to "end" and the loop stops and the user leaves
    elif gamestate == "start": 
        play_music(background_music) #play_music function is called which creates the background music 
        draw_cover(main_background) #this function draws the cover of the game onto the screen
        gamestate = can_proceed(events) # this function returns whether the display should proceed onto the next screesn by listening for space key    

    elif gamestate == "name":
        #global name
        draw_messages_and_title(gameDisplay)
        name = ask_name(gameDisplay,events)
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
        
        #start timer if the game just started
        if getattr(timer,'started') == False:
            timer.start()

        #if the player wants to pause
        if events["space"] == 1:
            #pause the timer
            timer.pause()
            gamestate = "pause"

        #I find the first soldier from the soldiers group if there is any 
        try:
            first_soldier = soldiers.sprites()[0]
        except:
            no_soldiers = True

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
        show_soldiers(first_soldier.get_soldiers_left(),soldier_icon,50,800,gameDisplay)
        show_tanks(first_soldier.get_tanks_left(),tank_icon,170,820,gameDisplay)

        #calculate the player's score
        #player1.calculate_score(getattr(gun,'bullets'),timer.get_elapsed_time(),soldiers.sprites()[0].get_soldiers_killed(),soldiers.sprites()[0].get_tanks_shot())

        if no_soldiers == True and first_soldier.get_tanks_left() == 0:
            global win_counter, win_sound,sound_play
            win_counter += 1
            #play game winning sound
            if sound_play == False:
                win_sound.play()
                sound_play = True
            if win_counter>150 and win_counter<450:
                #Fade the winning screen in
                winning_fading(gameDisplay,win_counter)            
            if win_counter>=450:
                #draw the winning image onto the screen
                gameDisplay.blit(winning_image,(0,0)) 
                #play the stamp sound
                stamp.play()
                win_counter = 0
                sound_play = False
                max_soldiers = 5
                no_soldiers = False
                #change game state to win
                gamestate = "win"
                
        #if player has no health, game is over
        if getattr(player1,'health') <= 0:
            #play game over sound
            global alpha_counter
            alpha_counter += 1
            if sound_play == False:
                loss_sound.play()
                sound_play = True
            if alpha_counter<255:
                #increase the brightness of the screen until it is fully white
                increase_brightness(gameDisplay,alpha_counter)
            else: 
                gameDisplay.blit(game_over,(0,0))
                alpha_counter = 0
                sound_play = False
                #change gamestate variable to "loss"
                max_soldiers = 5
                gamestate = "loss"

        #calculate the player's score
        try:
            player1.calculate_score(getattr(gun,'bullets'),timer.get_elapsed_time(),soldiers.sprites()[0].get_soldiers_killed(),soldiers.sprites()[0].get_tanks_shot())
        except:
            pass
        
        print(getattr(player1,"current_score"),getattr(player1,"high_score"))
    elif gamestate == "pause":
        if events["enter"] == 1:
            timer.resume()
            gamestate = "play"
 
        #display the pause menu with scores information
        display_pause_menu(gameDisplay,getattr(player1,"current_score"),getattr(player1,"high_score"))
    
    elif gamestate == "loss":
        check_score(getattr(player1,"name"),int(getattr(player1,"current_score")),getattr(player1,"high_score")) 
        loss_screen(gameDisplay,getattr(player1,"current_score"))
        if events["space"]:
            gamestate = "menu"
            reset_level(player1,timer,gun,grenade,soldiers,tanks,soldier_spritesheet,tank_spritesheet,first_soldier,powerups)

    elif gamestate == "win":
        global win_screen_image,win_screen_counter
        win_screen_counter += 1
        check_score(getattr(player1,"name"),getattr(player1,"current_score"),getattr(player1,"high_score"))
        win_screen(gameDisplay,getattr(player1,"current_score"),getattr(player1,"high_score"),win_screen_counter)
        if events["space"]:
            win_screen_counter = 0
            gamestate = "menu"
            reset_level(player1,timer,gun,grenade,soldiers,tanks,soldier_spritesheet,tank_spritesheet,first_soldier,powerups)

  
    pygame.display.update()# this line updates the display so that when a change happens in the loop it is displayed.
    clock.tick(120)
pygame.quit()
quit()  

