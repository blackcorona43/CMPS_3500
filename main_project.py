# course: CMPS3500
# CLASS Project
# PYTHON IMPLEMENTATION: BASIC DATA ANALYSIS
# date: 12/08/23
# Group number: 6
# Student 1: Galo De Paula Jimenez
# Student 2: Ruben Corona
# Student 3: Estevan Arroyo
# description: Implementation Basic Data Analysis Routines

# two player chess in python with Pygame!
# pawn double space checking
# castling
# en passant
# pawn promotion

import pygame
import random
import sys
from itertools import combinations
import os

# current directory
dirname = os.path.dirname(__file__)

WIDTH = 800
ROWS = 8

RED= pygame.image.load(os.path.join(dirname, 'images/red.png'))
GREEN= pygame.image.load(os.path.join(dirname, 'images/green.png'))

REDKING = pygame.image.load(os.path.join(dirname, 'images/redking.png'))
GREENKING = pygame.image.load(os.path.join(dirname, 'images/greenking.png'))

# images for the play button and checkers button
#CHESS_BOARD = pygame.image.load(os.path.join(dirname, 'images/chessBackground.jpg'))
TITLE_SCREEN_BG = pygame.image.load(os.path.join(dirname, 'images/title_screen.jpg'))
# this button is for checkers
CHECKERS_BUTTON = pygame.image.load(os.path.join(dirname, 'images/play_button.jpg'))
CHECKERS_BUTTON = pygame.transform.scale(CHECKERS_BUTTON, (150, 50))

#this button is for the chess game
CHESS_BUTTON = pygame.image.load(os.path.join(dirname, 'images/black king.png'))
CHESS_BUTTON = pygame.transform.scale(CHESS_BUTTON, (150, 50))

#button to quit game
QUIT_BUTTON = pygame.image.load(os.path.join(dirname, 'images/quit_button.png'))
QUIT_BUTTON = pygame.transform.scale(QUIT_BUTTON, (150, 50))

WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (235, 168, 52)
BLUE = (76, 252, 241)

pygame.init()
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Checkers')
help_menu_displayed = False

# Font settings for the help screen
HELP_FONT = pygame.font.Font(None, 36)
HELP_TEXT = [
    "Buttons:",
    "Press ESC to go back to the main menu.",
    "Press R to reset the game.",
    "Press 'H' to close this help screen.",
]

