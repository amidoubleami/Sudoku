from sudoku_alg import valid, solve, find_empty
from copy import deepcopy
from Button import Button
import numpy as np
from dokusan import generators
import pygame
import time
import random
import os
from enum import Enum
pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")
def generate(level):
    '''Randomly generates a Sudoku grid/board'''
    while True:  #return will interrupt the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        # puts one random number, then solves the board to generate a board
            rank = 0
            if level == Level.EASY:
                rank = 150
            if level == Level.MEDIUM:
                rank = 300
            if level == Level.HARD:
                rank = 450
                
            print(rank)
            arr = np.array (list(str(generators.random_sudoku(avg_rank=rank))))
            board  = arr.reshape((9, 9))
            board = board.astype(int).tolist()
        partialBoard = deepcopy(board) #copies board without being modified after solve is called
        if solve(board):
            return partialBoard
class Board:
    '''A sudoku board made out of Tiles'''
    def __init__(self, window, level):
        self.board = generate(level)
        self.solvedBoard = deepcopy(self.board)
        solve(self.solvedBoard)
        self.tiles = [[Tile(self.board[i][j], window, i*60, j*60) for j in range(9)] for i in range(9)]
        self.window = window
        self.level = level

    def draw_board(self):
        '''Fills the board with Tiles and renders their values'''
        for i in range(9):
            for j in range(9):
                if j%3 == 0 and j != 0: #vertical lines
                    pygame.draw.line(self.window, (0, 0, 0), ((j//3)*180, 0), ((j//3)*180, 540), 4)

                if i%3 == 0 and i != 0: #horizontal lines
                    pygame.draw.line(self.window, (0, 0, 0), (0, (i//3)*180), (540, (i//3)*180), 4)

                self.tiles[i][j].draw((0,0,0), 1)

                if self.tiles[i][j].value != 0: #don't draw 0s on the grid
                    self.tiles[i][j].display(self.tiles[i][j].value, (20+(j*60), (5+(i*60))), (0, 0, 0))  #20,5 are the coordinates of the first tile
        #bottom-most line
        pygame.draw.line(self.window, (0, 0, 0), (0, ((i+1) // 3) * 180), (540, ((i+1) // 3) * 180), 4)

    def deselect(self, tile):
        '''Deselects every tile except the one currently clicked'''
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j] != tile:
                    self.tiles[i][j].selected = False

    def redraw(self, keys, wrong, time,ltime):
        '''Redraws board with highlighted tiles'''
        self.window.fill((255,255,255))
        self.draw_board()
        for i in range(9):
            for j in range(9):
                if self.tiles[j][i].selected:  #draws the border on selected tiles
                    self.tiles[j][i].draw((50, 205, 50), 4)

                elif self.tiles[i][j].correct:
                    self.tiles[j][i].draw((34, 139, 34), 4)

                elif self.tiles[i][j].incorrect:
                    self.tiles[j][i].draw((255, 0, 0), 4)

        if len(keys) != 0: #draws inputs that the user places on board but not their final value on that tile
            for value in keys:
                self.tiles[value[0]][value[1]].display(keys[value], (20+(value[0]*60), (5+(value[1]*60))), (128, 128, 128))

        if wrong > 0:
            font = pygame.font.SysFont('Bauhaus 93', 30) #Red X
            text = font.render('X', True, (255, 0, 0))
            self.window.blit(text, (10, 554))

            font = pygame.font.SysFont('Bahnschrift', 40) #Number of Incorrect Inputs
            text = font.render(str(wrong), True, (0, 0, 0))
            self.window.blit(text, (32, 542))

        font = pygame.font.SysFont('Bahnschrift', 30) #Time Display
        text = font.render(str(time), True, (0, 0, 0))
        self.window.blit(text, (388, 542))

        font = pygame.font.SysFont('Bahnschrift', 30)
        text = font.render("Least Time Taken: {}".format(ltime), True, (0, 0, 0))
        self.window.blit(text, (20, 542))
        pygame.display.flip()

    def visualSolve(self, wrong, time):
        '''Showcases how the board is solved via backtracking'''
        for event in pygame.event.get(): #so that touching anything doesn't freeze the screen
            if event.type == pygame.QUIT:
                exit()

        empty = find_empty(self.board)
        if not empty:
            return True

        for nums in range(9):
            if valid(self.board, (empty[0],empty[1]), nums+1):
                self.board[empty[0]][empty[1]] = nums+1
                self.tiles[empty[0]][empty[1]].value = nums+1
                self.tiles[empty[0]][empty[1]].correct = True
                pygame.time.delay(63) #show tiles at a slower rate
                self.redraw({}, wrong, time)
                if self.visualSolve(wrong, time):
                    return True

                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(63)
                self.redraw({}, wrong, time)

    def hint(self, keys):
        '''Shows a random empty tile's solved value as a hint'''
        while True: #keeps generating i,j coords until it finds a valid random spot
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if self.board[i][j] == 0: #hint spot has to be empty
                if (j,i) in keys:
                    del keys[(j,i)]
                self.board[i][j] = self.solvedBoard[i][j]
                self.tiles[i][j].value = self.solvedBoard[i][j]
                return True

            elif self.board == self.solvedBoard:
                return False
class Tile:
    '''Represents each white tile/box on the grid'''
    def __init__(self, value, window, x1, y1):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60) #dimensions for the rectangle
        self.selected = False
        self.correct = False
        self.incorrect = False

    def draw(self, color, thickness):
        '''Draws a tile on the board'''
        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display(self, value, position, color):
        '''Displays a number on that tile'''
        font = pygame.font.SysFont('lato', 40)
        text = font.render(str(value), True, color)
        self.window.blit(text, position)

    def clicked(self, mousePos):
        '''Checks if a tile has been clicked'''
        if self.rect.collidepoint(mousePos): #checks if a point is inside a rect
            self.selected = True
        return self.selected

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play(level):
    screen = pygame.display.set_mode((1020, 590))
    screen.fill((255, 255, 255))  #color
    #loading screen when generating grid
    font = pygame.font.SysFont('Bahnschrift', 40)
    text = font.render("Generating", True, (0, 0, 0))
    screen.blit(text, (175, 245))

    font = pygame.font.SysFont('Bahnschrift', 40)
    text = font.render("Grid", True, (0, 0, 0))
    screen.blit(text, (230, 290))
    pygame.display.flip()

    #initiliaze values and variables
    wrong = 0
    board = Board(screen, level)
    selected = -1,-1 #NoneType error when selected = None, easier to just format as a tuple whose value will never be used
    keyDict = {}
    running = True
    startTime = time.time()
    least_time = 0
    if os.path.exists('least_time.txt'):
        with open('least_time', 'r') as file:
            least_time = int(file.read())
    else:
        least_time = 0
    while running:
        elapsed = time.time() - startTime
        passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))
        if board.board == board.solvedBoard: #user has solved the board
            if passedTime < least_time:
                least_time = passedTime
                with open('least_time.txt', 'w') as file:
                    file.write(str(least_time))
            pygame.display.flip()
            for i in range(9):
                for j in range(9):
                    board.tiles[i][j].selected = False
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit() #so that it doesnt go to the outer run loop

            elif event.type == pygame.MOUSEBUTTONUP: #allow clicks only while the board hasn't been solved
                mousePos = pygame.mouse.get_pos()
                for i in range(9):
                    for j in range (9):
                        if board.tiles[i][j].clicked(mousePos):
                            selected = i,j
                            board.deselect(board.tiles[i][j]) #deselects every tile except the one currently clicked

            elif event.type == pygame.KEYDOWN:
                if board.board[selected[1]][selected[0]] == 0 and selected != (-1,-1):
                    if event.key == pygame.K_1:
                        keyDict[selected] = 1

                    if event.key == pygame.K_2:
                        keyDict[selected] = 2

                    if event.key == pygame.K_3:
                        keyDict[selected] = 3

                    if event.key == pygame.K_4:
                        keyDict[selected] = 4

                    if event.key == pygame.K_5:
                        keyDict[selected] = 5

                    if event.key == pygame.K_6:
                        keyDict[selected] = 6

                    if event.key == pygame.K_7:
                        keyDict[selected] = 7

                    if event.key == pygame.K_8:
                        keyDict[selected] = 8

                    if event.key == pygame.K_9:
                        keyDict[selected] = 9

                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:  # clears tile out
                        if selected in keyDict:
                            board.tiles[selected[1]][selected[0]].value = 0
                            del keyDict[selected]

                    elif event.key == pygame.K_RETURN:
                        if selected in keyDict:
                            if keyDict[selected] != board.solvedBoard[selected[1]][selected[0]]: #clear tile when incorrect value is inputted
                                wrong += 1
                                board.tiles[selected[1]][selected[0]].value = 0
                                del keyDict[selected]
                                break
                            #valid and correct entry into cell
                            board.tiles[selected[1]][selected[0]].value = keyDict[selected] #assigns current grid value
                            board.board[selected[1]][selected[0]] = keyDict[selected] #assigns to actual board so that the correct value can't be modified
                            del keyDict[selected]

                if event.key == pygame.K_h:
                    board.hint(keyDict)

                if event.key == pygame.K_SPACE:
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].selected = False
                    keyDict = {}  #clear keyDict out
                    board.visualSolve(wrong, passedTime)
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].correct = False
                            board.tiles[i][j].incorrect = False #reset tiles
                    running = False
        board.redraw(keyDict, wrong, passedTime,least_time)
    while True: #another running loop so that the program ONLY closes when user closes program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "white")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        EASY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="EASY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MEDIUM_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="MEDIUM", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HARD_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="HARD", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(Level.EASY)
                if MEDIUM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(Level.MEDIUM)
                if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(Level.HARD)

        pygame.display.update()

class Level(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

main_menu()
pygame.quit()