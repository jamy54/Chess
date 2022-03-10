
from rules import Rule

import sys
import random

class Alg:
    def __init__(self, board):
        self.board = board
        self.rule = Rule(board)

    def evl(self, IsWhite):
        # this function will calculate the score on the board, if a move is performed
        # give score for each of piece and calculate the score for the chess board
        if IsWhite:
            return self.board.get_score(True) - self.board.get_score(False)
        else:
            return self.board.get_score(False) - self.board.get_score(True)


    def GetMinMaxMove(self, depth, IsWhite,alpha,beta):
        if depth == 0 or self.rule.IsCheckmate(IsWhite):
            return None, self.evl(IsWhite)
        moves = self.rule.GetListOfLegalMoves(IsWhite)
        best_move = random.choice(moves)

        if IsWhite:
            max_val = -sys.maxsize - 1
            for move in moves:
                self.board.make_temp_move(move)
                cur_eval = self.GetMinMaxMove(depth - 1, False,alpha,beta)
                m = self.board.undo_move()
                move[0].position = m[0].position
                move[1].position = m[1].position

                if cur_eval[1] > max_val and not self.board.Is_Reverse_move(move):
                    max_val = cur_eval[1]
                    best_move = move
                alpha = max(alpha,cur_eval[1])
                if beta<= alpha:
                    break
            return best_move, max_val
        else:
            min_val = sys.maxsize
            e_moves = self.rule.GetListOfLegalMoves(False)
            for e_move in e_moves:
                self.board.make_temp_move(e_move)
                cur_eval = self.GetMinMaxMove(depth - 1, True,alpha,beta)
                m = self.board.undo_move()
                e_move[0].position = m[0].position
                e_move[1].position = m[1].position
                if cur_eval[1] < min_val and not self.board.Is_Reverse_move(e_move):
                    min_val = cur_eval[1]
                    best_move = e_move
                beta = min(beta, cur_eval[1])
                if beta <= alpha:
                    break
            return best_move, min_val


