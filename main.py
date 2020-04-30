import numpy as np
import tkinter as tk
"""import everything made"""
import michi
import go
# import arm_control
# import img_process
"""========global var============="""
board_size = 7
show_board = ['.'] * board_size * board_size
np_board = np.zeros((board_size, board_size), dtype='u1')
remove_list = []
"""==============================="""


class Stone(go.Stone):
    def __init__(self, board, point, color):
        """Create, initialize and draw a stone."""
        super(Stone, self).__init__(board, point, color)
        self.coords = point[0], point[1]
        self.draw()

    def draw(self):
        """Draw the stone."""
        if self.coords == 'pass':
            return self.coords
        print(self.color, " played: ", chr(self.coords[0]+64), chr(self.coords[1]+48))
        x_pos, y_pos = self.coords
        if self.color == 'B':
            show_board[(x_pos-1)+(8-int(y_pos)-1)*board_size] = "X"

            np_board[8-int(y_pos)-1][x_pos-1] = "1"
        elif self.color == 'W':
            show_board[(x_pos-1)+(8-int(y_pos)-1)*board_size] = "O"

            np_board[8-int(y_pos)-1][x_pos-1] = "2"

    def remove(self):
        """Remove the stone from board."""
        global remove_list
        remove_list.append(self.coords)
        x_pos, y_pos = self.coords
        show_board[x_pos-1+(8-int(y_pos)-1)*board_size] = "."

        np_board[8-int(y_pos)-1][x_pos-1] = "0"

        super(Stone, self).remove()


class Board(go.Board):
    def __init__(self):
        """Create, initialize and draw an empty board."""
        super(Board, self).__init__()
        global show_board, np_board
        show_board = ['.'] * board_size * board_size
        np_board = np.zeros((board_size, board_size), dtype='u1')

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


def display_board():
    print(' ', end=' ')
    for i in range(board_size):
        print(chr(i+ord('A')), end=' ')
    print()
    for i in range(len(show_board)):
        if i % board_size == 0 :
            print(7-int(i / board_size), end=' ')
        print(show_board[i], end=' ')
        if i % board_size == 6 :
             print()
    print(np_board)



def main():
    tree = michi.TreeNode(pos=michi.empty_position())
    tree.expand()
    # arm = arm_control.Arm()
    # arm.reset()
    game_over = False
    end = False

    while not end:
        h_color = input("Which side you wanna take (B/W):").upper()
        if h_color == 'B' or h_color == 'W':
            if h_color == 'W':
                c_color = 'B'
                print("Computer takes black")
            else:
                c_color = 'W'
                print("Computer takes white")
        else:
            print("Wrong input of color!")
            continue
        board = Board()
        n_color = 'B'
        c_move = 0
        # arm.take_photo()  #????
        while not game_over:
            global remove_list, np_board
            remove_list = []
            display_board()
            if n_color == c_color:
                c_move = input("c_move :\n")
                tree, n = michi.gtp_io('play ' + c_color +' ' + c_move, tree)
                # tree, c_move =michi.gtp_io('genmove', tree)
                move = c_move
                n_color = h_color
                # arm.move(c_color, c_move)
            elif n_color == h_color:
                # arm.take_photo()  #????
                # black_num, white_num, img_board = img_process.get_board(debug=False)
                # print(img_board)
                # print("black:", black_num, "white:", white_num)
                # h_move = img_process.get_move(np_board, img_board, h_color)
                # print(h_move)

                h_move = input("h_move :\n")
                tree, n = michi.gtp_io('play ' + h_color +' ' + h_move, tree)
                move = h_move
                n_color = c_color
            else:
                print("Why am I here ?")
            if move == 'pass':
                print('Pass move made! turn to another one!')
                board.turn()
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
            print("remove : ", remove_list)
            while remove_list:
                coords = remove_list.pop()
                arm.remove_chess(n_color, coords)

            if c_move == 'pass' and h_move == 'pass':
                game_over = True


if __name__ == "__main__":
    main()
