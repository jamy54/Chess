# your code goes here
import string
import os
import sys
import time
from model import Board
from algo import  Alg

if __name__ == '__main__':
    board = Board()
    board.setup_board()
    IsWhite = True
    turns = 0
    intelligence_level = 4
    turn_number = 500


    board.draw_board()
    time.sleep(1)
    alg = Alg(board)

    f = open("boardview.txt", "w")
    f.write("")
    f.close()

    while not alg.rule.IsCheckmate(IsWhite) and turns < turn_number:

        move,value = alg.GetMinMaxMove(intelligence_level, IsWhite,-sys.maxsize - 1, sys.maxsize)
        board.make_move(move)
        board.draw_board("final move")

        IsWhite = not IsWhite
        turns = turns + 1


    if turns<turn_number:
        print(str(IsWhite)+' wins')
    else:
        print('game tied')