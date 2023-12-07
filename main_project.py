# two player chess in python with Pygame!
# pawn double space checking
# castling
# en passant
# pawn promotion

import pygame
import pygame
import random
import sys
from itertools import combinations
import os

# current directory
dirname = os.path.dirname(__file__)

WIDTH = 1000
ROWS = 8

RED= pygame.image.load(os.path.join(dirname, 'images/red.png'))
GREEN= pygame.image.load(os.path.join(dirname, 'images/green.png'))

REDKING = pygame.image.load(os.path.join(dirname, 'images/redking.png'))
GREENKING = pygame.image.load(os.path.join(dirname, 'images/greenking.png'))

# images for the play button and checkers button
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
WIN = pygame.display.set_mode((WIDTH,WIDTH),pygame.FULLSCREEN)
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

def main_menu():
    while True:
        title_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()

                # Check if the play button is clicked
                if WIDTH // 4 < mouseX < WIDTH // 4 + CHECKERS_BUTTON.get_width() and \
                        200 < mouseY < 200 + CHECKERS_BUTTON.get_height():
                    checkers_game()
                
                if WIDTH // 4 < mouseX < WIDTH // 4 + CHESS_BUTTON.get_width() and \
                        400 < mouseY < 400 + CHESS_BUTTON.get_height():
                    chess_game()

                # Check if the quit button is clicked
                elif WIDTH // 4 < mouseX < WIDTH // 4 + QUIT_BUTTON.get_width() and \
                        500 < mouseY < 500 + QUIT_BUTTON.get_height():
                    pygame.quit()
                    sys.exit()

        pygame.display.update()    

