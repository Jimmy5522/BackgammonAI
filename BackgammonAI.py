import pygame
import random
import time
import copy

def main():
    
    #ONLY SET TO FALSE IF USING RunXTimes.py SCRIPT
    user_playing = True #dictates whether the user will play or two AIs will play against each other
    show_hitboxes = False #dictates wether to show the hitboxes of the piece locations
    first_utility = utility_best #white AI
    second_utility = utility_experiment #black AI, if player is not playing


    random.seed
    
    pygame.init()

    if user_playing:
        pygame.display.set_caption("Backgammon")
        screen = pygame.display.set_mode((1080,720))
        board = pygame.transform.scale(pygame.image.load("board.png"), (1080, 720))
        font = pygame.font.Font(None, 48)
        white = pygame.Surface((50, 50))
        black = pygame.Surface((50, 50))
        hold_piece = pygame.Surface((50, 50))

        #Choosing an arbitrary color for the Surface background, will be transparent later
        surface_background = pygame.Color(65, 65, 65)

        #fill Surfaces with background color
        white.fill(surface_background)
        black.fill(surface_background)
        hold_piece.fill(surface_background)

        #make background transparent
        white.set_colorkey(surface_background)
        black.set_colorkey(surface_background)
        hold_piece.set_colorkey(surface_background)

        #draw object onto Surface pygame.Rect(927, 29, 50, 250)
        pygame.draw.circle(white, pygame.Color(255, 255, 255), (25, 25), 25)
        pygame.draw.circle(white, pygame.Color(0, 0, 0), (25, 25), 25, 2)#outline

        pygame.draw.circle(black, pygame.Color(0, 0, 0), (25, 25), 25)
        pygame.draw.circle(black, pygame.Color(255, 255, 255), (25, 25), 25, 2)#outline
        pygame.draw.circle(hold_piece, pygame.Color(100, 100, 100), (25, 25), 25)
        pygame.draw.circle(hold_piece, pygame.Color(150, 150, 150), (25, 25), 25)

    #initial board state of the game
    #first and last spots are for when a piece is in the end bin
    #positive is black, negative is white
    board_state_lst = [0,
                       2, 0, 0, 0, 0, -5,
                       0, -3, 0, 0, 0, 5,
                       -5, 0, 0, 0, 3, 0,
                       5, 0, 0, 0, 0, -2,
                       0]

    if user_playing:
        board_hitbox_lst = [pygame.Rect(998, 29, 62, 332),#white end zone

                            #white home section
                            pygame.Rect(927, 29, 50, 250),
                            pygame.Rect(847, 29, 50, 250),
                            pygame.Rect(768, 29, 50, 250),
                            pygame.Rect(683, 29, 50, 250),
                            pygame.Rect(603, 29, 50, 250),
                            pygame.Rect(524, 29, 50, 250),

                            #upper outer board section
                            pygame.Rect(434, 29, 50, 250),
                            pygame.Rect(354, 29, 50, 250),
                            pygame.Rect(274, 29, 50, 250),
                            pygame.Rect(189, 29, 50, 250),
                            pygame.Rect(110, 29, 50, 250),
                            pygame.Rect(30, 29, 50, 250),

                            #lower outer board section
                            pygame.Rect(30, 442, 50, 250),
                            pygame.Rect(110, 442, 50, 250),
                            pygame.Rect(189, 442, 50, 250),
                            pygame.Rect(274, 442, 50, 250),
                            pygame.Rect(354, 442, 50, 250),
                            pygame.Rect(434, 442, 50, 250),
                        
                            #black home section
                            pygame.Rect(524, 442, 50, 250),
                            pygame.Rect(603, 442, 50, 250),
                            pygame.Rect(683, 442, 50, 250),
                            pygame.Rect(768, 442, 50, 250),
                            pygame.Rect(847, 442, 50, 250),
                            pygame.Rect(927, 442, 50, 250),

                            #black end zone
                            pygame.Rect(998, 360, 62, 332)]

    #represents pieces on the bar
    black_bar_hitbox = pygame.Rect(478, 290, 50, 70)
    black_bar = 0
    
    white_bar_hitbox = pygame.Rect(478, 360, 50, 70)
    white_bar = 0
    
    running = True
    holding_piece = False

    

    if user_playing:
        rolls = roll_dice()
    else:
        rolls = [0, 0, 0, 0] #initializes dice to 0 to satisfy AI turn start condition
    while running:
        
        #check if someone won
        if black_won(board_state_lst):
            if user_playing:
                print("Black Wins!")
            else:
                f = open("BlackWins.txt", "r")
                val = f.read()
                f.close()

            
                f = open("BlackWins.txt", "w")
                f.write(str(int(val) + 1))
                f.close()
            running = False
        elif white_won(board_state_lst):
            if user_playing:
                print("White wins!")
            running = False
        else:

            
            
            
            #event handling
            for event in pygame.event.get():
                #quit
                if event.type == pygame.QUIT:
                    running = False

                #clicked the mouse and user is playing
                if user_playing and event.type == pygame.MOUSEBUTTONDOWN:

                    #get which hitbox was clicked
                    index_clicked_on = get_hitbox_clicked(board_hitbox_lst, black_bar_hitbox, white_bar_hitbox)

                    if index_clicked_on != -77: #value indicates no hitbox
                        #picking up piece
                        if not holding_piece:
                            start = index_clicked_on
                            holding_piece = True

                            #dropping a piece
                        else:
                            if (((index_clicked_on - start) in rolls) or overshooting_exit('b', rolls, board_state_lst, black_bar, white_bar, index_clicked_on, start)) or (start== -1 and index_clicked_on in rolls):
                                if overshooting_exit('b', rolls, board_state_lst, black_bar, white_bar, index_clicked_on, start):

                                    for i in range(len(rolls)):
                                       if rolls[i] > index_clicked_on - start:
                                           rolls[i] = index_clicked_on - start

                                if check_legal_move('b', start, rolls[rolls.index(index_clicked_on - start)], board_state_lst, black_bar, white_bar):
                                    
                                    black_bar, white_bar = move('b', start, rolls[rolls.index(index_clicked_on - start)], board_state_lst, black_bar, white_bar)

                                    #roll has been used
                                    rolls[rolls.index(index_clicked_on - start)] = 0
                            
                            holding_piece = False

            if get_valid_moves('b', rolls, board_state_lst, black_bar, white_bar) == []:
                rolls = roll_dice()
                
                black_bar, white_bar = AI_turn('w', rolls, board_state_lst, black_bar, white_bar, first_utility) #AI white player
                
                if user_playing:
                    rolls = roll_dice()

            if not user_playing and get_valid_moves('w', rolls, board_state_lst, black_bar, white_bar) == []:
                rolls = roll_dice()
                black_bar, white_bar = AI_turn('b', rolls, board_state_lst, black_bar, white_bar, second_utility) #AI black player

            if user_playing:
                
                #all Surfaces for displaying
                screen.blit(board, (0,0))
                draw_pieces(screen, board_state_lst, board_hitbox_lst, white, black, black_bar, white_bar, black_bar_hitbox, white_bar_hitbox)
                draw_rolls(screen, rolls, font)
            
                #display placeholder circle if player is holding a piece
                if holding_piece:
                    x, y = pygame.mouse.get_pos()
                    screen.blit(hold_piece,(x - 25, y - 25))
                if show_hitboxes:
                    #shows hitboxes for debugging purposes
                    for r in board_hitbox_lst:
                        pygame.draw.rect(screen, pygame.Color(75, 225, 75), r, 3)
                    pygame.draw.rect(screen, pygame.Color(75, 225, 75), black_bar_hitbox, 3)
                    pygame.draw.rect(screen, pygame.Color(75, 225, 75), white_bar_hitbox, 3)

                #update screen
                pygame.display.flip()

