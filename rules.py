# helper function to figure out if a move is legal for straight-line moves (rooks, bishops, queens, pawns)
# returns True if the path is clear for a move (from-square and to-square), non-inclusive
from model import Name, Entity


class Rule:
    def __init__(self, board):
        self.board = board

    def IsClearPath(self, fro, to):
        new_fro = Entity(pos=[-1,-1])
        if abs(fro.position[0] - to.position[0]) <= 1 and abs(fro.position[1] - to.position[1]) <= 1:
            return True
        else:
            if abs(fro.position[0] - to.position[0]) > 0 and abs(fro.position[1] - to.position[1]) == 0:
                i = -1 if fro.position[0] > to.position[0] else 1
                new_fro = self.board.get_piece_by_pos([fro.position[0] + i, fro.position[1]])
            elif abs(fro.position[1] - to.position[1]) > 0 and abs(fro.position[0] - to.position[0]) == 0:
                i = -1 if fro.position[1] > to.position[1] else 1
                new_fro = self.board.get_piece_by_pos([fro.position[0], fro.position[1] + i])

            elif abs(fro.position[1] - to.position[1]) == abs(fro.position[0] - to.position[0]):
                i = -1 if fro.position[0] > to.position[0] else 1
                j = -1 if fro.position[1] > to.position[1] else 1
                new_fro = self.board.get_piece_by_pos([fro.position[0] + i, fro.position[1] + j])
        if not new_fro.is_empty():
            return False
        else:
            return self.IsClearPath(new_fro, to)


    def IsMoveLegal(self, from_piece, to_piece):
        if from_piece.IsWhite == to_piece.IsWhite:
            return False

        if from_piece.genere == Name.pawn:
            if to_piece.is_empty() and from_piece.position[1] == to_piece.position[1] and \
                (((from_piece.position[0] - to_piece.position[0]) == 1 and not from_piece.IsWhite) or (
                        (from_piece.position[0] - to_piece.position[0]) == -1 and from_piece.IsWhite)):
                return True
            elif to_piece.is_empty() and from_piece.position[1] == to_piece.position[1] and \
                (((from_piece.position[0] - to_piece.position[0]) == 2 and not from_piece.IsWhite) or (
                        (from_piece.position[0] - to_piece.position[0]) == -2 and from_piece.IsWhite)) and \
                    ((from_piece.position[0] == 1 and from_piece.IsWhite) or (
                            from_piece.position[0] == 6 and not from_piece.IsWhite)):
                if self.IsClearPath(from_piece, to_piece):
                    return True
            elif (not to_piece.is_empty() and to_piece.IsWhite != from_piece.IsWhite):
                if (((from_piece.position[0] - to_piece.position[0]) == 1 and not from_piece.IsWhite) or (
                        (from_piece.position[0] - to_piece.position[0]) == -1 and from_piece.IsWhite)) and \
                        (((from_piece.position[1] - to_piece.position[1]) == 1 and not from_piece.IsWhite) or (
                                (from_piece.position[1] - to_piece.position[1]) == -1 and from_piece.IsWhite)):
                    return True

        elif from_piece.genere == Name.rook:
            if to_piece.position[0] == from_piece.position[0] or to_piece.position[1] == from_piece.position[1]:
                if to_piece.is_empty() or to_piece.IsWhite != from_piece.IsWhite:
                    if self.IsClearPath(from_piece, to_piece):
                        return True

        elif from_piece.genere == Name.bishop:
            if abs(from_piece.position[1] - to_piece.position[1]) == abs(from_piece.position[0] - to_piece.position[0]):
                if to_piece.is_empty() or to_piece.IsWhite != from_piece.IsWhite:
                    if self.IsClearPath(from_piece, to_piece):
                        return True

        elif from_piece.genere == Name.queen:
            if to_piece.position[0] == from_piece.position[0] or to_piece.position[1] == from_piece.position[1]:
                if to_piece.is_empty() or to_piece.IsWhite != from_piece.IsWhite:
                    if self.IsClearPath(from_piece, to_piece):
                        return True
            elif abs(from_piece.position[1] - to_piece.position[1]) == abs(from_piece.position[0] - to_piece.position[0]):
                if to_piece.is_empty() or to_piece.IsWhite != from_piece.IsWhite:
                    if self.IsClearPath(from_piece, to_piece):
                        return True

        elif from_piece.genere == Name.knight:
            col_diff = to_piece.position[1] - from_piece.position[1]
            row_diff = to_piece.position[0] - from_piece.position[0]
            if (col_diff == 1 and row_diff == -2) or \
                    (col_diff == 2 and row_diff == -1) or \
                    (col_diff == 2 and row_diff == 1) or \
                    (col_diff == 1 and row_diff == 2) or \
                    (col_diff == -1 and row_diff == -2) or \
                    (col_diff == -2 and row_diff == -1) or \
                    (col_diff == -2 and row_diff == 1) or \
                    (col_diff == -1 and row_diff == 2):
                if to_piece.is_empty() or to_piece.IsWhite != from_piece.IsWhite:
                    return True

        elif from_piece.genere == Name.king:
            if abs(from_piece.position[0] - to_piece.position[0]) <= 1 and abs(
                    from_piece.position[1] - to_piece.position[1]) <= 1:
                if to_piece.is_empty() or to_piece.IsWhite != from_piece.IsWhite:
                    return True

        return False


    def GetListOfLegalMoves(self, IsWhite, piece=None):
        moves = []
        for place in self.board.places:
            for p in place:
                if piece is None or id(piece) == id(p):
                    if p.IsWhite == IsWhite:
                        for i in range(8):
                            for j in range(8):
                                t = self.board.get_piece_by_pos([i, j])
                                if self.IsMoveLegal(p, t) and not self.DoesMovePutPlayerInCheck(p, t):
                                    moves.append([p, t])
        return moves


    # gets a list of all pieces for the current player that have legal moves
    def GetPiecesWithLegalMoves(self, IsWhite):
        pieces = []
        for i in range(8):
            for j in range(8):
                p = self.board.get_piece_by_pos([i, j])
                if p.IsWhite == IsWhite:
                    moves = self.GetListOfLegalMoves(p.IsWhite, p)
                    if len(moves) > 0:
                        pieces.append([p, moves])
        return pieces


    # returns True if the current player is in checkmate, else False
    def IsCheckmate(self, IsWhite):
        moves = self.GetListOfLegalMoves(IsWhite)
        return len(moves) == 0


    def find_king(self, IsWhite):
        for place in self.board.places:
            for p in place:
                if p.IsWhite == IsWhite and p.genere == Name.king:
                    return p


    # returns True if the given player is in Check state
    def IsInCheck(self, IsWhite):
        king = self.find_king(IsWhite)
        for i in range(8):
            for j in range(8):
                p = self.board.get_piece_by_pos([i, j])
                if not p.is_empty() and self.IsMoveLegal(p, king):
                    return True
        return False


    def DoesMovePutPlayerInCheck(self, fro, to):
        self.board.make_temp_move([fro,to])
        res = self.IsInCheck(fro.IsWhite)
        move = self.board.undo_move()
        fro.position = move[0].position
        to.position = move[1].position
        return res


