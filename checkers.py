########################################################
# CMPS 3500 - Class Project
# Checkers game simulator
# This is a program that will simulate a checkers board
# and provide basic game functionalities.
# This program does not abide all rules of checkers
########################################################

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

WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (235, 168, 52)
BLUE = (76, 252, 241)


pygame.init()
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Checkers')

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
            if (i==3) and (j==3):
                node.piece = Piece('R')
            elif(i==4) and (j==4):
                node.piece=Piece('G')
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
    global grid, highlightedPiece, currMove
    grid = make_grid(ROWS, WIDTH)
    highlightedPiece = None
    currMove = 'G'

    while True:
        if is_player_out(grid, currMove):
            print(f"Player {currMove} has won! Game over.")
            reset_game()

        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

            #press 1 to set the gamestate to game state 1
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
                        result = move(grid, highlightedPiece, clickedNode)
                        #fixes extra turn after capture
                        currMove = opposite(currMove)
                        
                elif highlightedPiece == clickedNode:
                    #deselect piece
                    resetColours(grid, highlightedPiece)
                    highlightedPiece = None
                    
                else:
                    if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                        if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                            highlightedPiece = highlight(clickedNode, grid, highlightedPiece)


        update_display(WIN, grid,ROWS,WIDTH)


main(WIDTH, ROWS)