def chess_game():
    pygame.init()
    global help_menu_displayed
    WIDTH = 1000
    HEIGHT = 900
    screen = pygame.display.set_mode([WIDTH, HEIGHT],pygame.FULLSCREEN)
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
            column = i % 4
            row = i // 4
            if row % 2 == 0:
                pygame.draw.rect(screen, 'light gray', [500 - (column * 200), row * 100, 100, 100])
            else:
                pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
            pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
            pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
            pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
            status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                        'Black: Select a Piece to Move!', 'Black: Select a Destination!']
            screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
            for i in range(9):
                pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
                pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
            screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))
            if white_promote or black_promote:
                pygame.draw.rect(screen, 'gray', [0, 800, WIDTH - 200, 100])
                pygame.draw.rect(screen, 'gold', [0, 800, WIDTH - 200, 100], 5)
                screen.blit(big_font.render('Select Piece to Promote Pawn', True, 'black'), (20, 820))


    # draw pieces onto board
    def draw_pieces():
        for i in range(len(white_pieces)):
            index = piece_list.index(white_pieces[i])
            if white_pieces[i] == 'pawn':
                screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
            else:
                screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
            if turn_step < 2:
                if selection == i:
                    pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                    100, 100], 2)

        for i in range(len(black_pieces)):
            index = piece_list.index(black_pieces[i])
            if black_pieces[i] == 'pawn':
                screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
            else:
                screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
            if turn_step >= 2:
                if selection == i:
                    pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                                                    100, 100], 2)


    # function to check all pieces valid options on board
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


    # draw valid moves on screen
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
            captured_piece = captured_pieces_white[i]
            index = piece_list.index(captured_piece)
            screen.blit(small_black_images[index], (825, 5 + 50 * i))
        for i in range(len(captured_pieces_black)):
            captured_piece = captured_pieces_black[i]
            index = piece_list.index(captured_piece)
            screen.blit(small_white_images[index], (925, 5 + 50 * i))


    # draw a flashing square around king if in check
    def draw_check():
        global check
        check = False
        if turn_step < 2:
            if 'king' in white_pieces:
                king_index = white_pieces.index('king')
                king_location = white_locations[king_index]
                for i in range(len(black_options)):
                    if king_location in black_options[i]:
                        check = True
                        if counter < 15:
                            pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                                white_locations[king_index][1] * 100 + 1, 100, 100], 5)
        else:
            if 'king' in black_pieces:
                king_index = black_pieces.index('king')
                king_location = black_locations[king_index]
                for i in range(len(white_options)):
                    if king_location in white_options[i]:
                        check = True
                        if counter < 15:
                            pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                                black_locations[king_index][1] * 100 + 1, 100, 100], 5)


    def draw_game_over():
        pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
        screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
        screen.blit(font.render(f'Press R to Restart!', True, 'white'), (210, 240))


    # check en passant because people on the internet won't stop bugging me for it
    def check_ep(old_coords, new_coords):
        if turn_step <= 1:
            index = white_locations.index(old_coords)
            ep_coords = (new_coords[0], new_coords[1] - 1)
            piece = white_pieces[index]
        else:
            index = black_locations.index(old_coords)
            ep_coords = (new_coords[0], new_coords[1] + 1)
            piece = black_pieces[index]
        if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
            # if piece was pawn and moved two spaces, return EP coords as defined above
            pass
        else:
            ep_coords = (100, 100)
        return ep_coords


    # add castling
    def check_castling():
        # king must not currently be in check, neither the rook nor king has moved previously, nothing between
        # and the king does not pass through or finish on an attacked piece
        castle_moves = []  # store each valid castle move as [((king_coords), (castle_coords))]
        rook_indexes = []
        rook_locations = []
        king_index = 0
        king_pos = (0, 0)
        if turn_step > 1:
            for i in range(len(white_pieces)):
                if white_pieces[i] == 'rook':
                    rook_indexes.append(white_moved[i])
                    rook_locations.append(white_locations[i])
                if white_pieces[i] == 'king':
                    king_index = i
                    king_pos = white_locations[i]
            if not white_moved[king_index] and False in rook_indexes and not check:
                for i in range(len(rook_indexes)):
                    castle = True
                    if rook_locations[i][0] > king_pos[0]:
                        empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                        (king_pos[0] + 3, king_pos[1])]
                    else:
                        empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                    for j in range(len(empty_squares)):
                        if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                                empty_squares[j] in black_options or rook_indexes[i]:
                            castle = False
                    if castle:
                        castle_moves.append((empty_squares[1], empty_squares[0]))
        else:
            for i in range(len(black_pieces)):
                if black_pieces[i] == 'rook':
                    rook_indexes.append(black_moved[i])
                    rook_locations.append(black_locations[i])
                if black_pieces[i] == 'king':
                    king_index = i
                    king_pos = black_locations[i]
            if not black_moved[king_index] and False in rook_indexes and not check:
                for i in range(len(rook_indexes)):
                    castle = True
                    if rook_locations[i][0] > king_pos[0]:
                        empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                        (king_pos[0] + 3, king_pos[1])]
                    else:
                        empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                    for j in range(len(empty_squares)):
                        if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                                empty_squares[j] in white_options or rook_indexes[i]:
                            castle = False
                    if castle:
                        castle_moves.append((empty_squares[1], empty_squares[0]))
        return castle_moves


    def draw_castling(moves):
        if turn_step < 2:
            color = 'red'
        else:
            color = 'blue'
        for i in range(len(moves)):
            pygame.draw.circle(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70), 8)
            screen.blit(font.render('king', True, 'black'), (moves[i][0][0] * 100 + 30, moves[i][0][1] * 100 + 70))
            pygame.draw.circle(screen, color, (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 8)
            screen.blit(font.render('rook', True, 'black'),
                        (moves[i][1][0] * 100 + 30, moves[i][1][1] * 100 + 70))
            pygame.draw.line(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70),
                            (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 2)


    # add pawn promotion
    def check_promotion():
        pawn_indexes = []
        white_promotion = False
        black_promotion = False
        promote_index = 100
        for i in range(len(white_pieces)):
            if white_pieces[i] == 'pawn':
                pawn_indexes.append(i)
        for i in range(len(pawn_indexes)):
            if white_locations[pawn_indexes[i]][1] == 7:
                white_promotion = True
                promote_index = pawn_indexes[i]
        pawn_indexes = []
        for i in range(len(black_pieces)):
            if black_pieces[i] == 'pawn':
                pawn_indexes.append(i)
        for i in range(len(pawn_indexes)):
            if black_locations[pawn_indexes[i]][1] == 0:
                black_promotion = True
                promote_index = pawn_indexes[i]
        return white_promotion, black_promotion, promote_index


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
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        x_pos = mouse_pos[0] // 100
        y_pos = mouse_pos[1] // 100
        if white_promote and left_click and x_pos > 7 and y_pos < 4:
            white_pieces[promo_index] = white_promotions[y_pos]
        elif black_promote and left_click and x_pos > 7 and y_pos < 4:
            black_pieces[promo_index] = black_promotions[y_pos]


    # main game loop
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
        draw_board()
        draw_pieces()
        draw_captured()
        draw_check()
        if not game_over:
            white_promote, black_promote, promo_index = check_promotion()
            if white_promote or black_promote:
                draw_promotion()
                check_promo_select()
        if selection != 100:
            valid_moves = check_valid_moves()
            draw_valid(valid_moves)
            if selected_piece == 'king':
                draw_castling(castling_moves)
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                x_coord = event.pos[0] // 100
                y_coord = event.pos[1] // 100
                click_coords = (x_coord, y_coord)
                if turn_step <= 1:
                    if click_coords == (8, 8) or click_coords == (9, 8):
                        winner = 'black'
                    if click_coords in white_locations:
                        selection = white_locations.index(click_coords)
                        # check what piece is selected, so you can only draw castling moves if king is selected
                        selected_piece = white_pieces[selection]
                        if turn_step == 0:
                            turn_step = 1
                    if click_coords in valid_moves and selection != 100:
                        white_ep = check_ep(white_locations[selection], click_coords)
                        white_locations[selection] = click_coords
                        white_moved[selection] = True
                        if click_coords in black_locations:
                            black_piece = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces[black_piece])
                            if black_pieces[black_piece] == 'king':
                                winner = 'white'
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                            black_moved.pop(black_piece)
                        # adding check if en passant pawn was captured
                        if click_coords == black_ep:
                            black_piece = black_locations.index((black_ep[0], black_ep[1] - 1))
                            captured_pieces_white.append(black_pieces[black_piece])
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                            black_moved.pop(black_piece)
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 2
                        selection = 100
                        valid_moves = []
                    # add option to castle
                    elif selection != 100 and selected_piece == 'king':
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
                                white_locations[selection] = click_coords
                                white_moved[selection] = True
                                if click_coords == (1, 0):
                                    rook_coords = (0, 0)
                                else:
                                    rook_coords = (7, 0)
                                rook_index = white_locations.index(rook_coords)
                                white_locations[rook_index] = castling_moves[q][1]
                                black_options = check_options(black_pieces, black_locations, 'black')
                                white_options = check_options(white_pieces, white_locations, 'white')
                                turn_step = 2
                                selection = 100
                                valid_moves = []
                if turn_step > 1:
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
                    # add option to castle
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