# makes a title screen to play checkers or chess
def title_screen():
    WIN.blit(TITLE_SCREEN_BG, (0, 0))
    WIN.blit(CHECKERS_BUTTON, (WIDTH // 4, 200))
    WIN.blit(CHESS_BUTTON, (WIDTH // 4, 400))
    WIN.blit(QUIT_BUTTON, (WIDTH // 4, 500))
    pygame.display.update()
    
# makes a help screen with ESC, R as options
def help_screen(win,rows,width):
    global help_menu_displayed
    # Draw a semi-transparent background
    pygame.draw.rect(WIN, (0, 0, 0, 150), (0, 0, WIDTH, WIDTH))

    # Draw a rectangle for the help box
    help_rect = pygame.Rect(WIDTH // 4, 100, WIDTH // 2, 300)
    pygame.draw.rect(WIN, WHITE, help_rect)

    # Render and display the help text
    for i, line in enumerate(HELP_TEXT):
        text_surface = HELP_FONT.render(line, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 150 + i * 40))
        WIN.blit(text_surface, text_rect)

    pygame.display.update()

# Creates the Main menu from where chess and checkers can be chosen
def main_menu():
    # Main Loop
    while True:
        title_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()

                # Check if the play button is clicked - Starts checkers
                if WIDTH // 4 < mouseX < WIDTH // 4 + CHECKERS_BUTTON.get_width() and \
                        200 < mouseY < 200 + CHECKERS_BUTTON.get_height():
                    checkers_game()
                
                # Check if the play button is clicked - Starts Chess
                if WIDTH // 4 < mouseX < WIDTH // 4 + CHESS_BUTTON.get_width() and \
                        400 < mouseY < 400 + CHESS_BUTTON.get_height():
                    chess_game()

                # Check if the quit button is clicked
                elif WIDTH // 4 < mouseX < WIDTH // 4 + QUIT_BUTTON.get_width() and \
                        500 < mouseY < 500 + QUIT_BUTTON.get_height():
                    pygame.quit()
                    sys.exit()

        pygame.display.update()    


"""
Function to manage the main logic of a chess game.
This function sets up the game board, handles player moves, checks for checkmate 
conditions, and manages the overall flow of the game. 
"""
def chess_game():
    pygame.init()
    global help_menu_displayed
    WIDTH = 1000
    HEIGHT = 900
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Two-Player Pygame Chess!')
    font = pygame.font.Font('freesansbold.ttf', 20)
    HELP_FONT = pygame.font.Font(None,36)
    medium_font = pygame.font.Font('freesansbold.ttf', 40)
    big_font = pygame.font.Font('freesansbold.ttf', 50)
    timer = pygame.time.Clock()
    fps = 60
    # game variables and images
    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
    captured_pieces_white = []
    captured_pieces_black = []
    
    # 0 - whites turn no selection: 
    # 1-whites turn piece selected: 
    # 2- black turn no selection, 
    # 3 - black turn piece selected
    
    turn_step = 0
    selection = 100
    valid_moves = []

    # load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
    black_queen = pygame.image.load('images/black queen.png')
    black_queen = pygame.transform.scale(black_queen, (80, 80))
    black_queen_small = pygame.transform.scale(black_queen, (45, 45))
    black_king = pygame.image.load('images/black king.png')
    black_king = pygame.transform.scale(black_king, (80, 80))
    black_king_small = pygame.transform.scale(black_king, (45, 45))
    black_rook = pygame.image.load('images/black rook.png')
    black_rook = pygame.transform.scale(black_rook, (80, 80))
    black_rook_small = pygame.transform.scale(black_rook, (45, 45))
    black_bishop = pygame.image.load('images/black bishop.png')
    black_bishop = pygame.transform.scale(black_bishop, (80, 80))
    black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
    black_knight = pygame.image.load('images/black knight.png')
    black_knight = pygame.transform.scale(black_knight, (80, 80))
    black_knight_small = pygame.transform.scale(black_knight, (45, 45))
    black_pawn = pygame.image.load('images/black pawn.png')
    black_pawn = pygame.transform.scale(black_pawn, (65, 65))
    black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
    white_queen = pygame.image.load('images/white queen.png')
    white_queen = pygame.transform.scale(white_queen, (80, 80))
    white_queen_small = pygame.transform.scale(white_queen, (45, 45))
    white_king = pygame.image.load('images/white king.png')
    white_king = pygame.transform.scale(white_king, (80, 80))
    white_king_small = pygame.transform.scale(white_king, (45, 45))
    white_rook = pygame.image.load('images/white rook.png')
    white_rook = pygame.transform.scale(white_rook, (80, 80))
    white_rook_small = pygame.transform.scale(white_rook, (45, 45))
    white_bishop = pygame.image.load('images/white bishop.png')
    white_bishop = pygame.transform.scale(white_bishop, (80, 80))
    white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
    white_knight = pygame.image.load('images/white knight.png')
    white_knight = pygame.transform.scale(white_knight, (80, 80))
    white_knight_small = pygame.transform.scale(white_knight, (45, 45))
    white_pawn = pygame.image.load('images/white pawn.png')
    white_pawn = pygame.transform.scale(white_pawn, (65, 65))
    white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))
    white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
    white_promotions = ['bishop', 'knight', 'rook', 'queen']
    white_moved = [False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False]
    small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                        white_rook_small, white_bishop_small]
    black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
    small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                        black_rook_small, black_bishop_small]
    black_promotions = ['bishop', 'knight', 'rook', 'queen']
    black_moved = [False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False]
    piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
    
    # check variables/ flashing counter
    counter = 0
    winner = ''
    game_over = False
    white_ep = (100, 100)
    black_ep = (100, 100)
    white_promote = False
    black_promote = False
    promo_index = 100
    check = False
    castling_moves = []

    # draw main game board
    def draw_board():
        for i in range(32):
            # draws 32 squares for board
            column = i % 4
            row = i // 4
            if row % 2 == 0:
                pygame.draw.rect(screen, 'light gray', [500 - (column * 200), row * 100, 100, 100])
            else:
                pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
            # draws the boarder to the board and the screen
            pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
            pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
            pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
            # statues text that displays players turn (Black or white)
            status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                        'Black: Select a Piece to Move!', 'Black: Select a Destination!']
            screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
            # draws grid lines for squares on board
            for i in range(9):
                pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
                pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
            # draws FORFEIT button
            screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))
            # draws pawn promotion if appropriate
            if white_promote or black_promote:
                pygame.draw.rect(screen, 'gray', [0, 800, WIDTH - 200, 100])
                pygame.draw.rect(screen, 'gold', [0, 800, WIDTH - 200, 100], 5)
                screen.blit(big_font.render('Select Piece to Promote Pawn', True, 'black'), (20, 820))

    # draw pieces onto board
    def draw_pieces():
        # Draw White Pieces
        for i in range(len(white_pieces)):
            # Determine the index of the current white piece
            index = piece_list.index(white_pieces[i])
            # Draw white piece
            if white_pieces[i] == 'pawn':
                screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
            else:
                screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
            # Highlight the selected white piece White's turn
            if turn_step < 2:
                if selection == i:
                    pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                    100, 100], 2)

         # Draw Black Pieces
        for i in range(len(black_pieces)):
            # Determine the index of the current black piece
            index = piece_list.index(black_pieces[i])
            # Draw black piece
            if black_pieces[i] == 'pawn':
                screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
            else:
                screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
            # Highlight the selected white piece blacks's turn
            if turn_step >= 2:
                if selection == i:
                    pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                                                    100, 100], 2)

    # this function iterates through each piece on the board, determines its 
    # type, and calls the corresponding function to calculate its valid moves. 
    def check_options(pieces, locations, turn):
        global castling_moves
        moves_list = []
        all_moves_list = []
        castling_moves = []
        for i in range((len(pieces))):
            location = locations[i]
            piece = pieces[i]
            if piece == 'pawn':
                moves_list = check_pawn(location, turn)
            elif piece == 'rook':
                moves_list = check_rook(location, turn)
            elif piece == 'knight':
                moves_list = check_knight(location, turn)
            elif piece == 'bishop':
                moves_list = check_bishop(location, turn)
            elif piece == 'queen':
                moves_list = check_queen(location, turn)
            elif piece == 'king':
                moves_list, castling_moves = check_king(location, turn)
            all_moves_list.append(moves_list)
        return all_moves_list

    # check king valid moves
    def check_king(position, color):
        moves_list = []
        castle_moves = check_castling()
        if color == 'white':
            enemies_list = black_locations
            friends_list = white_locations
        else:
            friends_list = black_locations
            enemies_list = white_locations
        # 8 squares to check for kings, they can go one square any direction
        targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
        for i in range(8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_list.append(target)
        return moves_list, castle_moves

    # check queen valid moves
    def check_queen(position, color):
        moves_list = check_bishop(position, color)
        second_list = check_rook(position, color)
        for i in range(len(second_list)):
            moves_list.append(second_list[i])
        return moves_list

    # check bishop moves
    def check_bishop(position, color):
        moves_list = []
        if color == 'white':
            enemies_list = black_locations
            friends_list = white_locations
        else:
            friends_list = black_locations
            enemies_list = white_locations
        for i in range(4):  
            # up-right, up-left, down-right, down-left
            path = True
            chain = 1
            if i == 0:
                x = 1
                y = -1
            elif i == 1:
                x = -1
                y = -1
            elif i == 2:
                x = 1
                y = 1
            else:
                x = -1
                y = 1
            while path:
                if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                        0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return moves_list

    # check rook moves
    def check_rook(position, color):
        moves_list = []
        if color == 'white':
            enemies_list = black_locations
            friends_list = white_locations
        else:
            friends_list = black_locations
            enemies_list = white_locations
        for i in range(4):  
            # down, up, right, left
            path = True
            chain = 1
            if i == 0:
                x = 0
                y = 1
            elif i == 1:
                x = 0
                y = -1
            elif i == 2:
                x = 1
                y = 0
            else:
                x = -1
                y = 0
            while path:
                if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                        0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return moves_list

    # check valid pawn moves
    def check_pawn(position, color):
        moves_list = []
        if color == 'white':
            if (position[0], position[1] + 1) not in white_locations and \
                    (position[0], position[1] + 1) not in black_locations and position[1] < 7:
                moves_list.append((position[0], position[1] + 1))
                # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
                if (position[0], position[1] + 2) not in white_locations and \
                        (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                    moves_list.append((position[0], position[1] + 2))
            if (position[0] + 1, position[1] + 1) in black_locations:
                moves_list.append((position[0] + 1, position[1] + 1))
            if (position[0] - 1, position[1] + 1) in black_locations:
                moves_list.append((position[0] - 1, position[1] + 1))
            # add en passant move checker
            if (position[0] + 1, position[1] + 1) == black_ep:
                moves_list.append((position[0] + 1, position[1] + 1))
            if (position[0] - 1, position[1] + 1) == black_ep:
                moves_list.append((position[0] - 1, position[1] + 1))
        else:
            if (position[0], position[1] - 1) not in white_locations and \
                    (position[0], position[1] - 1) not in black_locations and position[1] > 0:
                moves_list.append((position[0], position[1] - 1))
                # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
                if (position[0], position[1] - 2) not in white_locations and \
                        (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                    moves_list.append((position[0], position[1] - 2))
            if (position[0] + 1, position[1] - 1) in white_locations:
                moves_list.append((position[0] + 1, position[1] - 1))
            if (position[0] - 1, position[1] - 1) in white_locations:
                moves_list.append((position[0] - 1, position[1] - 1))
            # add en passant move checker
            if (position[0] + 1, position[1] - 1) == white_ep:
                moves_list.append((position[0] + 1, position[1] - 1))
            if (position[0] - 1, position[1] - 1) == white_ep:
                moves_list.append((position[0] - 1, position[1] - 1))
        return moves_list

    # check valid knight moves
    def check_knight(position, color):
        moves_list = []
        if color == 'white':
            enemies_list = black_locations
            friends_list = white_locations
        else:
            friends_list = black_locations
            enemies_list = white_locations
        # 8 squares to check for knights, they can go two squares in one direction and one in another
        targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        for i in range(8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_list.append(target)
        return moves_list

    # check for valid moves for just selected piece
    def check_valid_moves():
        if turn_step < 2:
            options_list = white_options
        else:
            options_list = black_options
        valid_options = options_list[selection]
        return valid_options

    # draw valid moves on screen. Red or blue circles to show moves
    def draw_valid(moves):
        if turn_step < 2:
            color = 'red'
        else:
            color = 'blue'
        for i in range(len(moves)):
            pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

    # draw captured pieces on side of screen
    def draw_captured():
        for i in range(len(captured_pieces_white)):
             # Get the type of the current captured white piece
            captured_piece = captured_pieces_white[i]
            # Find the index of the captured piece in the piece_list
            index = piece_list.index(captured_piece)
            # Blit the image of the captured white piece on the screen
            screen.blit(small_black_images[index], (825, 5 + 50 * i))
        for i in range(len(captured_pieces_black)):
            # Get the type of the current captured black piece
            captured_piece = captured_pieces_black[i]
            # Find the index of the captured piece in the piece_list
            index = piece_list.index(captured_piece)
            # Blit the image of the captured white piece on the screen
            screen.blit(small_white_images[index], (925, 5 + 50 * i))

    # draw a flashing square around king if in check
    def draw_check():
        global check
        check = False
        # Check if White's turn
        if turn_step < 2:
            if 'king' in white_pieces:
                # Find the index of the white king in the list of white pieces
                king_index = white_pieces.index('king')
                # Get the location of the white king on the board
                king_location = white_locations[king_index]

                # Check if the white king is in check
                for i in range(len(black_options)):
                    if king_location in black_options[i]:
                        check = True
                        # Flashing effect: Draw a dark red square around the white king
                        if counter < 15:
                            pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                                white_locations[king_index][1] * 100 + 1, 100, 100], 5)
        else:
            # Check if blacks's turn
            if 'king' in black_pieces:
                king_index = black_pieces.index('king')
                king_location = black_locations[king_index]
                # Check if black king in check
                for i in range(len(white_options)):
                    if king_location in white_options[i]:
                        # Flashing effect
                        check = True
                        if counter < 15:
                            pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                                black_locations[king_index][1] * 100 + 1, 100, 100], 5)

    #draw color winner and present option to restart
    def draw_game_over():
        pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
        screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
        screen.blit(font.render(f'Press R to Restart!', True, 'white'), (210, 240))

    # check en passant
    def check_ep(old_coords, new_coords):
        # Check if it's White's turn or the initial moves of the game
        if turn_step <= 1:
            # If White's turn or the initial moves, find the index of the piece in white_locations
            index = white_locations.index(old_coords)
            # Calculate en passant coordinates for White
            ep_coords = (new_coords[0], new_coords[1] - 1)
             # Get the type of the piece
            piece = white_pieces[index]
        else:
            # Same as above but for black
            index = black_locations.index(old_coords)
            ep_coords = (new_coords[0], new_coords[1] + 1)
            piece = black_pieces[index]
        if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
            # if piece was pawn and moved two spaces, return EP coords as defined above
            pass
        else:
            # If not, set en passant coordinates to (100, 100)
            ep_coords = (100, 100)
        return ep_coords

    # add castling
    def check_castling():
        castle_moves = []  # store each valid castle move as [((king_coords), (castle_coords))]
        rook_indexes = []
        rook_locations = []
        king_index = 0
        king_pos = (0, 0)
        # Check if it's Black's turn
        if turn_step > 1:
             # Loop through white pieces to search for rook and king in white squares
            for i in range(len(white_pieces)):
                if white_pieces[i] == 'rook':
                    rook_indexes.append(white_moved[i])
                    rook_locations.append(white_locations[i])
                if white_pieces[i] == 'king':
                    king_index = i
                    king_pos = white_locations[i]
            # Check if the king hasn't moved and there are unmoved rooks, and the king is not in check
            if not white_moved[king_index] and False in rook_indexes and not check:
                # loop to look for rooks
                for i in range(len(rook_indexes)):
                    castle = True
                    # Check the side of the board the rook is on and set empty squares accordingly
                    if rook_locations[i][0] > king_pos[0]:
                        empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                        (king_pos[0] + 3, king_pos[1])]
                    else:
                        empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                    # Check if the squares are empty and not under attack
                    for j in range(len(empty_squares)):
                        if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                                empty_squares[j] in black_options or rook_indexes[i]:
                            castle = False
                    if castle:
                        castle_moves.append((empty_squares[1], empty_squares[0]))
        else:
            # Loop through black rook and king
            for i in range(len(black_pieces)):
                if black_pieces[i] == 'rook':
                    rook_indexes.append(black_moved[i])
                    rook_locations.append(black_locations[i])
                if black_pieces[i] == 'king':
                    king_index = i
                    king_pos = black_locations[i]
            # Check if the king hasn't moved and there are unmoved rooks, and the king is not in check
            if not black_moved[king_index] and False in rook_indexes and not check:
                for i in range(len(rook_indexes)):
                    castle = True
                     # Check the side of the board the rook is on and set empty squares accordingly
                    if rook_locations[i][0] > king_pos[0]:
                        empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                        (king_pos[0] + 3, king_pos[1])]
                    else:
                        empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                     # Check if the squares are empty and not under attack
                    for j in range(len(empty_squares)):
                        if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                                empty_squares[j] in white_options or rook_indexes[i]:
                            castle = False
                    # If castling is valid, add the move to castle_moves
                    if castle:
                        castle_moves.append((empty_squares[1], empty_squares[0]))
        return castle_moves

    def draw_castling(moves):
        # Determine the color based on the turn
        if turn_step < 2:
            color = 'red'
        else:
            color = 'blue'
        # Loop through each castling move in the list of moves
        for i in range(len(moves)):
            pygame.draw.circle(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70), 8)
            screen.blit(font.render('king', True, 'black'), (moves[i][0][0] * 100 + 30, moves[i][0][1] * 100 + 70))
            pygame.draw.circle(screen, color, (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 8)
            screen.blit(font.render('rook', True, 'black'),
                        (moves[i][1][0] * 100 + 30, moves[i][1][1] * 100 + 70))
            # Draw a line connecting the king and rook positions
            pygame.draw.line(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70),
                            (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 2)

    # add pawn promotion
    def check_promotion():
        pawn_indexes = []
        white_promotion = False
        black_promotion = False
        promote_index = 100
         # Loop through white pieces and Check for pawns in white pieces
        for i in range(len(white_pieces)):
            if white_pieces[i] == 'pawn':
                pawn_indexes.append(i)
        # Check for pawn promotion for white pieces
        for i in range(len(pawn_indexes)):
            # Check if pawn is at the top row
            if white_locations[pawn_indexes[i]][1] == 7:
                white_promotion = True
                promote_index = pawn_indexes[i]
        
         # Needs to reset pawn indexes for black
        pawn_indexes = []
         # Loop through black pieces and Check for pawns in white pieces
        for i in range(len(black_pieces)):
            if black_pieces[i] == 'pawn':
                pawn_indexes.append(i)
        # Check for pawn promotion for black pieces
        for i in range(len(pawn_indexes)):
            # Check if pawn is at the top row
            if black_locations[pawn_indexes[i]][1] == 0:
                black_promotion = True
                promote_index = pawn_indexes[i]
        return white_promotion, black_promotion, promote_index

    # Draw promotion box
    def draw_promotion():
        pygame.draw.rect(screen, 'dark gray', [800, 0, 200, 420])
        if white_promote:
            color = 'white'
            for i in range(len(white_promotions)):
                piece = white_promotions[i]
                index = piece_list.index(piece)
                screen.blit(white_images[index], (860, 5 + 100 * i))
        elif black_promote:
            color = 'black'
            for i in range(len(black_promotions)):
                piece = black_promotions[i]
                index = piece_list.index(piece)
                screen.blit(black_images[index], (860, 5 + 100 * i))
        pygame.draw.rect(screen, color, [800, 0, 200,420], 8)

    def check_promo_select():
        # get mouse position and check for desired piece
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        x_pos = mouse_pos[0] // 100
        y_pos = mouse_pos[1] // 100
        #check if white and update to selected piece
        if white_promote and left_click and x_pos > 7 and y_pos < 4:
            white_pieces[promo_index] = white_promotions[y_pos]
        #check if black and update to selected piece
        elif black_promote and left_click and x_pos > 7 and y_pos < 4:
            black_pieces[promo_index] = black_promotions[y_pos]

    """
    #main game loop
    """
    #store valid moves or options for black and white
    black_options = check_options(black_pieces, black_locations, 'black')
    white_options = check_options(white_pieces, white_locations, 'white')
    run = True
    while run:
        timer.tick(fps)
        if counter < 30:
            counter += 1
        else:
            counter = 0
        screen.fill('dark gray')

        # Draw the main game components
        draw_board()
        draw_pieces()
        draw_captured()
        draw_check()

        if not game_over:
            # Check if pawn promotion is needed
            white_promote, black_promote, promo_index = check_promotion()
            if white_promote or black_promote:
                # Draw promotion options and handle selection
                draw_promotion()
                check_promo_select()

        # Check if a piece is currently selected
        if selection != 100:
            # Determine valid moves for the selected piece
            valid_moves = check_valid_moves()
            # Draw valid moves on the board
            draw_valid(valid_moves)
            
            if selected_piece == 'king':
                draw_castling(castling_moves)

        # Event handling loop for user input
        for event in pygame.event.get():
            # Check if the user closes the window
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                # Get the coordinates of the mouse click
                x_coord = event.pos[0] // 100
                y_coord = event.pos[1] // 100
                click_coords = (x_coord, y_coord)

                if turn_step <= 1: #check if its blacks turn
                    if click_coords == (8, 8) or click_coords == (9, 8):#check for FORFEIT
                        winner = 'black'
                    
                    # Check if BLACK clicks on a WHITE piece
                    if click_coords in white_locations:
                        selection = white_locations.index(click_coords)
                        selected_piece = white_pieces[selection]
                        #update turn step
                        if turn_step == 0:
                            turn_step = 1
                    
                     # Check for en passant and update the board state
                    if click_coords in valid_moves and selection != 100:
                        white_ep = check_ep(white_locations[selection], click_coords)
                        white_locations[selection] = click_coords
                        white_moved[selection] = True
                        # Check if the move captures a black piece
                        if click_coords in black_locations:
                            black_piece = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces[black_piece])

                            # if black king. white winner
                            if black_pieces[black_piece] == 'king':
                                winner = 'white'

                            #remove captured black pieces
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                            black_moved.pop(black_piece)

                        # Check if en passant pawn was captured
                        if click_coords == black_ep:
                            # Find the index of the captured black pawn
                            black_piece = black_locations.index((black_ep[0], black_ep[1] - 1))
                            # Add captured black piece to the white captured pieces
                            captured_pieces_white.append(black_pieces[black_piece])

                            # Remove the captured black piece from the board
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                            black_moved.pop(black_piece)

                        #update black and white options
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 2 # set next players turn

                        # Reset selection and valid moves after the move
                        selection = 100
                        valid_moves = []

                    # Check if a piece is selected and it is a king for castling
                    elif selection != 100 and selected_piece == 'king':
                        # Iterate through castling moves to find the matching move
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
                                # Update the king's position
                                white_locations[selection] = click_coords
                                white_moved[selection] = True

                                 # Determine the rook's position based on the castling move
                                if click_coords == (1, 0):
                                    rook_coords = (0, 0)
                                else:
                                    rook_coords = (7, 0)
                                # Find the index of the rook and update its position
                                rook_index = white_locations.index(rook_coords)
                                white_locations[rook_index] = castling_moves[q][1]

                                 # Find the index of the rook and update its position
                                black_options = check_options(black_pieces, black_locations, 'black')
                                white_options = check_options(white_pieces, white_locations, 'white')
                                
                                turn_step = 2
                                selection = 100
                                valid_moves = []

                #Same logic but this time for white turn
                if turn_step > 1: # Check if it's whites turn
                    # Check if black forfeit
                    if click_coords == (8, 8) or click_coords == (9, 8):
                        winner = 'white'
                    if click_coords in black_locations:
                        selection = black_locations.index(click_coords)
                        # check what piece is selected, so you can only draw castling moves if king is selected
                        selected_piece = black_pieces[selection]
                        if turn_step == 2:
                            turn_step = 3
                    if click_coords in valid_moves and selection != 100:
                        black_ep = check_ep(black_locations[selection], click_coords)
                        black_locations[selection] = click_coords
                        black_moved[selection] = True
                        if click_coords in white_locations:
                            white_piece = white_locations.index(click_coords)
                            captured_pieces_black.append(white_pieces[white_piece])
                            if white_pieces[white_piece] == 'king':
                                winner = 'black'
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                            white_moved.pop(white_piece)
                        if click_coords == white_ep:
                            white_piece = white_locations.index((white_ep[0], white_ep[1] + 1))
                            captured_pieces_black.append(white_pieces[white_piece])
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                            white_moved.pop(white_piece)
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 0
                        selection = 100
                        valid_moves = []
                    elif selection != 100 and selected_piece == 'king':
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
                                black_locations[selection] = click_coords
                                black_moved[selection] = True
                                if click_coords == (1, 7):
                                    rook_coords = (0, 7)
                                else:
                                    rook_coords = (7, 7)
                                rook_index = black_locations.index(rook_coords)
                                black_locations[rook_index] = castling_moves[q][1]
                                black_options = check_options(black_pieces, black_locations, 'black')
                                white_options = check_options(white_pieces, white_locations, 'white')
                                turn_step = 0
                                selection = 100
                                valid_moves = []
                #end of whites turn

            # Reset when game over shows                    
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    game_over = False
                    winner = ''
                    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                    white_moved = [False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False]
                    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                    black_moved = [False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False]
                    captured_pieces_white = []
                    captured_pieces_black = []
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
            
            #Reset whenver any player wants
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    winner = ''
                    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                    white_moved = [False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False]
                    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                    black_moved = [False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False]
                    captured_pieces_white = []
                    captured_pieces_black = []
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')

            #Reset whenver any player wants to state 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_over = False
                    winner = ''
                    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    white_locations = [(0, 0), (2, 2), (4, 1), (5, 0), (7, 2), (4, 2), (5, 2), (7, 0),
                                    (0, 1), (1, 1), (2, 1), (3, 2), (4, 3), (5, 1), (6, 1), (7, 1)]
                    white_moved = [False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False]
                    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    black_locations = [(0, 7), (0, 4), (1, 5), (6, 7), (3, 7), (2, 7), (5, 5), (5, 7),
                                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 4), (5, 6), (6, 6), (7, 6)]
                    black_moved = [False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False]
                    captured_pieces_white = []
                    captured_pieces_black = []
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')

            # ESC key to quit game
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu()
            # press H for help menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    # Toggle the help_menu_displayed variable
                    help_menu_displayed = not help_menu_displayed
        
        # Render and display the help screen if it's open
        if help_menu_displayed:
            help_screen(WIN,ROWS, WIDTH)
        pygame.display.flip()
            
        # winner display message                    
        if winner != '':
            game_over = True
            draw_game_over()

        pygame.display.flip()
    pygame.quit()