def roll_dice():
    vals = [1, 2, 3, 4, 5, 6]

    #Roll 2 stardard dice
    a = random.choice(vals)
    b = random.choice(vals)

    #If the rolls are the same, you get 4 moves
    if a == b:
        c = a
        d = a
    else:
        c = 0
        d = 0
    
    return [a, b, c, d]


def draw_pieces(screen, board_state_lst, board_hitbox_lst, white, black, black_bar, white_bar, black_bar_hitbox, white_bar_hitbox):

    i = 0
    while i < len(board_state_lst):
        j = 0
        while j != board_state_lst[i]:

            if i < 13:
                y = board_hitbox_lst[i].y + (abs(j) * 20)
            else:
                y = board_hitbox_lst[i].y + board_hitbox_lst[i].height - 50  - (abs(j) * 20)#50 is height of circle
            
            if board_state_lst[i] < 0:#negative value indicates white
                screen.blit(white, (board_hitbox_lst[i].x, y))
                j -= 1
            else:#positive value indicates black
                screen.blit(black, (board_hitbox_lst[i].x, y))
                j += 1
        i += 1

    #draw black bar pieces
    i = 0
    while i < black_bar:
        y = black_bar_hitbox.y + (i * 20)
        screen.blit(black, (black_bar_hitbox.x, y))
        i += 1

    #draw white bar pieces
    i = 0
    while i > white_bar :
        y = white_bar_hitbox.y + white_bar_hitbox.height - 50 - (i * 20)
        screen.blit(white, (white_bar_hitbox.x, y))
        i -= 1

