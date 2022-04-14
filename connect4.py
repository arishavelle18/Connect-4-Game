import numpy as np 
import pygame
import sys
import math
import random

BLUE = (0,96,255)
BLACK  = (0,0,0)
RED = (255,132,132)
GREEN = (255,62,51)
ROW_COUNT = 6
COLUMN_COUNT = 7

# for turn
PLAYER = 0
AI = 1

# for piece
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4
# get the background asset
BG = pygame.image.load("assets/Background.png")

# create a font that will access in the game 
def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

# initializing create_board():
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col , piece):
    board[row][col] = piece

# check if is valid to insert or not 
def is_valid_location(board,col):
    return board[ROW_COUNT-1][col] == 0

# just checking if the element is equal to zero then it will use it to manipulate to drop a piece 
def get_next_open_row(board,col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    # when you flip it the array of element is decreasing 
    print(np.flip(board,0))
    
def winning_move(board,piece):
    # check horizontal if you won
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check for vertizal
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    
    # check positive slope for diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # check negative slope for diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(3,ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window,piece):
    # declare score
    score = 0

    # check if the opponent piece is player or ai
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    
    # check the blocking of the opponent 

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    
    return score

def score_position(board,piece):
    score = 0
    # Score for center column
    center_array = [int(i) for i in list(board[:,COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score in Horizontal
    for r in range(ROW_COUNT):
        # row_array consist of row element in board ex [0,0,0,1,0,0,0]
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            # window hold every 4 element in the row_array
            window = row_array[c:c+WINDOW_LENGTH]
            # check if you put same piece horizontally and simultaneously
            # check if you put 3 same piece horizontally and it consist of zero value in the list 
            score += evaluate_window(window=window,piece=piece)
    # Score in Vertical
    for c in range(COLUMN_COUNT):
        # get all the list each column in board
        column_array= [ int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            # window hold all the row element
            window = column_array[r:r+WINDOW_LENGTH]

            # check if it create 4 same piece simultaneously
            # check if it create 3 same piece simultaneously and has a one 0
            score += evaluate_window(window=window,piece=piece)

    # Score in positive slope
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            # window hold all the positive slope element
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            
            # check if it create 4 same piece simultaneously
            # check if it create 3 same piece simultaneously and has a one 0
            score += evaluate_window(window=window,piece=piece)
            
    # Score in negative slope
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            # window hold all the negative slope element
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]

            # check if it create 4 same piece simultaneously
            # check if it create 3 same piece simultaneously and has a one 0
            score += evaluate_window(window=window,piece=piece)

    return score

def is_terminal_node(board):
    return winning_move(board=board,piece=PLAYER_PIECE) or winning_move(board=board,piece=AI_PIECE) or len(get_valid_locations(board=board)) == 0

def minimax(board,depth,alpha,beta,maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal  = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board,AI_PIECE):
                return (None , 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None , -100000000000000)
            else:
                return (None , 0)
        else:
            return (None , score_position(board,AI_PIECE))
    if maximizingPlayer: # maximize 
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board,col) 
            b_copy = board.copy()
            drop_piece(b_copy,row,col,AI_PIECE)
            new_score = minimax(b_copy,depth-1,alpha,beta,False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha,value)
            # check if the alpha is greater than or equal to beta then break
            if alpha >= beta:
                break
        return column , value
    else: # minimum
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy,row,col,PLAYER_PIECE)
            new_score = minimax(b_copy,depth-1,alpha,beta,True)[1]      
            if new_score < value :
                value =  new_score
                column = col 
            beta = min(beta,value)
            # check if the alpha is greater than or equal to beta then break
            if alpha >= beta:
                break
        return column, value
def get_valid_locations(board):
    # declare a valid_locations and this list will contain all the valid location in the board
    valid_locations = []
    # this will check column by column base on the board and append the column that is valid to the variable valid locations
    for col in range(COLUMN_COUNT):
        if is_valid_location(board,col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board,piece):
    # get the list that consist of valid locations
    valid_locations = get_valid_locations(board)

    # declare a variable that determine the best score and column
    # brb
    # best_score = 0
    best_score = -10000
    # this variable will just randomly choose in the list of valid_locations
    best_col = random.choice(valid_locations)

    # just loop all the column and check what is the better column that AI must insert
    for col in valid_locations:
        # get the row and its column that is available to insert
        row = get_next_open_row(board=board,col=col)
        # just create a temporary board
        temp_board = board.copy()
        # just drop or put the pieces in the certain part in the temporary board
        drop_piece(temp_board,row,col,piece)
        # calculate the score of that temporary board
        score = score_position(temp_board,piece)

        # checking if the score highest then it will overwrite the best score and column
        if score > best_score:
            best_score = score
            best_col = col
    
    return best_col


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,BLUE,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            pygame.draw.circle(screen,BLACK,(int(c*SQUARESIZE+SQUARESIZE/2),int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),RADIUS)
            
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # check if player 1 Red
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen,RED,(int(c*SQUARESIZE+SQUARESIZE/2),height - int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen,GREEN,(int(c*SQUARESIZE+SQUARESIZE/2),height - int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
    # take note: you need to update if you are something to manipulate in the window
    pygame.display.update()



board = create_board()

game_over =  False
# check if player 1 turn or AI turn 


# initialize the pygame  
pygame.init()

# how big the board is
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE  # 7
height = (ROW_COUNT + 1) * SQUARESIZE # 7 



# put width and height inside the tuple
size = (width,height)
# get the radius
RADIUS = int(SQUARESIZE/2 - 5)

# generate the size of the screen
screen = pygame.display.set_mode(size=size)
PLAY_TEXT = get_font(70).render("Connect 4", True, "#b68f40")
PLAY_RECT = PLAY_TEXT.get_rect(center=(height/2, 50))
screen.blit(PLAY_TEXT, PLAY_RECT)
draw_board(board=board)
#  if you want to change any design you need to update after
# pygame.display.update()

# initializing the font
myFont = get_font(40)
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             exit(1)
def connect4(cat):
    screen.fill("black")
    board = create_board()
    turn = random.randint(PLAYER,AI)
    draw_board(board=board)
    print_board(board)
    game_over =  False
    while not game_over:

        # to open pygame window you need this
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(1)
            # this function purpose is track the movement of the mouse
            if event.type == pygame.MOUSEMOTION:
                posX = event.pos[0]
                pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
                if turn == PLAYER and cat != 2:
                    pygame.draw.circle(screen,RED,(posX,SQUARESIZE/2),RADIUS)
                elif turn == AI and cat == 3:
                    pygame.draw.circle(screen,GREEN,(posX,SQUARESIZE/2),RADIUS)
                pygame.display.update()


            
            if event.type == pygame.MOUSEBUTTONDOWN and (cat == 1 or cat == 3):
                pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))

                # print(event.pos)
                if turn == PLAYER :
                # Player 1 
                    #  get the position of  x axis
                    posX = event.pos[0]
                    # col = int(input("Player 1 Make your Selection (0-6) :"))
                    col = int(math.floor(posX/SQUARESIZE))
                    print(col)
                    turn = 1

                    if is_valid_location(board=board,col=col):
                        row = get_next_open_row(board=board,col=col)
                        drop_piece(board=board, row=row,col=col,piece=PLAYER_PIECE)

                        # check if player 1 won 
                        if winning_move(board=board,piece=PLAYER_PIECE):
                            print("Congrats Player 1 Won")
                            label = myFont.render("Player 1 Won",1,RED)
                            screen.blit(label,(40,10))
                            game_over = True
                        print_board(board)
                        draw_board(board=board)
                    else:
                        turn = 0
                elif turn == AI and cat == 3 :
                # Player 2 
                    #  get the position of  x axis
                    posX = event.pos[0]
                    # col = int(input("Player 1 Make your Selection (0-6) :"))
                    col = int(math.floor(posX/SQUARESIZE))
                    print(col)
                    turn = 0

                    if is_valid_location(board=board,col=col):
                        row = get_next_open_row(board=board,col=col)
                        drop_piece(board=board, row=row,col=col,piece=AI_PIECE)

                        # check if player 1 won 
                        if winning_move(board=board,piece=AI_PIECE):
                            print("Congrats Player 1 Won")
                            label = myFont.render("Player 2 Won",1,GREEN)
                            screen.blit(label,(40,10))
                            game_over = True
                        print_board(board)
                        draw_board(board=board)
                    else:
                        turn = 1

                
        if turn == PLAYER and cat == 2 and cat !=3 :
            print("pasok1")
            col,minimax_score = minimax(board=board,depth=5,alpha=-math.inf,beta=math.inf,maximizingPlayer=True)
            turn = 1

            if is_valid_location(board=board,col=col):
                # pygame.time.wait(1000)
                row = get_next_open_row(board=board,col=col)
                drop_piece(board=board, row=row,col=col,piece=PLAYER_PIECE)
                # check if player 2 won 
                if winning_move(board=board,piece=PLAYER_PIECE):
                    # print("Congrats Player 2 Won")
                    label = myFont.render("AI 1 Won",1,RED)
                    screen.blit(label,(40,10))
                    game_over = True
                # print_board(board)
                draw_board(board=board)
            else:
                turn = 0

                
        if turn == AI and not game_over and (cat ==1 or cat ==2 ) and cat !=3 :
            print("pasok2")
                # Player 2  
            # posX = event.pos[0]
            # # col = int(input("Player 2 Make your Selection (0-6) :"))
            # col = int(math.floor(posX/SQUARESIZE))
            # col = random.randint(0,COLUMN_COUNT-1)
            # col = pick_best_move(board=board,piece=AI_PIECE)
            col,minimax_score = minimax(board=board,depth=5,alpha=-math.inf,beta=math.inf,maximizingPlayer=True)
            turn = 0

            if is_valid_location(board=board,col=col):
                # pygame.time.wait(1000)
                row = get_next_open_row(board=board,col=col)
                drop_piece(board=board, row=row,col=col,piece=AI_PIECE)
                # check if player 2 won 
                if winning_move(board=board,piece=AI_PIECE):
                    # print("Congrats Player 2 Won")
                    label = myFont.render("AI 2 Won" if cat ==2 else "AI Won",1,GREEN)
                    screen.blit(label,(40,10))
                    game_over = True
                # print_board(board)
                draw_board(board=board)
            else:
                turn = 1
            # turn+= 1
            # turn%=2
        
        # check if the game is over
        if game_over :
            pygame.time.wait(3000)

pygame.time.wait(3000)