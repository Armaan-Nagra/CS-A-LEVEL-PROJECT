import pygame
from settings import *
import json
import random
from enemy import *
#from button import *
pygame.init()
def initialise_pygame_display():
    global width, height, clock, gameDisplay # makes variables global so that they can be accessed elsewhere
    pygame.init() #initialises pygame library
    pygame.font.init()
    pygame.mixer.init()# initialises sound
    pygame.display.set_caption("Operation Monkey")
    # below, size of display is set as 2 variables
    width = 1000
    height = 1000
    gameDisplay = pygame.display.set_mode((width, height)) # display is created
    clock = pygame.time.Clock() # variable clock is an object which keeps track of time
    return width, height, gameDisplay, clock

def can_proceed(events):
    if events["space"] == 1:
        return "name"
    else:
        return "start"

def play_music(music):
    if not pygame.mixer.get_busy():
        music.play(-1)


def draw_cover(picture):
    gameDisplay.blit(picture,(0,0))
    
def draw_messages_and_title(gameDisplay):
    gameDisplay.fill(white)
    title = arcade_font.render("OPERATION MONKEY", False, black)
    gameDisplay.blit(title, (width // 2 - title.get_width() // 2, 50))
    gameDisplay.blit(message1, (0,200))
    gameDisplay.blit(message2, (0,425))


def ask_name(gameDisplay,events):
    global name_placeholder, input_rect, inside_input_box #makes variables global

    if events["left-click"] == 1:
        if input_rect.collidepoint((events["x"],events["y"])):
            inside_input_box = True # if the user clicks on the input box the variable is set to true
    if events["key-down"] == 1:
        if inside_input_box:
            now = pygame.time.get_ticks()
            global last_stamp
            if now - last_stamp >= 115: #simple algorithm to restrict how many characters are inputted, it is one character every 115 ms right now
                if events["back-space"] == 1: 
                    name_placeholder = name_placeholder[:-1] # if user presses backspace, a letter from name is deleted
                else:
                    name_placeholder += events["character"] #character is added to name variable depending on key pressed
                last_stamp = pygame.time.get_ticks()
                    
    if inside_input_box:
        colour = red
        outline = 5 # if user clicks on input box it changes colour and outline width
    else:
        colour = black
        outline = 2 # if he does not, it remains the same

    #input box is drawn and text is added to it as the player types in their name
    pygame.draw.rect(gameDisplay,colour,input_rect,outline)
    text_surface = base_font.render(name_placeholder,True, black)
    gameDisplay.blit(text_surface, (input_rect.x + 5, input_rect.y + 8))
    input_rect.w = max(300,text_surface.get_width() + 10) #input box automatically resizes itself
    
    return name_placeholder

def display_text(colour, x, y, message, font):
    message = font.render(message, False, colour)
    gameDisplay.blit(message, (x, y))
    
def load_name_score():
    try:
        with open('name_score.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}



def display_name_score(name):
    file = load_name_score()
    for x in file["users"]:
        if x["username"] == name.upper():
            high_score = x["high_score"]
    display_text(white,15,175,"Name: "+name,name_score_font)
    display_text(white,15,225,"High Score: "+str(high_score),name_score_font)

    
def precedence(first_button,second_button,current):
    if first_button!= current and second_button == current:
        return first_button
    elif second_button!= current and first_button == current:
        return second_button
    else:
        return current

def display_menu_texts():
    gameDisplay.fill(black)
    display_text(white,207,50,"OPERATION MONKEY",arcade_font)
    display_text(red,600,900,"PRESS ESC TO EXIT",pygame.font.Font(None,50))
    
def display_leaderboard():
    gameDisplay.fill(black)
    display_text(yellow, 230,50,"LEADERBOARD",pygame.font.Font("Stages/Stage 2/arcade_font.ttf", 50))

    positions = calculate_positions() # functions returns the top 3 scores as dictionary objects

    if positions == "invalid":
        display_text(red, 200,400 , "NOT ENOUGH DATA", leaderboard_font)
    else:
        display_text(white, 250, 250, "NAME", leaderboard_font) 
        display_text(white, 750, 250, "SCORE", leaderboard_font)
        for x in range(3): # loops 3 times to display the names and high_scores
            display_text(white, 50, 350+(100*x),(str(x+1)+".       "+ positions[x]["username"]), leaderboard_font)
            display_text(white, 750, 350+(100*x), str(positions[x]["high_score"]), leaderboard_font)
        
        




def calculate_positions():
    data = load_name_score() #loads the JSON file

    #creates placeholders for the top 3 scorers
    first = {
        "username": "player1",
        "high_score": 0
        }
    second = {
        "username": "player2",
        "high_score": 0
        }
    third = {
        "username": "player3",
        "high_score": 0
        }

    #returns "invalid" if there are less than 3 items of data.
    if len(data["users"]) < 3:
        return "invalid"
    
    #logic to check the order of scoring
    for x in data["users"]:
        if x["high_score"] > first["high_score"]: 
            third = second.copy()
            second = first.copy()
            first = x
        elif x["high_score"] > second["high_score"]:
            third = second.copy()
            second = x
        elif x["high_score"] > third["high_score"]:
            third = x

    return first, second, third

def scroll_background(gd):
    global background_x #creates a global variable which contains x co-ordinate of background photo
    background_x -= scroll_speed #the photo moves to the left with "scroll_speed"
    if background_x <= -2000: #if the photo reaches x co-ordinate "-2000", x co-ordinate becomes 0
        background_x = 0 
    #background_image is a variable stored in settings and it's displayed to the screen at x co-ordinate 0 and 2,000
    gd.blit(level_background, (background_x, 0)) 
    gd.blit(level_background, (background_x + 2000, 0))

def show_soldiers(soldier_count,soldier_photo,x,y,gd):
      gd.blit(soldier_photo, (x,y))
      display_text(black,x+25,y+110,str(soldier_count),level_font)

def show_tanks(tank_count,tank_photo,x,y,gd):
      gd.blit(tank_photo, (x,y))
      display_text(black,x+45,y+90,str(tank_count),level_font)

def spawn_initial_enemies(soldier_spritesheet,tank_spritesheet,player1,s_spritesheet,t_spritesheet):
    for x in range(5):  
        direction = random.getrandbits(1)
        if direction == 1:
            enemy_soldier = enemy(random.randint(-1000,-150),random.randint(250,600),100,s_spritesheet,random.randint(1,2),direction,2,75,player1,"soldier",100,200,-0.5)
        else:
            enemy_soldier = enemy(random.randint(1000,2000),random.randint(250,600),100,s_spritesheet,random.randint(1,2),direction,2,75,player1,"soldier",100,200,-0.5)
        soldiers.add(enemy_soldier) 

    direction = random.getrandbits(1)
    if direction == 1:
        enemy_tank = enemy(random.randint(-1000,-250),random.randint(250,600),500,t_spritesheet,random.randint(1,2),direction,2,75,player1,"tank",320,200,-1)
    else:
        enemy_tank = enemy(random.randint(1000,2000),random.randint(250,600),500,t_spritesheet,random.randint(1,2),direction,2,75,player1,"tank",320,200,-1)
    tanks.add(enemy_tank) 


def display_pause_menu(gd,score, high_score):
    gd.blit(pause_menu,(100,150))
    display_text(white,600,289,str(int(score)),arcade_font)
    display_text(white,600,385,str(int(high_score)),arcade_font)

def check_score(name,new_score,high_score):
    #load a copy of the JSON file containing scores
    file = load_name_score()
    
    #update scores in the "file" variable
    if new_score > high_score:
        for x in file["users"]:
            if x["username"] == name.upper():
                x["high_score"] = int(new_score)
    
    #ammend these changes into the name_score.json file
    with open('name_score.json', 'w') as output_file:
        json.dump(file, output_file, indent=3)

def return_high_score(name):
    file = load_name_score()
    for x in file["users"]:
        if x["username"] == name.upper():
            return(x["high_score"])     

def increase_brightness(gd,counter):
    #a surface is created and the game_over image is drawn over it
    fade = pygame.Surface((1000,1000))
    fade.blit(game_over,(0,0))

    #changes the transparency of the fade surface to the counter parameter
    fade.set_alpha(counter) 
    #draws the surface "fade" onto the game display
    gd.blit(fade,(0,0))

def loss_screen(gd,score):
    gd.blit(game_over,(0,0))
    display_text(black,650,450,str(int(score)),pygame.font.Font("Stages/Stage 2/arcade_font.ttf", 65))

def winning_fading(gd,counter):
    #create a fade surface
    fade = pygame.Surface((1000,1000))
    #draw the winning image onto the surface
    fade.blit(winning_image,(0,0))
    #change opacity of the surface
    fade.set_alpha(counter-150)
    #draw surface onto screen
    gd.blit(fade,(0,0))

def win_screen(gd,score,high_score,counter):
    #draw the winning image and mission completed stamp onto the screen
    gd.blit(winning_image,(0,0))
    gd.blit(mission_completed,(0,0))
    #once some time has passed and counter is greater than or equal to 100
    if counter >= 100:
        #draw the win_screen_image containing scoring onto the screen
        gd.blit(win_screen_image,(0,0))
        #display the appropriate scores
        display_text(black,580,350,str(int(score)),pygame.font.Font("Stages/Stage 2/arcade_font.ttf", 35))
        display_text(black,580,511,str(int(score)),pygame.font.Font("Stages/Stage 2/arcade_font.ttf", 35))

def reset_level(player,timer,uzi,grenade,soldiers,tanks,soldier_spritesheet,tank_spritesheet,first_soldier,powerup):
    #make the cursor visible 
    pygame.mouse.set_visible(True)
    #reset the powerups options
    powerup.reset_powerups()
    #reset the player options
    player.reset_player()
    #reset the timer
    timer.reset_timer()
    #reset the uzi 
    uzi.reset_weapon()
    #reset the grenades
    grenade.reset_weapon()
    #reset the enemies
    first_soldier.reset_enemies()
    tanks.empty()
    soldiers.empty()
    #spawns the enemies again randomly 
    spawn_initial_enemies(soldiers,tanks,player,soldier_spritesheet,tank_spritesheet)

def display_game_graphics(gd,powerups,soldiers,tanks,first_soldier,events,gun,grenade,player):
    gd.fill(white)
    scroll_background(gd)
    powerups.update(first_soldier.get_soldiers_left(),events["x"],events["y"],events["left-click"])
    soldiers.update(gd)
    tanks.update(gd)
    player.health_bar(gd)
    gun.display_HUD(uzi,gd,750,800,775,925)
    grenade.display_HUD(grenade_image,gd,875,800,915,925)
    show_soldiers(first_soldier.get_soldiers_left(),soldier_icon,50,800,gd)
    show_tanks(first_soldier.get_tanks_left(),tank_icon,170,820,gd)
    gun.shoot_effects(events["left-click"], black_cross,gd,events["x"],events["y"],events["x"] - 25,events["y"]-25,[soldiers,tanks])
    grenade.shoot_effects(events["right-click"], grenade_visual, gd,events["x"],events["y"],events["x"] - 125,events["y"] - 125,[soldiers,tanks])
    gun.draw_hitbox(gd,black,4,10)

def start_timer(timer):
    if getattr(timer,'started') == False:
        timer.start()

def pause_game(timer,events):
    if events["space"] == 1:
        #pause the timer
        timer.pause()
        return "pause"
    else:
        return "play"

def max_soldiers_onscreen(given_first_soldier):
    if given_first_soldier.get_soldiers_killed() >= 10 and given_first_soldier.get_soldiers_killed() <=29:
        return 10 
    if given_first_soldier.get_soldiers_killed() >= 30:
        return given_first_soldier.get_soldiers_left() 
    else:
        return 5
    
def add_soldiers_to_screen(soldiers,max_soldiers,first_soldier,player):
    if len(soldiers) < max_soldiers and first_soldier.get_soldiers_left() >=0:
        direction = random.getrandbits(1)
        if direction == 1:
            enemy_soldier = enemy(random.randint(-1500,-150),random.randint(250,600),100,soldier_spritesheet,random.randint(1,2),direction,2,75,player,"soldier",100,200,-0.5)
        else:
            enemy_soldier = enemy(random.randint(1000,1500),random.randint(250,600),100,soldier_spritesheet,random.randint(1,2),direction,2,75,player,"soldier",100,200,-0.5)
        soldiers.add(enemy_soldier)

def add_tanks_to_screen(tanks,max_tanks,first_soldier,player):
    if len(tanks) < max_tanks and first_soldier.get_tanks_left() !=0:  
        direction = random.getrandbits(1)
        #direction = 1
        if direction == 1:
            enemy_tank = enemy(random.randint(-1000,-250),random.randint(250,600),300,tank_spritesheet,random.randint(1,2),direction,2,75,player,"tank",320,200,-1)
        else:
            enemy_tank = enemy(random.randint(1000,2000),random.randint(250,600),300,tank_spritesheet,random.randint(1,2),direction,2,75,player,"tank",320,200,-1)
        tanks.add(enemy_tank) 