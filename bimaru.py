# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 199318 Rita Pessoa
# 102635 Andre Franco

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

from sys import stdin

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    def __init__(self, board, row, column, size):
        self.board = board
        self.row = row
        self.column = column
        self.size = size

    def get_value(self, row: int, col: int) -> str:
        return self.board[row-1][col-1]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        if row == 1:
            t = ('null', self.board[row][col-1])
            return t
        if row == 10:
            t = (self.board[row-2][col-1], 'null')
            return t
        t = (self.board[row-2][col-1], self.board[row][col-1])
        return t

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        if col == 1:
            t = ('null', self.board[row-1][col])
            return t
        if col == 10:
            t = (self.board[row-1][col-2], 'null')
            return t
        t = (self.board[row-1][col-2], self.board[row-1][col])
        return t

    @staticmethod
    def parse_instance():
        #create board as a matrix
        board_array = [['' for i in range(10)] for j in range(10)]
        #create row as the number of pieces on each row missing
        row = stdin.readline().split()
        row = [int(x) for x in row if x.isdigit()]
        #create column as the number of pieces on each column missing
        column = stdin.readline().split()
        column = [int(x) for x in column if x.isdigit()]
        #create hints by placing each hint on the respective spot of the matrix
        hints = int(stdin.readline())
        x = 0
        y = 0
        while x < hints:
            hint = stdin.readline().split()
            h_row = int(hint[1])
            h_col = int(hint[2])
            board_array[h_row][h_col] = hint[3]
            if(hint[3] == 'C'):
                y += 1
            if(hint[3] != 'W'):
                #everytime a piece is added we must remove 1 from the respective row and column values
                row[h_row] = row[h_row] - 1
                column[h_col] = column[h_col] - 1
                #everytime there is a hint that is not water we will put water around it ( with the respective exceptions)
                for i in range(h_row - 1, h_row + 2, 1):
                    if i < 0:
                        continue
                    if i > 9:
                        break
                    for j in range(h_col - 1, h_col + 2, 1):
                        if j < 0 or j > 9 or i == h_row and j == h_col:
                            continue
                        if hint[3] == 'L' and i == h_row and j == h_col + 1:
                            continue
                        if hint[3] == 'R' and i == h_row and j == h_col - 1:
                            continue
                        if hint[3] == 'T' and j == h_col and i == h_row + 1:
                            continue
                        if hint[3] == 'B' and j == h_col and i == h_row - 1:
                            continue
                        if hint[3] == 'M':
                            if j == h_col and i == h_row - 1:
                                continue
                            if j == h_col and i == h_row + 1:
                                continue
                            if j == h_col - 1 and i == h_row:
                                continue
                            if j == h_col + 1 and i == h_row:
                                continue
                        if board_array[i][j] == '':
                            board_array[i][j] = '.'
            x = x + 1
        #given the board_array, the row and column we will create  our Board
        board = Board(board_array, row, column, [4-y, 3, 2, 1])
        return board
    
    def adjacent_positions_empty(self, row: int, col: int):
        n = 0
        for i in range(row - 1, row + 2, 1):
            if i < 0:
                continue
            if i > 9:
                return n
            for j in range(col - 1, col + 2, 1):
                if j < 0 or j > 9 or (i == row and j == col):
                    continue
                if self.board[i][j] != '' and self.board[i][j] != '.' and self.board[i][j] != 'W':   
                    n = n + 1
        return n

    def clear_nearby_positions(self, row: int, col: int, size: int, vertical: bool):
        if vertical:
            for i in range(row - 1, row + size + 1, 1):
                if i < 0:
                    continue
                if i > 9:
                    break
                for j in range(col - 1, col + 2, 1):
                    if j < 0 or j > 9 or (i == row and j == col):
                        continue
                    if self.board[i][j] == '':
                        self.board[i][j] = '.'
        if not vertical:
            for i in range(row - 1, row + 2, 1):
                if i < 0:
                    continue
                if i > 9:
                    break
                for j in range(col - 1, col + size + 1, 1):
                    if j < 0 or j > 9 or (i == row and j == col):
                        continue
                    if self.board[i][j] == '':   
                        self.board[i][j] = '.'
    
    def fill_full_rows(self):
        #if there are no more pieces to put in a row or column we will fill those with water
        for i in range(10):
            if self.row[i] == 0:
                for j in range(10):
                    if self.board[i][j] == '':
                        self.board[i][j] = '.'
            if self.column[i] == 0:
                for j in range(10):
                    if self.board[j][i] == '':
                        self.board[j][i] = '.'

    def print(self):
        for i in range(10):
            for j in range(10):
                if self.board[i][j] == '':
                    print('.', end = '')
                if self.board[i][j] == '.': #to remove
                    print('*', end = '')
                else:
                    print(self.board[i][j], end = '')
            print('\n')
    # TODO: outros metodos da classe