def check_legal_move(color, start_space, roll, board_state, black_bar, white_bar):

    if roll == 0:
        return False
    #check to see if there is a black piece on starting space
    if color == 'b':
        
        #piece on bar, but did not move it
        if black_bar > 0 and start_space != 0:
            return False

        #clicked bar, but nothing there
        if start_space == 0 and black_bar  <= 0:
            return False

        #clicked opposing bar or final bin
        if start_space == 25:
            return False

        #checking to make sure there's a black piece on the start space
        if not (board_state[start_space] >= 1 or (start_space == 0 and black_bar >= 1)):
            return False

        #trying to overshoot a piece off the board
        if in_final_stage(color, board_state, black_bar, white_bar) and (start_space + roll) > 25:
            if roll > (25 - get_last_piece_location(color, board_state, black_bar, white_bar)):
                return True
            else:
                return False
            
        #trying to move a piece off the board exactly
        if in_final_stage(color, board_state, black_bar, white_bar) and start_space + roll == 25:
            return True
        #trying to move a piece normally
        elif start_space + roll < 25 and board_state[start_space + roll] >= -1:
            return True
        else:
            return False

    elif(color == 'w'):

        #piece on bar, but did not move it
        if white_bar < 0 and start_space != 25:
            return False

        #clicked bar, but nothing there
        if start_space == 25 and white_bar >= 0:
            return False

        #clicked opposing bar or final bin
        if start_space == 0:
            return False

        #checking to see if there's a white piece in the starting space
        if not (board_state[start_space] <= -1 or (start_space == 25 and white_bar <= -1)):
           return False

        
        #trying to overshoot a piece off the board
        if in_final_stage(color, board_state, black_bar, white_bar) and start_space - roll < 0:
            if roll > (get_last_piece_location(color, board_state, black_bar, white_bar)):
                return True
            else:
                return False
        #trying to move a piece off the board exactly
        elif in_final_stage(color, board_state, black_bar, white_bar) and start_space - roll == 0:
            return True

        #trying to move a piece normally
        elif start_space - roll >= 1 and board_state[start_space - roll] <= 1:
            return True
        else:
            return False
        
    else:
        return False

def in_final_stage(color, board_state, black_bar, white_bar):
    if color=='b':
        if get_last_piece_location(color, board_state, black_bar, white_bar) >= 19:
            return True
        else:
            return False
    else:
        if get_last_piece_location(color, board_state, black_bar, white_bar) <= 6:
            return True
        else:
            return False