# Start of checkers game
def checkers_game():
    priorMoves=[]
    class Node:
        def __init__(self, row, col, width):
            self.row = row
            self.col = col
            self.x = int(row * width)
            self.y = int(col * width)
            self.colour = WHITE
            self.piece = None

        def draw(self, WIN):
            pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / ROWS, WIDTH / ROWS))
            if self.piece:
                WIN.blit(self.piece.image, (self.x, self.y))


    def update_display(win, grid, rows, width):
        for row in grid:
            for spot in row:
                spot.draw(win)
        draw_grid(win, rows, width)
        pygame.display.update()


    def make_grid(rows, width):
        grid = []
        gap = width// rows
        count = 0
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                node = Node(j,i, gap)
                if abs(i-j) % 2 == 0:
                    node.colour=BLACK
                if (abs(i+j)%2==0) and (i<3):
                    node.piece = Piece('R')
                elif(abs(i+j)%2==0) and i>4:
                    node.piece=Piece('G')
                count+=1
                grid[i].append(node)
        return grid

    # defines the grid stat when restarting the game to a desired state
    def make_grid_1(rows, width):
        grid = []
        gap = width// rows
        count = 0
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                node = Node(j,i, gap)
                if abs(i-j) % 2 == 0:
                    node.colour=BLACK
                if  i==0:
                    if j == 0 or j == 4:
                        node.piece = Piece('R')
                if  i==1:
                    if j == 3 or j == 5 or j == 7:
                        node.piece = Piece('R')
                if  i==2:
                    if j == 0 or j == 6:
                        node.piece = Piece('R')
                if  i==3:
                    if j == 1:
                        node.piece = Piece('R')   
                if  i==7:
                    if j == 3:
                        node.piece = Piece('R')
                        node.piece.type = 'KING'
                        node.piece.image=REDKING

     
                if  i==3:
                    if j == 3:
                        node.piece = Piece('G')  
                if  i==5:
                    if j == 1 or j == 3 or j == 7:
                        node.piece = Piece('G')  
                if  i==6:
                    if j == 0 or j == 2 or j == 6:
                        node.piece = Piece('G')


                count+=1
                grid[i].append(node)
        return grid


    def draw_grid(win, rows, width):
        gap = width // ROWS
        for i in range(rows):
            pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


    class Piece:
        def __init__(self, team):
            self.team=team
            self.image= RED if self.team=='R' else GREEN
            self.type=None

        def draw(self, x, y):
            WIN.blit(self.image, (x,y))


    def getNode(grid, rows, width):
        gap = width//rows
        RowX,RowY = pygame.mouse.get_pos()
        Row = RowX//gap
        Col = RowY//gap
        return (Col,Row)

    def count_pieces(grid):
        count_red = 0
        count_green = 0
        for row in grid:
            for spot in row:
                if spot.piece:
                    if spot.piece.team == 'R':
                        count_red += 1
                    elif spot.piece.team == 'G':
                        count_green += 1
        return count_red, count_green

    def is_player_out(grid, player):
        count_red, count_green = count_pieces(grid)
        if player == 'R' and count_green == 0:
            return 'G'
        elif player == 'G' and count_red == 0:
            return 'R'
        else:
            return False


    def resetColours(grid, node):
        positions = generatePotentialMoves(node, grid)
        positions.append(node)

        for colouredNodes in positions:
            nodeX, nodeY = colouredNodes
            grid[nodeX][nodeY].colour = BLACK if abs(nodeX - nodeY) % 2 == 0 else WHITE

    def HighlightpotentialMoves(piecePosition, grid):
        positions = generatePotentialMoves(piecePosition, grid)
        for position in positions:
            Column,Row = position
            grid[Column][Row].colour=BLUE

    def opposite(team):
        return "R" if team=="G" else "G"

    def generatePotentialMoves(nodePosition, grid):
        checker = lambda x,y: x+y>=0 and x+y<8
        positions= []
        column, row = nodePosition
        if grid[column][row].piece:
            vectors = [[1, -1], [1, 1]] if grid[column][row].piece.team == "R" else [[-1, -1], [-1, 1]]
            if grid[column][row].piece.type=='KING':
                vectors = [[1, -1], [1, 1],[-1, -1], [-1, 1]]
            for vector in vectors:
                columnVector, rowVector = vector
                if checker(columnVector,column) and checker(rowVector,row):
                    #grid[(column+columnVector)][(row+rowVector)].colour=ORANGE
                    if not grid[(column+columnVector)][(row+rowVector)].piece:
                        positions.append((column + columnVector, row + rowVector))
                    elif grid[column+columnVector][row+rowVector].piece and\
                            grid[column+columnVector][row+rowVector].piece.team==opposite(grid[column][row].piece.team):

                        if checker((2* columnVector), column) and checker((2* rowVector), row) \
                                and not grid[(2* columnVector)+ column][(2* rowVector) + row].piece:
                            positions.append((2* columnVector+ column,2* rowVector+ row ))

        return positions


    """
    Error with locating possible moves row col error
    """
    def highlight(ClickedNode, Grid, OldHighlight):
        Column,Row = ClickedNode
        Grid[Column][Row].colour=ORANGE
        if OldHighlight:
            resetColours(Grid, OldHighlight)
        HighlightpotentialMoves(ClickedNode, Grid)
        return (Column,Row)

    def move(grid, piecePosition, newPosition):
        resetColours(grid, piecePosition)
        newColumn, newRow = newPosition
        oldColumn, oldRow = piecePosition

        piece = grid[oldColumn][oldRow].piece
        grid[newColumn][newRow].piece=piece
        grid[oldColumn][oldRow].piece = None

        if newColumn==7 and grid[newColumn][newRow].piece.team=='R':
            grid[newColumn][newRow].piece.type='KING'
            grid[newColumn][newRow].piece.image=REDKING
        if newColumn==0 and grid[newColumn][newRow].piece.team=='G':
            grid[newColumn][newRow].piece.type='KING'
            grid[newColumn][newRow].piece.image=GREENKING
        if abs(newColumn-oldColumn)==2 or abs(newRow-oldRow)==2:
            grid[int((newColumn+oldColumn)/2)][int((newRow+oldRow)/2)].piece = None
            return grid[newColumn][newRow].piece.team
        return opposite(grid[newColumn][newRow].piece.team)

    # function to reset the game
    def reset_game():
        global grid, highlightedPiece, currMove
        grid = make_grid(ROWS, WIDTH)
        highlightedPiece = None
        currMove = 'G'

    # defines reseting the game to a desired state
    def reset_game_1():
        global grid, highlightedPiece, currMove
        grid = make_grid_1(ROWS, WIDTH)
        highlightedPiece = None
        currMove = 'G'

    def main(WIDTH, ROWS):
        global grid, highlightedPiece, currMove, help_menu_displayed, double_jump
        grid = make_grid(ROWS, WIDTH)
        highlightedPiece = None
        currMove = 'G'
        help_menu_displayed = False
        double_jump = False

        while True:
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
                    
                    if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE:
                        if highlightedPiece:
                            pieceColumn, pieceRow = highlightedPiece
                        if currMove == grid[pieceColumn][pieceRow].piece.team:
                            resetColours(grid, highlightedPiece)
                            double_jump = move(grid, highlightedPiece, clickedNode)
                            currMove = double_jump
                            # currMove = move(grid, highlightedPiece, clickedNode)
                    elif highlightedPiece == clickedNode:
                       pass                
                    else:
                        if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                            if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                                highlightedPiece = highlight(clickedNode, grid, highlightedPiece)                     
            
            
            update_display(WIN, grid,ROWS,WIDTH)
    main(WIDTH, ROWS)

while True:
    main_menu()