#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Goban made with Python, pygame and go.py.

This is a front-end for my go library 'go.py', handling drawing and
pygame-related activities. Together they form a fully working goban.

"""

import numpy as np
import pygame
import copy
from sys import exit
import time
from time import sleep
"""import everything made"""
import michi
import go
import arm_control
import img_process
"""========global var============="""
board_size = 7
show_board = ['.'] * board_size * board_size
np_board = np.zeros((board_size, board_size), dtype='u1')
BOARD_SIZE = (500, 450)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
Green4 = (0, 139, 0)
BLUE = (0, 0, 255)
black_num, white_num = 0, 0
wempty_num, bempty_num = 0, 0
remove_list = []
"""==============================="""


def text_objects(text, font, color):
    textsurface = font.render(text, True, color)
    return textsurface, textsurface.get_rect()


class Stone(go.Stone):
    def __init__(self, board, point, color):
        """Create, initialize and draw a stone."""
        if color == "B":
            color = BLACK
        else:
            color = WHITE
        super(Stone, self).__init__(board, point, color)
        self.coords = point[0], point[1]
        self.coord = (30 + self.point[0] * 40, 20 + ((board_size + 1 - self.point[1]) * 40))
        self.draw()

    def draw(self):
        smalltext = pygame.font.Font("./images/FiraCode-Bold.ttf", 15)
        """Draw the stone as a circle."""
        # pygame.draw.circle(screen, self.color, self.coord, 20, 0)
        x, y = self.coord
        x = x - 20
        y = y - 20
        stone_color = black_stone if self.color == BLACK else white_stone
        screen.blit(stone_color, (x, y))
        pygame.display.update()
        """"""
        """Draw the stone."""
        if self.coords == 'pass':
            return self.coords
        print(self.color, " played: ", chr(self.coords[0]+64), chr(self.coords[1]+48))
        x_pos, y_pos = self.coords
        if self.color == BLACK:
            show_board[(x_pos-1)+(board_size-int(y_pos))*board_size] = "X"
            np_board[board_size-int(y_pos)][x_pos-1] = "1"
        elif self.color == WHITE:
            show_board[(x_pos-1)+(board_size-int(y_pos))*board_size] = "O"
            np_board[board_size-int(y_pos)][x_pos-1] = "2"

    def remove(self):
        """Remove the stone from board."""
        global remove_list
        remove_list.append(self.coords)
        blit_coords = (self.coord[0] - 20, self.coord[1] - 20)
        area_rect = pygame.Rect(blit_coords, (40, 40))
        screen.blit(background, blit_coords, area_rect)
        pygame.display.update()
        x_pos, y_pos = self.coords
        show_board[x_pos-1+(board_size-int(y_pos))*board_size] = "."
        np_board[board_size-int(y_pos)][x_pos-1] = "0"
        super(Stone, self).remove()


class Board(go.Board):
    def __init__(self):
        """Create, initialize and draw an empty board."""
        super(Board, self).__init__()
        self.outline = pygame.Rect(70, 60, 240, 240)
        self.draw()
        global show_board, np_board
        show_board = ['.'] * board_size * board_size
        np_board = np.zeros((board_size, board_size), dtype = 'u1')

    def draw(self):
        """Draw the board to the background and blit it to the screen.

        The board is drawn by first drawing the outline, then the 19x19
        grid and finally by adding hoshi to the board. All these
        operations are done with pygame's draw functions.

        This method should only be called once, when initializing the
        board.

        """
        smalltext = pygame.font.Font("./images/FiraCode-Bold.ttf", 15)
        """draw button"""
        background.blit(black_button, (330, 33))
        textsurf, textrect = text_objects("BLACK", smalltext, WHITE)
        textrect.center = (365, 50)
        background.blit(textsurf, textrect)
        """"""
        background.blit(white_button, (410, 32))
        textsurf, textrect = text_objects("WHITE", smalltext, BLACK)
        textrect.center = (445, 50)
        background.blit(textsurf, textrect)
        """"""
        background.blit(white_bar, (345, 93))
        textsurf, textrect = text_objects("OK", smalltext, BLACK)
        textrect.center = (407, 115)
        background.blit(textsurf, textrect)
        """"""
        background.blit(white_bar, (345, 153))
        textsurf, textrect = text_objects("HINT!", smalltext, BLUE)
        textrect.center = (407, 175)
        background.blit(textsurf, textrect)
        """"""
        background.blit(white_bar, (345, 213))
        textsurf, textrect = text_objects("PASS", smalltext, Green4)
        textrect.center = (407, 235)
        background.blit(textsurf, textrect)
        """"""
        background.blit(white_bar, (345, 273))
        textsurf, textrect = text_objects("RESIGN", smalltext, RED)
        textrect.center = (407, 295)
        background.blit(textsurf, textrect)
        """Draw board"""
        pygame.draw.rect(background, BLACK, self.outline, 3)
        # Outline is inflated here for future use as a collidebox for the mouse
        self.outline.inflate_ip(20, 20)
        for i in range(board_size - 1):
            for j in range(board_size - 1):
                rect = pygame.Rect(70 + (40 * i), 60 + (40 * j), 40, 40)
                pygame.draw.rect(background, BLACK, rect, 1)
        for i in range(1):
            for j in range(1):
                coords = (190 + (120 * i), 180 + (120 * j))
                pygame.draw.circle(background, BLACK, coords, 5, 0)
        for i in range(board_size):
            textsurf, textrect = text_objects(str(board_size - i), smalltext, BLACK)
            textrect.center = (40, 60+ (40 * i))
            background.blit(textsurf, textrect)
            textsurf, textrect = text_objects(chr(i + ord('A')), smalltext, BLACK)
            textrect.center = (70 + (40 * i), 330)
            background.blit(textsurf, textrect)
        """"""
        screen.blit(background, (0, 0))
        """draw count"""
        global black_num, white_num, wempty_num, bempty_num
        black_num, white_num =0, 0
        wempty_num, bempty_num =0, 0
        screen.blit(text_bar, (70, 5))
        textsurf, textrect = text_objects("Black: " + str(black_num), smalltext, BLACK)
        textrect.center = (150, 19)
        screen.blit(textsurf, textrect)
        textsurf, textrect = text_objects("White: " + str(white_num), smalltext, BLACK)
        textrect.center = (245, 19)
        screen.blit(textsurf, textrect)
        """draw time"""
        screen.blit(white_bar, (345, 333))
        textsurf, textrect = text_objects("Time: ", smalltext, RED)
        textrect.center = (407, 355)
        screen.blit(textsurf, textrect)
        """draw your time"""
        screen.blit(white_bar, (345, 393))
        textsurf, textrect = text_objects("YourTime: 0" , smalltext, RED)
        textrect.center = (407, 415)
        screen.blit(textsurf, textrect)
        """draw text bar"""
        screen.blit(text_bar, (70, 350))
        textsurf, textrect = text_objects('Which side you wanna', smalltext, BLUE)
        textrect.center = (190, 362)
        screen.blit(textsurf, textrect)
        screen.blit(text_bar, (70, 380))
        textsurf, textrect = text_objects('take (BLACK/WHITE) : ', smalltext, BLUE)
        textrect.center = (195, 392)
        screen.blit(textsurf, textrect)
        pygame.display.update()



    def update_liberties(self, added_stone=None):
        """Updates the liberties of the entire board, group by group.

        Usually a stone is added each turn. To allow killing by 'suicide',
        all the 'old' groups should be updated before the newly added one.

        """
        for group in self.groups:
            if added_stone:
                if group == added_stone.group:
                    continue
            group.update_liberties()
        if added_stone:
            added_stone.group.update_liberties()


def get_stone_num():
    black_n, white_n = 0, 0
    for i in range(board_size * board_size):
        if show_board[i] == 'X':
            black_n += 1
        if show_board[i] == 'O':
            white_n += 1
    return black_n, white_n

def get_emptystone_num():
    bem_n, wem_n = 0, 0
    for i in range(board_size * board_size):
        if show_board[i] == '.':
            if i == 0 or i == 6 or i == 42 or i == 48:
                if i == 0 or i == 6:
                    if show_board[i + 7] == 'X':
                         bem_n += 1
                    if show_board[i + 7] == 'O':
                         wem_n += 1
                if i == 42 or i == 48:
                    if show_board[i - 7] == 'X':
                         bem_n += 1
                    if show_board[i - 7] == 'O':
                         wem_n += 1
            if i == 7 or i == 14 or i == 21 or i == 28 or i == 35:
                if show_board[i + 1] == 'X':
                    bem_n += 1
                if show_board[i + 1] == 'O':
                    wem_n += 1
            if i == 1 or i == 2 or i == 3 or i == 4 or i == 5:
                if show_board[i + 1] == 'X':
                    bem_n += 1
                if show_board[i + 1] == 'O':
                    wem_n += 1
            if i == 13 or i == 20 or i == 27 or i == 34 or i == 41:
                if show_board[i - 1] == 'X':
                    bem_n += 1
                if show_board[i - 1] == 'O':
                    wem_n += 1
            if i == 43 or i == 44 or i == 45 or i == 46 or i == 47:
                if show_board[i + 1] == 'X':
                    bem_n += 1
                if show_board[i + 1] == 'O':
                    wem_n += 1
            else:
                if show_board[i + 1] == 'X':
                    bem_n += 1
                if show_board[i + 1] == 'O':
                    wem_n += 1
    return bem_n, wem_n

def display_board():
    print(' ', end = ' ')
    for i in range(board_size):
        print(chr(i + ord('A')), end = ' ')
    print()
    for i in range(len(show_board)):
        if i % board_size == 0 :
            print(board_size - int(i / board_size), end = ' ')
        print(show_board[i], end = ' ')
        if i % board_size == board_size - 1 :
             print()
    print(np_board)


def main():
    end = False
    arm = arm_control.Arm()
    smalltext = pygame.font.Font("./images/FiraCode-Bold.ttf", 15)
    while not end:
        tree = michi.TreeNode(pos = michi.empty_position())
        tree.expand()
        move_done, next_on_hit, pass_on_hit, game_over = False, False, False, False
        c_move, h_move = None, None
        board = Board()
        global remove_list
        global black_num, white_num
        h_color, c_color, n_color = None, None, None
        coord = []
        print('New game!')
        t_start = time.time()
        while not game_over:
            move_done, next_on_hit, pass_on_hit, hint_on_hit = False, False, False, False
            t_end = time.time()
            if n_color is not None:
                """draw time"""
                total_time = round(t_end - t_start, 1)
                minutes =int(total_time // 60)
                seconds = round(total_time % 60, 1)
                screen.blit(white_bar, (345, 333))
                textsurf, textrect = text_objects("Time: " + str(minutes) + ':' + str(seconds), smalltext, RED)
                textrect.center = (405, 355)
                screen.blit(textsurf, textrect)
                pygame.display.update()
            pygame.time.wait(250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    remove_list = []
                    display_board()
                    if event.button == 1 and 395 > event.pos[0] > 335 and 75 > event.pos[1] > 25 and h_color is None:
                        print("You play Black")
                        h_color = "B"
                        c_color = "W"
                        n_color = "B"
                        h_t = time.time()
                        t_start = time.time()
                        area_rect = pygame.Rect((70, 350), (250, 90))
                        screen.blit(background, (70, 350), area_rect)
                        """draw text bar"""
                        screen.blit(text_bar, (70, 350))
                        textsurf, textrect = text_objects("It's your turn!", smalltext, BLUE)
                        textrect.center = (190, 362)
                        screen.blit(textsurf, textrect)
                        pygame.display.update()
                    elif event.button == 1 and 475 > event.pos[0] > 415 and 75 > event.pos[1] > 25 and h_color is None:
                        print("You play white")
                        h_color = "W"
                        c_color = "B"
                        n_color = "B"
                        t_start = time.time()
                        area_rect = pygame.Rect((70, 350), (250, 90))
                        screen.blit(background, (70, 350), area_rect)
                        pygame.display.update()
                    elif event.button == 1 and 475 > event.pos[0] > 345 and 130 > event.pos[1] > 80 and h_color is not None:
                        print("OK!")
                        next_on_hit = True
                    elif event.button == 1 and 475 > event.pos[0] > 345 and 200 > event.pos[1] > 150 and h_color is not None:
                        print('HINT!')
                        hint_on_hit = True
                    elif event.button == 1 and 475 > event.pos[0] > 345 and 270 > event.pos[1] > 210 and h_color is not None:
                        print('Pass move made! turn to another one!')
                        pass_on_hit = True
                    elif event.button == 1 and 475 > event.pos[0] > 345 and 340 > event.pos[1] > 280:
                        print('RESIGN!')
                        h_move = 'resign'
                        move = 'resign'
                    else:
                        print('No command')
            if n_color == c_color and c_color is not None:
                """draw text bar"""
                screen.blit(text_bar, (70, 350))
                screen.blit(text_bar, (70, 380))
                textsurf, textrect = text_objects("It's computer's turn!", smalltext, BLUE)
                textrect.center = (190, 362)
                screen.blit(textsurf, textrect)
                textsurf, textrect = text_objects('Wait for calculating!', smalltext, BLUE)
                textrect.center = (190, 392)
                screen.blit(textsurf, textrect)
                pygame.display.update()
                """"""
                arm.take_photo()
                # c_move = input("c_move :\n")
                # tree, n = michi.gtp_io('play ' + c_color +' ' + c_move, tree)
                print('Wait for calculating!')
                tree, c_move, n=michi.gtp_io('genmove', tree)
                print('gtp return: ',c_color, c_move)
                move = c_move
                arm.move(c_color, c_move)
                move_done = True
                n_color = h_color
                h_t = time.time()
                """draw text bar"""
                area_rect = pygame.Rect((70, 350), (250, 90))
                screen.blit(background, (70, 350), area_rect)
                screen.blit(text_bar, (70, 350))
                textsurf, textrect = text_objects("It's your turn!", smalltext, BLUE)
                textrect.center = (190, 362)
                screen.blit(textsurf, textrect)
                pygame.display.update()
            elif n_color == h_color and c_color is not None:
                h_end = time.time()
                screen.blit(white_bar, (345, 393))
                textsurf, textrect = text_objects("YourTime:" + str(round(h_end - h_t, 1)), smalltext, RED)
                textrect.center = (405, 415)
                screen.blit(textsurf, textrect)
                if pass_on_hit:
                    """Remove the recomand stone as a circle."""
                    while coord:
                        x, y = coord.pop()
                        blit_coords = (x - 20, y - 20)
                        area_rect = pygame.Rect(blit_coords, (40, 40))
                        screen.blit(background, blit_coords, area_rect)
                    area_rect = pygame.Rect((70, 350), (250, 90))
                    screen.blit(background, (70, 350), area_rect)
                    pygame.display.update()
                    """"""
                    move_done = True
                    pass_on_hit = False
                    move = "pass"
                    h_move = move
                    n_color = c_color
                    tree, n = michi.gtp_io('play ' + h_color +' ' + h_move, tree)
                elif hint_on_hit:
                    """draw text bar"""
                    screen.blit(text_bar, (70, 350))
                    textsurf, textrect = text_objects('Wait for hint spot!', smalltext, BLUE)
                    textrect.center = (190, 362)
                    screen.blit(textsurf, textrect)
                    pygame.display.update()
                    print('\nWait for recommand move by MCTS tree')
                    tree1 = copy.deepcopy(tree)
                    tree1, n, pos_winrate = michi.gtp_io('genmove', tree1)
                    pos_winrate = sorted(pos_winrate, key = lambda s: s[1], reverse = True)
                    print(pos_winrate)
                    """Draw the recomend stone """
                    screen.blit(text_bar, (70, 350))
                    screen.blit(text_bar, (70, 380))
                    screen.blit(text_bar, (70, 410))
                    textsurf, textrect = text_objects('Hint spot : ', smalltext, BLUE)
                    textrect.center = (142, 362)
                    screen.blit(textsurf, textrect)
                    for i in range(len(pos_winrate)):
                        """Draw the recomand stone as a circle."""
                        x, y = pos_winrate[i][0]
                        x = int(ord(x) - ord('A')) + 1
                        y = int(y)
                        coord.append((30 + x * 40, 20 + ((board_size + 1 - y) * 40)))
                        pygame.draw.circle(screen, (255 - i * 40, 0 ,0 ), coord[i], 20, 0)
                        """"""
                        if i < 1 :
                            textsurf, textrect = text_objects('{}({})'.format(pos_winrate[i][0], pos_winrate[i][1]), smalltext, BLUE)
                            textrect.center = (240, 362)
                            screen.blit(textsurf, textrect)
                        elif i < 3:
                            textsurf, textrect = text_objects('{}({})'.format(pos_winrate[i][0], pos_winrate[i][1]), smalltext, BLUE)
                            textrect.center = (138 + (i - 1) * 102, 392)
                            screen.blit(textsurf, textrect)
                        else:
                            textsurf, textrect = text_objects('{}({})'.format(pos_winrate[i][0], pos_winrate[i][1]), smalltext, BLUE)
                            textrect.center = (138 + (i - 3) * 102, 422)
                            screen.blit(textsurf, textrect)
                    pygame.display.update()
                elif next_on_hit:
                    """Remove the recomand stone as a circle."""
                    while coord:
                        x, y = coord.pop()
                        blit_coords = (x - 20, y - 20)
                        area_rect = pygame.Rect(blit_coords, (40, 40))
                        screen.blit(background, blit_coords, area_rect)
                    area_rect = pygame.Rect((70, 350), (250, 90))
                    screen.blit(background, (70, 350), area_rect)
                    pygame.display.update()
                    """"""
                    arm.take_photo()
                    img_board = img_process.get_board(debug=False)
                    print(img_board)
                    h_move = img_process.get_move(np_board, img_board, h_color)
                    # h_move = input("h_move and press enter to confirm your move\n")
                    if h_move is None:
                        print("No move found!")
                        h_move = input("Where is your move?")
                    print("move:", h_move)
                    tree, n = michi.gtp_io('play ' + h_color +' ' + h_move, tree)
                    move = h_move
                    n_color = c_color

            if move_done or next_on_hit:
                if move == 'pass':
                    print('Pass move made! turn to another one!')
                    board.turn()
                elif move == 'resign':
                    print('Move resign')
                else:
                    x, y = move
                    x = int(ord(x) - ord('A'))+1
                    y = int(y)
                    stone = board.search(point=(x, y))
                    if stone:
                        stone.remove()
                    else:
                        added_stone = Stone(board, (x, y), board.turn())
                    board.update_liberties(added_stone)
                    """draw count"""
                    black_num, white_num = get_stone_num()
                    screen.blit(text_bar, (70, 5))
                    textsurf, textrect = text_objects("Black: " + str(black_num), smalltext, BLACK)
                    textrect.center = (150, 19)
                    screen.blit(textsurf, textrect)
                    textsurf, textrect = text_objects("White: " + str(white_num), smalltext, BLACK)
                    textrect.center = (245, 19)
                    screen.blit(textsurf, textrect)
                    pygame.display.update()
                print("remove : ", remove_list)
                move_done, next_on_hit = False, False
                while remove_list:
                    coords = remove_list.pop()
                    print(coords)
                    arm.remove_chess(n_color, coords)
                arm.take_photo()
            if (c_move == 'pass' and h_move == 'pass') or c_move == 'resign' or h_move == 'resign':
                """clear area"""
                area_rect = pygame.Rect((70, 350), (250, 90))
                screen.blit(background, (70, 350), area_rect)
                """"""
                screen.blit(text_bar, (70, 350))
                screen.blit(text_bar, (70, 380))
                screen.blit(text_bar, (70, 410))
                textsurf, textrect = text_objects('Press (OK) to', smalltext, BLUE)
                textrect.center = (190, 392)
                screen.blit(textsurf, textrect)
                textsurf, textrect = text_objects('the next game!', smalltext, BLUE)
                textrect.center = (190, 422)
                screen.blit(textsurf, textrect)
                if c_move =='resign':
                    textsurf, textrect = text_objects('You win the game!', smalltext, BLUE)
                    textrect.center = (190, 362)
                    screen.blit(textsurf, textrect)
                elif h_move =='resign':
                    textsurf, textrect = text_objects('Computer win the game!', smalltext, BLUE)
                    textrect.center = (190, 362)
                    screen.blit(textsurf, textrect)
                else:
                    if h_color == 'B':
                        bempty_num, wempty_num = get_emptystone_num()
                        h_empty = bempty_num
                        c_empty = wempty_num
                        h_num = black_num
                        c_num = white_num
                        if h_num > c_num + c_empty - 2:
                            textsurf, textrect = text_objects('You win the game!', smalltext, BLUE)
                            textrect.center = (190, 362)
                            screen.blit(textsurf, textrect)
                        else:
                            textsurf, textrect = text_objects('Computer win the game!', smalltext, BLUE)
                            textrect.center = (190, 362)
                            screen.blit(textsurf, textrect)
                    else:
                        bempty_num, wempty_num = get_emptystone_num()
                        h_empty = wempty_num
                        c_empty = bempty_num
                        h_num = white_num
                        c_num = black_num
                        if h_num > c_num + c_empty - 2:
                            textsurf, textrect = text_objects('You win the game!', smalltext, BLUE)
                            textrect.center = (190, 362)
                            screen.blit(textsurf, textrect)
                        else:
                            textsurf, textrect = text_objects('Computer win the game!', smalltext, BLUE)
                            textrect.center = (190, 362)
                            screen.blit(textsurf, textrect)
                pygame.display.update()
                next_game = False
                while not next_game:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1 and 475 > event.pos[0] > 345 and 130 > event.pos[1] > 80 and h_color is not None:
                                print("OK! next game")
                                next_game = True
                                game_over = True
                            else:
                                print('No command')
                # arm.game_over()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('GoGame')
    icon = pygame.image.load('./images/icon.jpg')
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
    background = pygame.image.load('./images/basemap.jpg').convert()
    text_bar = pygame.image.load('./images/text_bar.png').convert()
    text_bar = pygame.transform.scale(text_bar, (240, 26))
    black_button = pygame.image.load('./images/black_bar.png').convert_alpha()
    black_button = pygame.transform.scale(black_button, (70, 35))
    white_b = pygame.image.load('./images/white_bar.png').convert_alpha()
    white_button = pygame.transform.scale(white_b, (70, 35))
    white_bar = pygame.transform.scale(white_b, (126, 40))
    black_stone = pygame.image.load('./images/black_stone.png').convert_alpha()
    black_stone = pygame.transform.scale(black_stone, (40, 40))
    white_stone = pygame.image.load('./images/white_stone.png').convert_alpha()
    white_stone = pygame.transform.scale(white_stone, (40, 40))
    main()