def get_last_piece_location(color, board_state, black_bar, white_bar):
    
    if color=='b':
        if black_bar > 0:
            return 0

        i = 0
        while i < len(board_state) - 1 and board_state[i] <= 0:#iterates until it gets to either a black piece or the start of the board
            i += 1
        return i
    elif color=='w':
        if white_bar < 0:
            return 25
        
        i = len(board_state) - 1
        while i > 0 and board_state[i] >= 0:#iterates until it gets to either a white piece or the end of the board
            i -= 1
        return i

def move(color, start_space, roll, board_state, black_bar, white_bar):
    if color=='b':
        
        #if its on the bar
        if start_space == 0:
            black_bar -= 1
        else:
            board_state[start_space] -= 1

        #overshooting the exit
        if start_space + roll > 25:
            roll = 25 - start_space
            
        #moving to an empty or black occupied space
        if board_state[start_space + roll] >= 0:
            board_state[start_space + roll] += 1

        #bumping a white piece
        elif board_state[start_space + roll] == -1:
            board_state[start_space + roll] += 2
            white_bar -= 1
        else:
            raise Exception("Attempted illegal move")

    elif color=='w':

        if start_space == 25:
            white_bar += 1
        else:
            board_state[start_space] += 1

        #overshooting the exit
        if start_space - roll < 0:
            roll = start_space


        #moving to an empty or white occupied space
        if board_state[start_space - roll] <= 0:
            board_state[start_space - roll] -= 1

        #bumping a black piece
        elif board_state[start_space - roll] == 1:
            board_state[start_space - roll] -= 2
            black_bar += 1
        else:
            raise Exception("Attempted illegal move")
    return black_bar, white_bar

#gets the hitbox clicked on. If none, returns -77
def get_hitbox_clicked(board_hitbox_lst, black_bar_hitbox, white_bar_hitbox):
    x, y = pygame.mouse.get_pos()

    #check to see if trying to move off the bar
    if black_bar_hitbox.collidepoint(x,y):
        return 0
    if white_bar_hitbox.collidepoint(x,y):
        return 25
    
    for i, r in enumerate(board_hitbox_lst):
        if r.collidepoint(x, y):
            return i
    return -77

#makes random moves
def AI_random(color, rolls, board_state, black_bar, white_bar):
    
    possible_moves = get_valid_moves(color, rolls, board_state, black_bar, white_bar)

    while possible_moves != []:
        rand_move = random.choice(possible_moves)
        black_bar, white_bar = move(color, rand_move[0], rand_move[1], board_state, black_bar, white_bar)
        rolls[rolls.index(rand_move[1])] = 0
        possible_moves = get_valid_moves(color, rolls, board_state, black_bar, white_bar)

    return black_bar, white_bar


