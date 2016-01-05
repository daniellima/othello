# coding: utf-8


class MinimaxPlayer:
    def __init__(self, color, depth=4):
        from models.board import Board
        self.color = color
        self.depth = depth
        self.opponent_color = Board.BLACK if color is Board.WHITE else Board.WHITE

    def evaluate_board(self, board):
        score = 10 * self.score_evaluation(board)
        corner = 801.724 * self.corner_evaluation(board)
        corner_c = 382.026 * self.corner_closeness_evaluation(board)
        mobility = 78.922 * self.mobility_evaluation(board)
        frontier = 74.396 * self.frontier_evaluation(board)
        value = 10 * self.value_evaluation(board)
        return score+corner+corner_c+mobility+frontier+value

    def corner_evaluation(self, board):
        count = 0
        opp_count = 0
        if board.get_square_color(1, 1) == self.color:
            count += 1
        elif board.get_square_color(1, 1) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(1, 8) == self.color:
            count += 1
        elif board.get_square_color(1, 8) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(8, 1) == self.color:
            count += 1
        elif board.get_square_color(8, 1) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(8, 8) == self.color:
            count += 1
        elif board.get_square_color(8, 8) == self.opponent_color:
            opp_count += 1

        return 25 * count - 25 * opp_count

    def corner_closeness_evaluation(self, board):
        from models.board import Board

        count = 0
        opp_count = 0
        if board.get_square_color(2, 1) == self.color:
            count += 1
        elif board.get_square_color(2, 1) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(1, 2) == self.color:
            count += 1
        elif board.get_square_color(1, 2) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(2, 2) == self.color:
            count += 1
        elif board.get_square_color(2, 2) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(2, 8) == self.color:
            count += 1
        elif board.get_square_color(2, 8) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(2, 7) == self.color:
            count += 1
        elif board.get_square_color(2, 7) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(1, 7) == self.color:
            count += 1
        elif board.get_square_color(1, 7) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(7, 1) == self.color:
            count += 1
        elif board.get_square_color(7, 1) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(7, 2) == self.color:
            count += 1
        elif board.get_square_color(7, 2) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(8, 2) == self.color:
            count += 1
        elif board.get_square_color(8, 2) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(7, 8) == self.color:
            count += 1
        elif board.get_square_color(7, 8) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(7, 7) == self.color:
            count += 1
        elif board.get_square_color(7, 7) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(8, 7) == self.color:
            count += 1
        elif board.get_square_color(8, 7) == self.opponent_color:
            opp_count += 1

        if self.color == Board.WHITE:
            count = -count
            opp_count = -opp_count

        return -12.5 * count + 12.5 * opp_count

    def score_evaluation(self, board):
        from models.board import Board

        score = board.score()
        white = score[0]
        black = score[1]
        ret = 0
        if white == black:
            return ret
        if black > white:
            ret = 100 * black / (black + white)
        if white > black:
            ret = -100 * white / (white + black)

        if self.color == Board.WHITE:
            ret = -ret
        return ret

    def mobility_evaluation(self, board):
        from models.board import Board

        my_moves = len(board.valid_moves(self.color))
        opp_moves = len(board.valid_moves(self.opponent_color))
        ret = 0
        if my_moves == 0 or opp_moves == 0 or my_moves == opp_moves:
            return ret
        if my_moves > opp_moves:
            ret = 100 * my_moves / (my_moves + opp_moves)
        if opp_moves > my_moves:
            ret = -100 * opp_moves / (my_moves + opp_moves)

        if self.color == Board.WHITE:
            ret = -ret
        return ret

    def value_evaluation(self, board):
        value_map = [
            [ 20, -3,  11,   8,   8,  11, -3, 20],
            [ -3, -7,  -4,   1,   1,  -4, -7, -3],
            [ 11, -4,   2,   2,   2,   2, -4, 11],
            [  8,  1,   2,  -3,  -3,   2,  1,  8],
            [  8,  1,   2,  -3,  -3,   2,  1,  8],
            [ 11, -4,   2,   2,   2,   2, -4, 11],
            [ -3, -7,  -4,   1,   1,  -4, -7, -3],
            [ 20, -3,  11,   8,   8,  11, -3, 20],
        ]

        from models.board import Board

        score = 0
        for i in range(1, 9):
            for j in range(1, 9):
                value = value_map[i-1][j-1]
                if board.get_square_color(i, j) == self.color:
                    score += value
                elif board.get_square_color(i, j) == self.opponent_color:
                    score -= value
        return score

    def frontier_evaluation(self, board):
        from models.board import Board

        my = 0
        opp = 0
        close = [-1, 0, 1]
        for i in range(1, 8):
            for j in range(1, 8):
                if board.get_square_color(i, j) != Board.EMPTY:
                    for ii in range(0, 2):
                        for jj in range(0, 2):
                            x = close[ii] + i
                            y = close[jj] + j
                            if 1 <= x <= 8 and 1 <= y <= 8 and not (ii == 0 and jj == 0):
                                if board.get_square_color(x, y) == Board.BLACK:
                                    my += 1
                                if board.get_square_color(x, y) == Board.WHITE:
                                    opp += 1
        ret = 0
        if my == opp:
            return ret
        if my > opp:
            ret = 100 * my / (my + opp)
        if opp > my:
            ret = -100 * opp / (my + opp)

        if self.color == Board.WHITE:
            ret = -ret
        return ret

    def play(self, board):
        depth = self.depth if not self.game_is_ending(board) else 8
        value, move = self.evaluate(board, 1, depth, -float("inf"), float("inf"))

        return move

    def game_is_ending(self, board):
        score = board.score()
        return (64 - score[1] - score[0]) <= 10

    def endgame(self, board):
        return len(board.valid_moves(self.color)) == 0 and len(board.valid_moves(self.opponent_color)) == 0

    def evaluate_endgame_board(self, board):
        from models.board import Board

        score = board.score()
        if score[0] > score[1]:
            if self.color == Board.WHITE:
                return 100000 + score[0]
            else:
                return -100000
        elif score[1] > score[0]:
            if self.color == Board.BLACK:
                return 100000 + score[1]
            else:
                return -100000
        else:
            return -100000

    # Funcão que, dado um board, retorna o melhor movimento.
    # É recursiva.
    # board = board do jogo
    # nodeType = 1 sae for MAX, -1 se for MIN
    # depth = profundidade em que a busca ja foi
    def evaluate(self, board, node_type, depth, alpha, beta):
        # se ainda nao chegou no final
        endgame = self.endgame(board)
        if depth > 0 and not endgame:
            if node_type == 1:
                cur_value = alpha
                comp = max
                color = self.color
            else:
                cur_value = beta
                comp = min
                color = self.opponent_color
            cur_move = None
            # se não tenho movimento, eu passo a vez
            if len(board.valid_moves(color)) == 0:
                value, move = self.evaluate(board, -node_type, depth - 1, alpha, beta)
                return value, move
            # para cada movimento possivel
            for move in board.valid_moves(color):
                # faz um clone do board, em que o movimento foi feito
                child = board.get_clone()
                child.play(move, color)
                # pega o valor do no filho (ignorando o movimento)
                # na chamada recursiva, inverte o tipo e reduz a profundidade
                if node_type == 1:
                    value, ignore = self.evaluate(child, -node_type, depth - 1, cur_value, beta)
                else:
                    value, ignore = self.evaluate(child, -node_type, depth - 1, alpha, cur_value)

                if comp([cur_value, value]) == value:
                    cur_value = value
                    cur_move = move
                if node_type == 1:
                    if cur_value >= beta:
                        return cur_value, cur_move
                else:
                    if cur_value <= alpha:
                        return cur_value, cur_move
            # retorna o valor e o movimento que sao os melhores
            return cur_value, cur_move
        # se nao deve mais descer
        else:
            if endgame:
                return self.evaluate_endgame_board(board), None
            else:
                return self.evaluate_board(board), None