"""
Function to manage the main logic of a checkers game.
This function sets up the game board, handles player moves,
checks for victory conditions, and manages the overall flow of the game.
"""
def checkers_game():
    # Set up the pygame display with a square window
    pygame.display.set_mode((WIDTH,WIDTH))
    priorMoves=[] # Initialize an empty list to store prior moves

    # Define  class "Node" to represent each square on the game board
    class Node:
        def __init__(self, row, col, width):
            self.row = row
            self.col = col
            # Calculate the pixel coordinates of the Node based on its position and width
            self.x = int(row * width)
            self.y = int(col * width)
            self.colour = WHITE # Set the initial color of the Node to WHITE
            self.piece = None

         # draws the Node on the game window
        def draw(self, WIN):
            pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / ROWS, WIDTH / ROWS)) # Draw a rectangle
             # If Node has piece, draw the piece's image on the game window at the Node
            if self.piece:
                WIN.blit(self.piece.image, (self.x, self.y))

    # this func updates the display with the current state of the game board
    def update_display(win, grid, rows, width):
        # Iterate through each row in the grid
        for row in grid:
            for spot in row:
                spot.draw(win)# Draw current spot
        # Draw the grid lines on the game window
        draw_grid(win, rows, width)
        # Update the display
        pygame.display.update()

    # this func creates the game board grid
    def make_grid(rows, width):
        grid = []
        # Calculate the gap between each spot (Node) based on the number of rows
        gap = width// rows
        count = 0
        # Iterate through each row
        for i in range(rows):
            grid.append([])
             # Iterate through each column
            for j in range(rows):
                # Create a Node at the current position with appropriate gap
                node = Node(j,i, gap)
                # Set the color of the Node based on its position
                if abs(i-j) % 2 == 0:
                    node.colour=BLACK

                 # Place red pieces on the bottom rows
                if (abs(i+j)%2==0) and (i<3):
                    node.piece = Piece('R')
                # Place green pieces on the top rows
                elif(abs(i+j)%2==0) and i>4:
                    node.piece=Piece('G')
                count+=1
                # Append the current Node to the grid
                grid[i].append(node)
        return grid

    # creates a custom game board grid with specific piece placements
    def make_grid_1(rows, width):
        grid = []         # Initialize empty grid list
        # Calculate the gap between each spot (Node) based on the number of rows
        gap = width // rows
        count = 0

        # Iterate through each row 
        for i in range(rows):
            grid.append([])     # Append empty list for the current row
            
            # Iterate through each column in the current row
            for j in range(rows):
                # Create Node at the current position with gap
                node = Node(j, i, gap)

                # Set color of the Node based on its position
                if abs(i - j) % 2 == 0:
                    node.colour = BLACK

                # Set the initial state of the grid with specific piece placements
                if i == 0:
                    if j == 0 or j == 4:
                        node.piece = Piece('R')
                elif i == 1:
                    if j == 3 or j == 5 or j == 7:
                        node.piece = Piece('R')
                elif i == 2:
                    if j == 0 or j == 6:
                        node.piece = Piece('R')
                elif i == 3:
                    if j == 1:
                        node.piece = Piece('R')
                elif i == 7:
                    if j == 3:
                        node.piece = Piece('R')
                        node.piece.type = 'KING'
                        node.piece.image = REDKING

                # Set the initial state of the grid with specific piece placements
                if i == 3:
                    if j == 3:
                        node.piece = Piece('G')
                elif i == 5:
                    if j == 1 or j == 3 or j == 7:
                        node.piece = Piece('G')
                elif i == 6:
                    if j == 0 or j == 2 or j == 6:
                        node.piece = Piece('G')

                count += 1
                # Append the current Node to the grid
                grid[i].append(node)

        # Return the completed grid
        return grid

    # DRAW grid lines on the game window
    def draw_grid(win, rows, width):
        gap = width // ROWS     # Calculate the gap between each spot 

        # Iterate through each row in the grid
        for i in range(rows):
            # Draw a horizontal line - current row
            pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
            # Iterate through each column in the current row
            for j in range(rows):
                # Draw a vertical line - current column
                pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

    # this class represents game pieces
    class Piece:
        def __init__(self, team):
            self.team = team    # Initialize the piece with its team (R or G)
            self.image = RED if self.team == 'R' else GREEN     # Set color (RED or GREEN)
            self.type = None

        # draws the piece on the game window at specified position
        def draw(self, x, y):
            WIN.blit(self.image, (x, y))


    # Function to get the grid position (row, column) of the mouse cursor
    def getNode(grid, rows, width):
        gap = width // rows                     # Calculate the gap between each spot
        RowX, RowY = pygame.mouse.get_pos()     # Get current mouse position
        
        # Calculate row and column based on the mouse position and gap
        Row = RowX // gap
        Col = RowY // gap
        return (Col, Row)

    # Counts the number of R and G pieces left
    def count_pieces(grid):
        count_red = 0
        count_green = 0
        for row in grid:        
            for spot in row:    
                # Check if the spot has a piece and increment
                if spot.piece:
                    if spot.piece.team == 'R':
                        count_red += 1
                    elif spot.piece.team == 'G':
                        count_green += 1

        # Return the counts as a tuple (count_red, count_green)
        return count_red, count_green

    #check if a player is out of pieces (lost)
    def is_player_out(grid, player):
        # Get the counts of red and green pieces on the game board
        count_red, count_green = count_pieces(grid)
        # Check if the specified player is out of pieces and return the opponent's team if true
        if player == 'R' and count_green == 0:
            return 'G'
        elif player == 'G' and count_red == 0:
            return 'R'
        else:
            # Return False if player still has pieces
            return False

    # Function to reset colors of nodes in potential move positions and the current node
    def resetColours(grid, node):
        positions = generatePotentialMoves(node, grid)      # Generate potential move positions for the given node
        positions.append(node)                              # Include the current node in the list of positions

        # Iterate through the colored nodes in the potential move positions
        for colouredNodes in positions:
            nodeX, nodeY = colouredNodes # Extract column and row indices of the colored node
            # Set color of node based on position and checkered pattern
            grid[nodeX][nodeY].colour = BLACK if abs(nodeX - nodeY) % 2 == 0 else WHITE

    # highlights potential move positions on the game board
    def HighlightpotentialMoves(piecePosition, grid):
        # Generate potential move positions for the given piece 
        positions = generatePotentialMoves(piecePosition, grid)
        # Iterate through potential move positions and set color to blue
        for position in positions:
            Column, Row = position
            grid[Column][Row].colour = BLUE

    # get opposite team of the given team
    def opposite(team):
        return "R" if team == "G" else "G"

    # generate potential move positions for given node position on game board
    def generatePotentialMoves(nodePosition, grid):
        # Lambda checks if the resulting position is within the bounds of the game
        checker = lambda x, y: x + y >= 0 and x + y < 8
        positions = []                  # store potential move positions
        column, row = nodePosition      # Extract column and row node position

        # Check if the current node has piece
        if grid[column][row].piece:
            # Define vectors for potential moves based on the team of the piece
            vectors = [[1, -1], [1, 1]] if grid[column][row].piece.team == "R" else [[-1, -1], [-1, 1]]
            # If piece is a king, allow additional vectors for backward moves
            if grid[column][row].piece.type == 'KING':
                vectors = [[1, -1], [1, 1], [-1, -1], [-1, 1]]

            # Iterate through the defined vectors
            for vector in vectors:
                columnVector, rowVector = vector
                # Check resulting position within bounds
                if checker(columnVector, column) and checker(rowVector, row):
                    # Check if next node is empty
                    if not grid[(column + columnVector)][(row + rowVector)].piece:
                        positions.append((column + columnVector, row + rowVector))
                    # Check if next node has an opponent's piece
                    elif grid[column + columnVector][row + rowVector].piece and \
                            grid[column + columnVector][row + rowVector].piece.team == opposite(grid[column][row].piece.team):
                        # Check if the node after the opponent's piece is empty
                        if checker((2 * columnVector), column) and checker((2 * rowVector), row) \
                                and not grid[(2 * columnVector) + column][(2 * rowVector) + row].piece:
                            positions.append((2 * columnVector + column, 2 * rowVector + row))

        return positions



    """
    Error with locating possible moves row col error
    """
    # highlights a clicked node, resets old highlights, and displays potential move positions
    def highlight(ClickedNode, Grid, OldHighlight):
        Column, Row = ClickedNode
        # Highlight the clicked node in orange
        Grid[Column][Row].colour = ORANGE
        # Reset colors of old highlighted nodes
        if OldHighlight:
            resetColours(Grid, OldHighlight)
        HighlightpotentialMoves(ClickedNode, Grid)
        return (Column, Row)

    # moves piece on the game board
    def move(grid, piecePosition, newPosition):
        resetColours(grid, piecePosition)       # Reset colors nodes of piece that will move
        # Extract column and row indices of the new and old positions
        newColumn, newRow = newPosition
        oldColumn, oldRow = piecePosition

        # Move the piece to the new position
        piece = grid[oldColumn][oldRow].piece
        grid[newColumn][newRow].piece = piece
        grid[oldColumn][oldRow].piece = None

        # Check for promotion to king and update piece type and image accordingly
        if newColumn == 7 and grid[newColumn][newRow].piece.team == 'R':
            grid[newColumn][newRow].piece.type = 'KING'
            grid[newColumn][newRow].piece.image = REDKING
        if newColumn == 0 and grid[newColumn][newRow].piece.team == 'G':
            grid[newColumn][newRow].piece.type = 'KING'
            grid[newColumn][newRow].piece.image = GREENKING

        # Check for capturing an opponent's piece during a move
        if abs(newColumn - oldColumn) == 2 or abs(newRow - oldRow) == 2:
            grid[int((newColumn + oldColumn) / 2)][int((newRow + oldRow) / 2)].piece = None
            return grid[newColumn][newRow].piece.team

        # If no capturing occurred, return the opposite team's color
        return opposite(grid[newColumn][newRow].piece.team)

    # Function to reset the game state to the initial state
    def reset_game():
        global grid, highlightedPiece, currMove
        grid = make_grid(ROWS, WIDTH)
        highlightedPiece = None
        currMove = 'G'

    # Function to reset the game state to a custom initial state
    def reset_game_1():
        global grid, highlightedPiece, currMove
        grid = make_grid_1(ROWS, WIDTH)
        highlightedPiece = None
        currMove = 'G'

    # Main function for initializing game state variables
    def main(WIDTH, ROWS):
        #initialize variables
        global grid, highlightedPiece, currMove, help_menu_displayed, double_jump
        grid = make_grid(ROWS, WIDTH)
        highlightedPiece = None
        currMove = 'G'
        help_menu_displayed = False
        double_jump = False

        while True:
            # Check if the current player has won
            if is_player_out(grid, currMove):      
                print(f"Player {currMove} has won! Game over.")
                reset_game()
            # click on the quit button to exit fully
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    print('EXIT SUCCESSFUL')
                    pygame.quit()
                    sys.exit()
                # press escape to return to main menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu()
                        sys.exit()
                # press r to reset game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()

                # press 1 to set the gamestate to game state 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        reset_game_1()        

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickedNode = getNode(grid, ROWS, WIDTH)
                    ClickedPositionColumn, ClickedPositionRow = clickedNode
                    
                     # Move the highlighted piece to the clicked position if valid
                    if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE:
                        if highlightedPiece:
                            pieceColumn, pieceRow = highlightedPiece
                        if currMove == grid[pieceColumn][pieceRow].piece.team:
                            resetColours(grid, highlightedPiece)
                            double_jump = move(grid, highlightedPiece, clickedNode)
                            currMove = double_jump
                            # currMove = move(grid, highlightedPiece, clickedNode)
                    elif highlightedPiece == clickedNode:   # Unhighlight the piece if it's clicked again
                       pass                
                    else:
                         # Highlight the clicked piece for potential moves
                        if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                            if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                                highlightedPiece = highlight(clickedNode, grid, highlightedPiece)                     
            
            # Update and display the game window
            update_display(WIN, grid,ROWS,WIDTH)
    main(WIDTH, ROWS)

while True:
    main_menu()