def AI_turn(color, rolls, board_state, black_bar, white_bar, utility_function):

    a_possible_moves = get_valid_moves(color, rolls, board_state, black_bar, white_bar)

    best_move_value = -1000000 #starting low value
    best_moves = []

    if a_possible_moves != []:
        for a in a_possible_moves:
            a_temp_board = copy.copy(board_state)
            a_temp_black_bar = black_bar
            a_temp_white_bar = white_bar
            a_temp_rolls = copy.copy(rolls)

            a_temp_black_bar, a_temp_white_bar = move(color, a[0], a[1], a_temp_board, a_temp_black_bar, a_temp_white_bar)
            a_temp_rolls[a_temp_rolls.index(a[1])] = 0
            b_possible_moves = get_valid_moves(color, a_temp_rolls, a_temp_board, a_temp_black_bar, a_temp_white_bar)
            if b_possible_moves == []:
                new_move_value = utility_function(color, a_temp_board, a_temp_black_bar, a_temp_white_bar)
                if new_move_value > best_move_value:
                    best_move_value = new_move_value
                    best_moves = [a]
            else:
                for b in b_possible_moves:
                    b_temp_board = copy.copy(a_temp_board)
                    b_temp_black_bar = a_temp_black_bar
                    b_temp_white_bar = a_temp_white_bar
                    b_temp_rolls = copy.copy(a_temp_rolls)

                    b_temp_black_bar, b_temp_white_bar = move(color, b[0], b[1], b_temp_board, b_temp_black_bar, b_temp_white_bar)
                    b_temp_rolls[b_temp_rolls.index(b[1])] = 0
                    c_possible_moves = get_valid_moves(color, b_temp_rolls, b_temp_board, b_temp_black_bar, b_temp_white_bar)
                    if c_possible_moves == []:
                        new_move_value = utility_function(color, b_temp_board, b_temp_black_bar, b_temp_white_bar)
                        if new_move_value > best_move_value:
                            best_move_value = new_move_value
                            best_moves = [a, b]
                    else:
                        for c in c_possible_moves:
                            c_temp_board = copy.copy(b_temp_board)
                            c_temp_black_bar = b_temp_black_bar
                            c_temp_white_bar = b_temp_white_bar
                            c_temp_rolls = copy.copy(b_temp_rolls)

                            c_temp_black_bar, c_temp_white_bar = move(color, c[0], c[1], c_temp_board, c_temp_black_bar, c_temp_white_bar)
                            c_temp_rolls[c_temp_rolls.index(c[1])] = 0
                            d_possible_moves = get_valid_moves(color, c_temp_rolls, c_temp_board, c_temp_black_bar, c_temp_white_bar)
                            if d_possible_moves == []:
                                new_move_value = utility_function(color, c_temp_board, c_temp_black_bar, c_temp_white_bar)
                                if new_move_value > best_move_value:
                                    best_move_value = new_move_value
                                    best_moves = [a, b, c]
                            else:
                                for d in d_possible_moves:
                                    d_temp_board = copy.copy(c_temp_board)
                                    d_temp_black_bar = c_temp_black_bar
                                    d_temp_white_bar = c_temp_white_bar
                                    d_temp_rolls = copy.copy(c_temp_rolls)

                                    d_temp_black_bar, d_temp_white_bar = move(color, d[0], d[1], d_temp_board, d_temp_black_bar, d_temp_white_bar)
                                    d_temp_rolls[d_temp_rolls.index(d[1])] = 0

                                    new_move_value = utility_function(color, d_temp_board, d_temp_black_bar, d_temp_white_bar)
                                    if new_move_value > best_move_value:
                                        best_move_value = new_move_value
                                        best_moves = [a, b, c, d]
    for m in best_moves:
        black_bar, white_bar = move(color, m[0], m[1], board_state, black_bar, white_bar)
        rolls[rolls.index(m[1])] = 0
    return black_bar, white_bar
                
            

def utility_experiment(color, board_state, black_bar, white_bar):

    #values to be edited for decision making
    opponent_bar_reward = 60
    lone_piece_punishment = 2
    home_board_piece_reward = 5
    final_bin_piece_reward = 10
    piece_location_multiplier = .5

    value = 0
    if color == 'b':
        value += abs(white_bar) * opponent_bar_reward #rewarded for white bar pieces
        for i, b in enumerate(board_state):
            if b > 0:
                value += i * b * piece_location_multiplier #adds value based on how close to the end the black pieces are

                if i > 18: #adds value for moving pieces into home area
                    value += home_board_piece_reward
                if i == 25: #adds value for moving pieces into final bin
                    value += final_bin_piece_reward
                    
                if b == 1:
                    if get_last_piece_location('w', board_state, black_bar, white_bar) > i: #checks to see if a piece is able to capture the lone piece. If not, then no penalty
                        value -= lone_piece_punishment  * i #punishment for leaving a piece unattended
    else:
        value += abs(black_bar) * opponent_bar_reward #rewarded for black bar pieces
        for i, b in enumerate(board_state):
            if b < 0 :
                value += (25 - i) * abs(b) * piece_location_multiplier #adds value based on how close to the end the white pieces are
                if i < 7: #adds value for moving pieces into home area
                    value += home_board_piece_reward
                if i == 0: #adds value for moving pieces into final bin
                    value += final_bin_piece_reward
                if b == -1:
                    if get_last_piece_location('b', board_state, black_bar, white_bar) < i: #checks to see if a piece is able to capture the lone piece. If not, then no penalty
                        value -= lone_piece_punishment * (25 - i) #punishment for leaving a piece unattended
    return value

