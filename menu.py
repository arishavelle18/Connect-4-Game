from button import Button
import pygame
import sys
import connect4
pygame.init()
SCREEN = pygame.display.set_mode((700,700))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/Background.png")
SQUARESIZE = 100
ROW_COUNT = 6
COLUMN_COUNT = 7
width = COLUMN_COUNT * SQUARESIZE  # 7
height = (ROW_COUNT + 1) * SQUARESIZE # 7 

# create a font that will access in the game 
def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def play():
    pygame.display.set_caption("Connect 4")
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # change the background into black
        SCREEN.blit(BG,(0,0))

        PLAY_TEXT = get_font(70).render("MODE", True, "#b68f40")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(height/2, 100))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(620, 560), 
                            text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")
        Player_AI = Button(image=pygame.transform.scale(pygame.image.load("assets/PlayRect.png"), (500, 100)), pos=(width/2,height/3), text_input="Player vs AI", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        
        Player_Player = Button(image=pygame.transform.scale(pygame.image.load("assets/OptionsRect.png"), (680, 100)), pos=(width/2,height/2+30), 
                            text_input="Player vs Player", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        AI_AI = Button(image=pygame.transform.scale(pygame.image.load("assets/QuitRect.png"), (400, 100)), pos=(width/2,height/1.5+60), 
                            text_input="AI vs AI", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BACK,Player_AI,Player_Player, AI_AI]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)
        
        # PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        # # PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if Player_AI.checkForInput(PLAY_MOUSE_POS):
                    connect4.connect4(1)
                if Player_Player.checkForInput(PLAY_MOUSE_POS):
                    connect4.connect4(3)
                if AI_AI.checkForInput(PLAY_MOUSE_POS):
                    connect4.connect4(2)

        pygame.display.update()
    
def options():
    pygame.display.set_caption("INSTRUCTION")
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG,(0,0))

        OPTIONS_TEXT = get_font(45).render("INSTRUCTION", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(height/2, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_TEXT1 = get_font(11).render("To be the first player ", True, "#b68f40")
        OPTIONS_RECT1 = OPTIONS_TEXT1.get_rect(center=(height/2, 200))
        SCREEN.blit(OPTIONS_TEXT1, OPTIONS_RECT1)
        # of the same colored discs in a row (either vertically, horizontally, or diagonally
        OPTIONS_TEXT2 = get_font(11).render("to connect 4 of the same colored discs in a row", True, "#b68f40")
        OPTIONS_RECT2 = OPTIONS_TEXT2.get_rect(center=(height/2, 230))
        SCREEN.blit(OPTIONS_TEXT2, OPTIONS_RECT2)
        OPTIONS_TEXT3 = get_font(11).render("(either vertically, horizontally, or diagonally)", True, "#b68f40")
        OPTIONS_RECT3 = OPTIONS_TEXT3.get_rect(center=(height/2, 260))
        SCREEN.blit(OPTIONS_TEXT3, OPTIONS_RECT3)
        # 

        OPTIONS_BACK = Button(image=None, pos=(width/2, height/2), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    pygame.display.set_caption("Menu")

    while True:
        SCREEN.blit(BG,(0,0))

        # check what is the coordinate of the mouse 
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # just put the "Main menu" text in the middle
        MENU_TEXT = get_font(70).render("MAIN MENU",True,"#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(height/2,100))
        # play ,option and quit button 
        PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/PlayRect.png"), (250, 100)), pos=(width/2,height/3), text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        
        OPTIONS_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/OptionsRect.png"), (600, 100)), pos=(width/2,height/2+30), 
                            text_input="INSTRUCTION", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/QuitRect.png"), (250, 100)), pos=(width/2,height/1.5+60), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                 #  if you want to play
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                #  if you want to go in option
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()



main_menu()