class Bimaru(Problem):
    def __init__(self, board: Board):
        self.board = board
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def get_actions_hints(self, state, piece, row: int, col: int, action):
        i = row
        j = col
        if (piece == 'M' and ((j > 0 and j < 9) or i == 0 or i == 9))  or piece == 'T' or piece == 'B':
            size = min(4, state.board.column[i] + 1)
            for k in range(1, size):
                if state.board.size[k] != 0:
                    if piece == 'T':
                        if state.board.board[i+k][j] != '':
                            break
                        T = ((i, j), (i+k, j), k+1)
                        action.append(T)
                    if piece == 'B':
                        if state.board.board[i-k][j] != '':
                            break
                        T = ((i-k, j), (i, j), k+1)
                        action.append(T)
                if piece == 'M':    
                    if k == 1:
                        if state.board.board[i][j+k] != '' or state.board.board[i][j-k] != '' :
                            break
                        if state.board.size[k+1] != 0:
                            T = ((i, j-k), (i, j+k), k+2)
                            action.append(T)
                        k += 1
                    if k > 2:
                        if state.board.size[k] != 0:
                            if state.board.board[i][j+k] == '':
                                T = ((i, j-k+1), (i, j+k), k+1)
                                action.append(T)
                            if state.board.board[i][j-k] == '':
                                T = ((i, j-k), (i, j+k-1), k+1)
                                action.append(T)
        if (piece == 'M' and ((i > 0 and i < 9) or j == 0 or j == 9))  or piece == 'R' or piece == 'L':
            size = min(4, state.board.row[i] + 1)
            for k in range(1, size):
                if state.board.size[k] != 0:
                    if piece == 'R':
                        if state.board.board[i][j-k] != '':
                            break
                        T = ((i, j-k), (i, j), k+1)
                        action.append(T)
                    if piece == 'L':
                        if state.board.board[i][j+k] != '':
                            break
                        T = ((i, j), (i, j+k), k+1)
                        action.append(T)
                if piece == 'M':
                    if k == 1:
                        if state.board.board[i+k][j] != '' or state.board.board[i-k][j] != '':
                            break
                        if state.board.size[k+1] != 0:
                            T = ((i-k, j), (i+k, j), k+2)
                            action.append(T)
                        k += 1
                    if k > 2:
                        if state.board.size[k] != 0:
                            if state.board.board[i+k][j] == '':
                                T = ((i-k+1, j), (i+k, j), k+1)
                                action.append(T)
                            if state.board.board[i-k][j] == '':
                                T = ((i-k, j), (i+k-1, j), k+1)
                                action.append(T)      
        return action
    
    def check_actions_empty(self, state: BimaruState, row: int, col: int):
        if state.board.adjacent_positions_empty(row, col) != 0:
            return False
        if ((row > 1 and state.board.board[row-2][col] == 'T') or (row < 8 and state.board.board[row+2][col] == 'B') 
        or (col > 1 and state.board.board[row][col-2] == 'L') or (col < 8 and state.board.board[row][col+2] == 'R')):
            return False
        return True

    def actions(self, state: BimaruState):
        action = list()
        size1 = state.board.size[0]
        for i in range(10):
            row = state.board.row[i]
            if row == 0:
                continue
            for j in range(10):
                piece = state.board.board[i][j]
                if state.board.column[j] == 0:
                    continue
                if piece == '.' or piece == 'W':
                    continue
                if piece != '':
                    if self.check_valid_positions(state, i, j) == -1:
                        action = self.get_actions_hints(state, piece, i, j, action)
                if piece == '':
                    if not self.check_actions_empty(state, i, j):
                        continue
                    if size1 != 0: 
                        T = ((i, j), (i, j), 1)
                        action.append(T)
                    size = min(4, row)
                    for k in range(1, size):
                        if j + k > 9:
                            break
                        if state.board.size[k] == 0:
                            continue
                        if not self.check_actions_empty(state, i, j+k) or state.board.board[i][j+k] != '':
                            break
                        T = ((i, j), (i, j+k), k+1)
                        action.append(T)
                    size = min(4, state.board.column[j])
                    for k in range(1, size):
                        if i + k > 9:
                            break
                        if state.board.size[k] == 0:
                            continue
                        if not self.check_actions_empty(state, i+k, j) or state.board.board[i+k][j] != '':
                            break
                        T = ((i, j), (i+k, j), k+1)
                        action.append(T)
        return action
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

    def add_position(self, state: BimaruState, row: int, col: int, piece, size: int):
        if state.board.board[row][col] == '':
            state.board.board[row][col] = piece
            state.board.row[row] = state.board.row[row] - 1
            state.board.column[col] = state.board.column[col] - 1
            if size == 1:
                state.board.clear_nearby_positions(row, col, size, False)
                state.board.fill_full_rows()

    def result(self, state: BimaruState, action):
        new_board_array = [[state.board.board[i][j] for j in range(10)] for i in range(10)]
        new_row = [state.board.row[i] for i in range(10)]
        new_column = [state.board.column[i] for i in range(10)]
        new_size = [state.board.size[i] for i in range(4)]
        new_board = Board(new_board_array, new_row, new_column, new_size)
        new_state = BimaruState(new_board)
        posx_i = action[0][0]
        posy_i = action[0][1]
        posx_f = action[1][0]
        posy_f = action[1][1]
        size = action[2]
        if size == 1:
            self.add_position(new_state, posx_i, posy_i, 'C', size)
            new_state.board.size[size-1] -= 1
            return new_state
        if posx_i == posx_f:
            if size >= 3:
                self.add_position(new_state, posx_i, posy_i + 1, 'M', size)
                if size == 4:
                    self.add_position(new_state, posx_i, posy_i + 2, 'M', size)
            new_state.board.size[size-1] -= 1
            self.add_position(new_state, posx_i, posy_i, 'L', size)
            self.add_position(new_state, posx_f, posy_f, 'R', size)
            new_state.board.clear_nearby_positions(posx_i, posy_i, size, False)
        if posy_i == posy_f:
            if size >= 3:
                self.add_position(new_state, posx_i + 1, posy_i, 'M', size)
                if size == 4:
                    self.add_position(new_state, posx_i + 2, posy_i, 'M', size)
            new_state.board.size[size-1] -= 1
            self.add_position(new_state, posx_i, posy_i, 'T', size)
            self.add_position(new_state, posx_f, posy_f, 'B', size)
            new_state.board.clear_nearby_positions(posx_i, posy_i, size, True)
        new_state.board.fill_full_rows()
        return new_state

    def check_size_pieces(self, state: BimaruState):
        for i in range(10):
            for j in range(10):
                if (state.board.board[i][j] == 'R' or state.board.board[i][j] == 'B'):
                    size = self.check_valid_positions(state, i, j)
                    if size == -1:
                        continue
                    state.board.size[size - 1] -= 1
    
    def goal_test(self, state: BimaruState):
        if state.board.size[0] != 0 or state.board.size[1] != 0 or state.board.size[2] != 0 or state.board.size[3] != 0:
            return False
        for i in range(10):
            if state.board.row[i] != 0 or state.board.column[i] != 0:
                return False
            for j in range(10):
                if(state.board.board[i][j] != '' and state.board.board[i][j] != '.' and state.board.board[i][j] != 'W'):
                    size = self.check_valid_positions(state, i, j)
                    if size == -1:
                        return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    def check_valid_positions(self, state: BimaruState, row: int, col:int) -> bool:
        i = row
        j = col
        piece = state.board.board[i][j]
        if piece == 'C':
            if state.board.adjacent_positions_empty(i, j) != 0:
                return -1
            return 1
        if piece == 'M':
            if state.board.adjacent_positions_empty(i, j) != 2:
                return -1
            HBorders = state.board.adjacent_horizontal_values(i+1, j+1)
            VBorders = state.board.adjacent_vertical_values(i+1, j+1)
            if VBorders != ('T', 'B') and VBorders != ('T', 'M') and VBorders != ('M', 'B') and HBorders != ('L', 'M') and HBorders != ('L', 'R') and HBorders != ('M', 'R'):
                return -1
        if piece != 'C' and piece != 'M':
            if state.board.adjacent_positions_empty(i, j) != 1:
                return -1
            if piece == 'L':
                RBorder = state.board.board[i][j+1]
                if RBorder != 'R' and RBorder != 'M':
                    return -1
            if piece == 'R':
                LBorder = state.board.board[i][j-1]
                if LBorder != 'L' and LBorder != 'M':
                    return -1
                for n in range(1, 5):
                    if j - n < 0:
                        return n
                    if state.board.board[i][j-n] == '' or state.board.board[i][j-n] == '.' or state.board.board[i][j-n] == 'W':
                        return n
            if piece == 'T':
                BBorder = state.board.board[i+1][j]
                if BBorder != 'M' and BBorder != 'B':
                    return -1
            if piece == 'B':
                TBorder = state.board.board[i-1][j] 
                if TBorder != 'T' and TBorder != 'M':
                    return -1
                for n in range(1, 5):
                    if i - n < 0:
                        return n
                    if state.board.board[i-n][j] == '' or state.board.board[i-n][j] == '.' or state.board.board[i-n][j] == 'W':
                        return n
        return 0
    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    board.fill_full_rows()
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    bimaru = Bimaru(board)
    bimaru_state = BimaruState(board)
    bimaru.check_size_pieces(bimaru_state)
    print(bimaru.actions(bimaru_state))
    #b1 = bimaru.result(bimaru_state, ((0, 0), (3, 0), 4))
    #print(bimaru.actions(bimaru_state))
    bimaru.board.print()
    pass