def utility_best(color, board_state, black_bar, white_bar):

    #values to be edited for decision making
    #these are the values with the highest win rate
    opponent_bar_reward = 60
    lone_piece_punishment = 2
    home_board_piece_reward = 5
    final_bin_piece_reward = 10
    piece_location_multiplier = .1

    value = 0
    
    if color == 'b':
        value += abs(white_bar) * opponent_bar_reward #rewarded for white bar pieces
        for i, b in enumerate(board_state):
            if b > 0:
                value += i * b * piece_location_multiplier #adds value based on how close to the end the black pieces are

                if i > 18: #adds value for moving pieces into home area
                    value += home_board_piece_reward
                if i == 25: #adds value for moving pieces into final bin
                    value += final_bin_piece_reward
                    
                if b == 1:
                    if get_last_piece_location('w', board_state, black_bar, white_bar) > i: #checks to see if a piece is able to capture the lone piece. If not, then no penalty
                        value -= lone_piece_punishment * i #punishment for leaving a piece unattended
    else:
        value += abs(black_bar) * opponent_bar_reward #rewarded for black bar pieces
        for i, b in enumerate(board_state):
            #if(b > 0):
                #value -= i * b #subtracts value based on how close to the end the black pieces are
            if b < 0:
                value += (25 - i) * abs(b) * piece_location_multiplier #adds value based on how close to the end the white pieces are
                if i < 7: #adds value for moving pieces into home area
                    value += home_board_piece_reward
                if i == 0: #adds value for moving pieces into final bin
                    value += final_bin_piece_reward
                if b == -1:
                    if get_last_piece_location('b', board_state, black_bar, white_bar) < i: #checks to see if a piece is able to capture the lone piece. If not, then no penalty
                        value -= lone_piece_punishment * (25 - i)#punishment for leaving a piece unattended
    return value


def get_valid_moves(color, rolls, board_state, black_bar, white_bar):
    lst = []
    for r in rolls:
        if r != 0:
            for i in range(len(board_state)):
                if check_legal_move(color, i, r, board_state, black_bar, white_bar):
                    lst.append((i, r))
    return lst

def overshooting_exit(color, rolls, board_state, black_bar, white_bar, index_clicked_on, start):
    if color=='b':
        if index_clicked_on == 25 and in_final_stage(color, board_state, black_bar, white_bar):
            if max(rolls) > (index_clicked_on - start) and start == get_last_piece_location(color, board_state, black_bar, white_bar):
                return True
    else:
        if index_clicked_on == 0 and in_final_stage(color, board_state, black_bar, white_bar):
            if max(rolls) > (start - index_clicked_on) and start == get_last_piece_location(color, board_state, black_bar, white_bar):
                return True
    return False

def black_won(board_state):
    return board_state[25] == 15 #all black pieces are in the black bin

def white_won(board_state):
    return board_state[0] == -15 #all white pieces are in the white bin

def draw_rolls(screen, rolls, font):
    rolls_str = 'Rolls: '
    for r in rolls:
        if r != 0:
            rolls_str += str(r) + ' '
        else:
            rolls_str += '   '

    text = font.render(rolls_str, True, pygame.Color(0, 0, 0))
    textRect = text.get_rect()
    textRect.center = 620, 355
    screen.blit(text, textRect)


if __name__=="__main__":
    main()
