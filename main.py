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

# creating objects of classes
player1 = player(0,100)
gun = weapon("uzi",101,150,gunshot_sound)
grenade = weapon("grenade",5,500,grenade_sound)
powerups = powerups(player1, gun,random.randint(800,1100),-100,300, gameDisplay)
timer = PausableTimer()


spawn_initial_enemies(soldier_spritesheet,tank_spritesheet,player1,soldier_spritesheet,tank_spritesheet)

gamestate = "start"
while gamestate != "end": # loops until the user wants to exit the game.

    events = get_events() # the variable events contains the dictionary of events returned by get_events()

    if events["quit"] == 1 or events["esc"] == 1: # if user presses the x on the top right of display or presses esc key
        gamestate = "end" # the gamestate is equal to "end" and the loop stops and the user leaves
    

    elif gamestate == "start": 
        play_music(background_music) # play_music function is called which creates the background music 
        draw_cover(main_background) # this function draws the cover of the game onto the screen
        gamestate = can_proceed(events) # this function returns whether the display should proceed onto the next screesn by listening for space key    


    elif gamestate == "name":
        draw_messages_and_title(gameDisplay)
        name = ask_name(gameDisplay,events)
        display_text(black,50,715,"Enter Name:",base_font)
        b = button(300,850,100,350,gameDisplay,dark_green,"name", "menu", "SUBMIT", 90, white, events)
        gamestate = b.name(name)


    elif gamestate == "menu":
        display_menu_texts() # displays title and exit game writing
        player1.change_name(name)
        display_name_score(name) # displays name of player and their highest score

        # code below creates 2 classes for the buttons, play button and leaderboard button
        play = button(350,400,300,300,gameDisplay,orange,"menu","play","PLAY", 60, white,events)
        lb = button(550,150,150,350,gameDisplay,yellow,"menu","leaderboard","LEADERBOARD",45,black,events)

        # the functions below makes sure gamestate is assigned a value based on the precedence of the button clicked
        # this stops user from clicking both buttons and breaking game
        gamestate = precedence(lb.redirect(), play.redirect(),"menu")

    
    elif gamestate == "leaderboard":
        display_leaderboard()   

        #leader board to main menu button
        lb_to_mm = button(550,750,200,400,gameDisplay,navy_blue,"leaderboard","menu","BACK TO MAIN MENU",45,white,events)
        gamestate = lb_to_mm.redirect()
        

    elif gamestate == "play":

        background_music.stop()
        
        try: #Finding the first soldier from the sprite group
            first_soldier = soldiers.sprites()[0]
        except:
            no_soldiers = True

        #display the graphics
        display_game_graphics(gameDisplay,powerups,soldiers,tanks,first_soldier,events,gun,grenade,player1)

        #start the timer to check how long game takes to finish 
        start_timer(timer)
        
        #declares how many enemies are allowed at any one time on the screen
        max_soldiers = max_soldiers_onscreen(first_soldier)

        #add enemies to screen as soon as they are killed or shot
        add_soldiers_to_screen(soldiers,max_soldiers,first_soldier,player1)
        add_tanks_to_screen(tanks,max_tanks,first_soldier,player1) 

        #checking if the player has won the game    
        no_soldiers, gamestate = check_win(no_soldiers,first_soldier,player1,gameDisplay, gamestate)

        #if player has no health, game is over
        if gamestate != "win":
            gamestate = check_loss(player1,gameDisplay)
        
        #if player presses pause, pause menu is displayed
        if gamestate != "win" and gamestate != "loss":
            gamestate = pause_game(timer,events)
                
        try: #calculate the player's score
            player1.calculate_score(getattr(gun,'bullets'),timer.get_elapsed_time(),soldiers.sprites()[0].get_soldiers_killed(),soldiers.sprites()[0].get_tanks_shot())
        except:
            pass
        
     
    elif gamestate == "pause":
        #wait for player to resume
        gamestate = resume(events,timer)
        #display the pause menu with scores information
        display_pause_menu(gameDisplay,getattr(player1,"current_score"),getattr(player1,"high_score"))
    

    elif gamestate == "loss":
        check_score(getattr(player1,"name"),int(getattr(player1,"current_score")),getattr(player1,"high_score")) 
        display_loss_screen(gameDisplay,getattr(player1,"current_score"))
        gamestate = play_again(events,player1,timer,gun,grenade,soldiers,tanks,first_soldier,powerups,"loss",0)


    elif gamestate == "win":
        global win_screen_image,win_screen_counter
        win_screen_counter += 1
        check_score(getattr(player1,"name"),getattr(player1,"current_score"),getattr(player1,"high_score"))
        win_screen(gameDisplay,getattr(player1,"current_score"),getattr(player1,"high_score"),win_screen_counter)
        gamestate, win_screen_counter = play_again(events,player1,timer,gun,grenade,soldiers,tanks,first_soldier,powerups,"win",win_screen_counter)

  
    pygame.display.update()# this line updates the display so that when a change happens in the loop it is displayed.
    clock.tick(120)
pygame.quit()
quit()  

