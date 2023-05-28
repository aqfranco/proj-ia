# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

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
    def __init__(self, board, row, column):
        self.board = board
        self.row = row
        self.column = column

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
        board_array = [['' for i in range(10)] for j in range(10)]
        row = stdin.readline().split()
        row = [int(x) for x in row if x.isdigit()]
        column = stdin.readline().split()
        column = [int(x) for x in column if x.isdigit()]
        hints = int(stdin.readline())
        x = 0
        while x < hints:
            hint = stdin.readline().split()
            board_array[int(hint[1])][int(hint[2])] = hint[3]
            row[int(hint[1])] = row[int(hint[1])] - 1
            column[int(hint[2])] = column[int(hint[2])] - 1
            x = x + 1
        board = Board(board_array, row, column)
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

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        new_board_array = [[state.board.board[i][j] for j in range(10)] for i in range(10)]
        new_row = [state.board.row[i] for i in range(10)]
        new_column = [state.board.column[i] for i in range(10)]
        new_board = Board(new_board_array, new_row, new_column)
        new_state = BimaruState(new_board)
        posx_i = action[0][0]
        posy_i = action[0][1]
        posx_f = action[1][0]
        posy_f = action[1][1]
        size = action[2]
        if not isinstance(size, int) and size == 'W':
            new_state.board.board[posx_i][posy_i] = 'W'
            new_state.board.fill_full_rows()
            return new_state
        if size == 1:
            new_state.board.board[posx_i][posy_i] = 'C'
            new_state.board.clear_nearby_positions(posx_i, posy_i, size, False)
            new_state.board.row[posx_i] = new_state.board.row[posx_i] - 1
            new_state.board.column[posy_i] = new_state.board.column[posy_i] - 1
            new_state.board.fill_full_rows()
            return new_state
        if posx_i == posx_f:
            if size >= 3:
                new_state.board.board[posx_i][posy_i + 1] = 'M'
                new_state.board.column[posy_i + 1] = new_state.board.column[posy_i + 1] - 1
                if size == 4:
                    new_state.board.board[posx_i][posy_i + 2] = 'M'
                    new_state.board.column[posy_i + 2] = new_state.board.column[posy_i + 2] - 1
            new_state.board.board[posx_i][posy_i] = 'L'
            new_state.board.board[posx_f][posy_f] = 'R'
            new_state.board.row[posx_i] = new_state.board.row[posx_i] - size
            new_state.board.column[posy_i] = new_state.board.column[posy_i] - 1
            new_state.board.column[posy_f] = new_state.board.column[posy_f] - 1
            new_state.board.clear_nearby_positions(posx_i, posy_i, size, False)
        if posy_i == posy_f:
            if size >= 3:
                new_state.board.board[posx_i + 1][posy_i] = 'M'
                new_state.board.row[posx_i + 1] = new_state.board.row[posx_i + 1] - 1
                if size == 4:
                    new_state.board.board[posx_i + 2][posy_i] = 'M'
                    new_state.board.row[posx_i + 2] = new_state.board.row[posx_i + 2] - 1
            new_state.board.board[posx_i][posy_i] = 'T'
            new_state.board.board[posx_f][posy_f] = 'B'
            new_state.board.column[posy_i] = new_state.board.column[posy_i] - size
            new_state.board.row[posx_i] = new_state.board.row[posx_i] - 1
            new_state.board.row[posx_f] = new_state.board.row[posx_f] - 1
            new_state.board.clear_nearby_positions(posx_i, posy_i, size, True)
        new_state.board.fill_full_rows()
        return new_state

    def goal_test(self, state: BimaruState):
        size1 = 0
        size2 = 0
        size3 = 0 
        size4 = 0
        for i in range(10):
            if state.board.row[i] != 0 or state.board.column[i] != 0:
                return False
            for j in range(10):
                if(state.board.board[i][j] != '' and state.board.board[i][j] != '.' and state.board.board[i][j] != 'W'):
                    size = self.check_valid_positions(state, i, j)
                    if size == -1:
                        return False
                    if size == 1:
                        if size1 == 4:
                            return False
                        if size1 < 4:
                            size1 = size1 + 1
                    if size == 2:
                        if size2 == 3:
                            return False
                        if size2 < 3:
                            size2 = size2 + 1
                    if size == 3:
                        if size3 == 2:
                            return False
                        if size3 < 2:
                            size3 = size3 + 1
                    if size == 4:
                        if size4 == 1:
                            return False
                        if size4 < 1:
                            size4 = size4 + 1
        if size1 == 4 and size2 == 3 and size3 == 2 and size4 == 1:
            return True
        return False

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
    #board.fill_full_rows()
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    bimaru = Bimaru(board)
    bimaru_state = BimaruState(board)
    b1 = bimaru.result(bimaru_state, ((0, 0), (2, 0), 3))
    #print(bimaru.goal_test(bimaru_state))
    pass
