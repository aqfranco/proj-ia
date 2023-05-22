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
            return "(" + self.board[row][col-1] + ")"
        if row == 10:
            return "(" + self.board[row-2][col-1] + ")"
        return "(" + self.board[row-2][col-1] + ", " + self.board[row][col-1] + ")"

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        if col == 1:
            return "(" + self.board[row-1][col] + ")"
        if col == 10:
            return "(" + self.board[row-1][col-2] + ")"
        return "(" + self.board[row-1][col-2] + ", " + self.board[row-1][col] + ")"

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
            x = x + 1
        board = Board(board_array, row, column)
        return board

    def adjacent_positions_empty(self, row: int, col: int) -> int:
        n = 0
        for i in range(row - 1, row + 2, 1):
            for j in range(col - 1, col + 2, 1):
                if i < 0 or i > 9 or j < 0 or j > 9 or (i == row and j == col):
                    continue
                if self.board[i][j] != '' and self.board[i][j] != '.' and self.board[i][j] != 'W':
                    n = n + 1
        return n

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
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        for i in range(10):
            n = 0
            for j in range(10):
                if(state.board.board[i][j] != '' and state.board.board[i][j] != '.' and state.board.board[i][j] != 'W'):
                    if not self.check_valid_positions(i, j):
                        return False
                    n = n + 1
            if n != state.board.row[i]:
                return False
        for j in range(10):
            n = 0
            for i in range(10):
                if(state.board.board[i][j] != '' and state.board.board[i][j] != '.' and state.board.board[i][j] != 'W'):
                    n = n + 1
            if n != state.board.column[j]:
                return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    def check_valid_positions(self, row: int, col:int) -> bool:
        i = row
        j = col
        piece = self.board.board[i][j]
        if piece == 'C':
            if self.board.adjacent_positions_empty(i, j) != 0:
                return False
        if piece == 'M':
            if self.board.adjacent_positions_empty(i, j) != 2:
                return False
            HBorders = self.board.adjacent_horizontal_values(i+1, j+1)
            VBorders = self.board.adjacent_vertical_values(i+1, j+1)
            if VBorders != '(T, B)' and VBorders != '(T, M)' and VBorders != '(M, B)' and HBorders != '(L, M)' and HBorders != '(L, R)' and HBorders != '(M, R)':
                return False
        if piece != 'C' and piece != 'M':
            if self.board.adjacent_positions_empty(i, j) != 1:
                return False
            if piece == 'L':
                RBorder = self.board.board[i][j+1]
                if RBorder != 'R' and RBorder != 'M':
                    return False
            if piece == 'R':
                LBorder = self.board.board[i][j-1]
                if LBorder != 'L' and LBorder != 'M':
                    return False
            if piece == 'T':
                BBorder = self.board.board[i+1][j]
                if BBorder != 'M' and BBorder != 'B':
                    return False
            if piece == 'B':
                TBorder = self.board.board[i-1][j] 
                if TBorder != 'T' and TBorder != 'M':
                    return False
        return True
    
    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    bimaru = Bimaru(board)
    bimaru_state = BimaruState(board)
    
    print(bimaru.goal_test(bimaru_state))

    pass
