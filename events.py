import pygame

#below is a dictionary which shows whether a key is pressed/clicked
events = {
    "space": 0,
    "esc": 0,
    "left-click": 0,
    "right-click": 0,
    "quit": 0,
    "x": 500,
    "y": 500,
    "key-down":0,
    "back-space": 0,
    "character": None,
    "letter-done": 0,
    "enter": 0,
    "c": 0,
    }

#the function below assigns a value to the keys in the dictionary above.
def get_events():
    for event in pygame.event.get():


            if event.type == pygame.QUIT: #checks if game was quit by pressing x
                events["quit"] = 1
            
            
            if event.type == pygame.KEYDOWN: #checls if the keyboard key is pressed down
                events["key-down"] = 1

                if events["letter-done"] == 0:
                    events["character"] = event.unicode
                    events["letter-done"] = 1

                if event.key == pygame.K_SPACE:
                    events["space"] = 1

                if event.key == pygame.K_ESCAPE:
                    events["esc"] = 1

                if event.key == pygame.K_BACKSPACE:
                    events["back-space"] = 1

                if event.key == pygame.K_RETURN:
                    events["enter"] = 1

                if event.key == pygame.K_c:
                    events["c"] = 1
            

            if event.type == pygame.KEYUP: #checks if they keyboard key has been released
                events["key-down"] = 0

                if events["letter-done"] == 1:
                    events["letter-done"] = 0

                if event.key == pygame.K_SPACE:
                    events["space"] = 0

                if event.key == pygame.K_ESCAPE:
                    events["esc"] = 0

                if event.key == pygame.K_BACKSPACE:
                    events["back-space"] = 0

                if event.key == pygame.K_RETURN:
                    events["enter"] = 0

                if event.key == pygame.K_c:
                    events["c"] = 0
            

            if event.type == pygame.MOUSEBUTTONDOWN: #checks if the mouse button is clicked
                if event.button == 1:
                    events["left-click"] = 1

                if event.button == 3:
                    events["right-click"] = 1
            

            if event.type == pygame.MOUSEBUTTONUP: #checks if the mouse button is released
                if event.button == 1:
                    events["left-click"] = 0
                    
                if event.button == 3:
                    events["right-click"] = 0

            
            events["x"],events["y"] = pygame.mouse.get_pos()
            
    return events #the event dictionary is returned so that it can be accessed in the main loop             
                    
        
