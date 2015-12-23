# coding: utf-8

class MinimaxPlayer:

    def __init__(self, color):
        self.color = color
        if(self.color == 'o'):
            self.opponent_color = '@'
        else:
            self.opponent_color = 'o'

    def play(self, board):
        ignore, move = self.evaluate(board, 1, 4, -float("inf"), float("inf"))
        return move

    def evaluate_board(self, board):
        return self.score(board)

    def score(self, board):
        score = {'@': 0, 'o': 0, '.': 0}
        for i in range(1, 9):
          for j in range(1, 9):
            score[board.get_square_color(i, j)] += 1
        return score[self.color]

    def mobility(self, board):
        return board.valid_moves(self.color).__len__() - board.valid_moves(self.opponent_color).__len__()

    # Funcão que, dado um board, retorna o melhor movimento.
    # É recursiva.
    # board = board do jogo
    # nodeType = 1 se for MAX, -1 se for MIN
    # depth = profundidade em que a busca ja foi
    def evaluate(self, board, nodeType, depth, alpha, beta):
        # se ainda nao chegou no final
        if(depth > 0):
            if(nodeType == 1):
                cur_value = alpha
                comp = max
            else:
                cur_value = beta
                comp = min
            cur_move = None
            # para cada movimento possivel
            for move in board.valid_moves(self.color):
                # faz um clone do board, em que o movimento foi feito
                child = board.get_clone()
                child.play(move, self.color)
                # pega o valor do no filho (ignorando o movimento)
                # na chamada recursiva, inverte o tipo e reduz a profundidade
                if(nodeType == 1):
                    value, ignore = self.evaluate(child, -nodeType, depth-1, cur_value, beta)
                else:
                    value, ignore = self.evaluate(child, -nodeType, depth-1, alpha, cur_value)

                if(comp([cur_value, value]) == value):
                    cur_value = value
                    cur_move = move
                if(nodeType == 1):
                    if(cur_value >= beta): return (cur_value, cur_move)
                else:
                    if(cur_value <= alpha): return (cur_value, cur_move)
            # retorna o valor e o movimento que sao os melhores
            return (cur_value, cur_move)
        # se nao deve mais descer
        else:
            return (self.evaluate_board(board), None)
