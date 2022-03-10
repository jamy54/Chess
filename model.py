import enum
import copy

# creating enumerations using class
class Name(enum.Enum):
    pawn = 1
    rook = 2
    knight = 3
    bishop = 4
    queen = 5
    king = 6


class Entity:
    def __init__(self, gen=None, symb='.', pos=None, isWhite=None):
        self.genere = gen
        self.symbol = symb
        self.position = pos
        self.IsWhite = isWhite
        self.value = self.get_value(gen)

    def get_value(self, name):
        if name == Name.pawn:
            return 100
        elif name == Name.rook:
            return 500
        elif name == Name.knight:
            return 310
        elif name == Name.bishop:
            return 320
        elif name == Name.queen:
            return 900
        elif name == Name.king:
            return 10000
        else:
            return 0

    def is_empty(self):
        return self.genere is None

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        if (isinstance(other, Entity)):
            return self.genere == other.genere and self.symbol == other.symbol and self.IsWhite == other.IsWhite and self.value == other.value
        return False
class Board:
    def __init__(self):
        self.places = [[Entity(pos=[i, j]) for j in range(8)] for i in range(8)]
        self.temp_mov = []
        self.last_move = dict.fromkeys([True,False], None)

    def setup_board(self):
        self.draw_pawn()
        self.draw_rook()
        self.draw_knight()
        self.draw_bishop()
        self.draw_queen()
        self.draw_king()

    def draw_pawn(self):
        for i in range(8):
            self.places[1][i] = Entity(Name.pawn, 'p', [1, i], True)
            self.places[6][i] = Entity(Name.pawn, 'p'.upper(), [6, i], False)

    def draw_rook(self):
        for i in range(2):
            self.places[0][i * 7] = Entity(Name.rook, 'r', [0, i * 7], True)
            self.places[7][i * 7] = Entity(Name.rook, 'r'.upper(), [7, i * 7], False)

    def draw_knight(self):
        for i in range(2):
            self.places[0][i * 5 + 1] = Entity(Name.knight, 't', [0, i * 5 + 1], True)
            self.places[7][i * 5 + 1] = Entity(Name.knight, 't'.upper(), [7, i * 5 + 1], False)

    def draw_bishop(self):
        for i in range(2):
            self.places[0][i * 2 + 2 + i] = Entity(Name.bishop, 'b', [0, i * 2 + 2 + i], True)
            self.places[7][i * 2 + 2 + i] = Entity(Name.bishop, 'b'.upper(), [7, i * 2 + 2 + i], False)

    def draw_queen(self):
        for i in range(1):
            self.places[0][3] = Entity(Name.queen, 'q', [0, 3], True)
            self.places[7][3] = Entity(Name.queen, 'q'.upper(), [7, 3], False)

    def draw_king(self):
        for i in range(1):
            self.places[0][4] = Entity(Name.king, 'k', [0, 4], True)
            self.places[7][4] = Entity(Name.king, 'k'.upper(), [7, 4], False)

    def get_piece_by_pos(self, pos):
        return self.places[pos[0]][pos[1]]

    def set_piece(self, pos, entity):
        entity.position = pos
        self.places[pos[0]][pos[1]] = entity

    def get_score(self, IsWhite):
        score = 0
        for place in self.places:
            for p in place:
                if p.IsWhite == IsWhite:
                    score = score + p.value
        return score

    def draw_board(self,move=None):
        data = ''
        for place in self.places:
            for p in place:
                # data = data + p.symbol + str(p.position[0]) + str(p.position[1])
                data = data + p.symbol
            data = data + '\n'
        print("\n"+data+"\n" + str(move) +"\n")
        f = open("boardview.txt", "a")
        f.write("\n"+data+"\n" + str(move) +"\n")
        f.close()

    def make_temp_move(self, move):
        fro = move[0]
        to = move[1]
        tem_fro, temp_to = copy.deepcopy(fro),copy.deepcopy(to)
        self.temp_mov.append([tem_fro,temp_to])
        #self.draw_board("age, count: "+str(len( self.temp_mov))+"fro pos: "+ str(tem_fro.position)+"to pos: "+ str(temp_to.position))
        self.set_piece(to.position, fro)
        self.set_piece(tem_fro.position, Entity(pos=tem_fro.position))
        #self.draw_board("pore, count: "+str(len( self.temp_mov))+"fro pos: "+ str(tem_fro.position)+"to pos: "+ str(temp_to.position))
        pass



    def undo_move(self):
        if len(self.temp_mov) != 0:
            move = self.temp_mov.pop()
            tem_fro, temp_to = move[0], move[1]
            self.set_piece(tem_fro.position, tem_fro)
            self.set_piece(temp_to.position, temp_to)
            #self.draw_board("undo")
            return  [tem_fro,temp_to]

    def Is_Reverse_move(self,move):
        fro = move[0]
        to = move[1]
        last_move = self.last_move[fro.IsWhite]
        if last_move is None:
            return False
        elif last_move[0] == fro and last_move[1] == to:
            return True

        return False

    def make_move(self, move):
        fro = move[0]
        to = move[1]
        tem_fro, temp_to = copy.deepcopy(fro),copy.deepcopy(to)
        self.set_piece(to.position, fro)
        self.set_piece(tem_fro.position, Entity(pos=tem_fro.position))
        self.last_move[tem_fro.IsWhite] = [tem_fro, temp_to]
