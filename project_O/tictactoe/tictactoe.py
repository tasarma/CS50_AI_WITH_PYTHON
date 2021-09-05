"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = 0
    o = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x += 1
            elif board[i][j] == O:
                o += 1
            else:
                pass
    
    if x > o:
        return O
    else:
        return  X
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i,j))
    return moves
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy_board = copy.deepcopy(board)
    if copy_board[action[0]][action[1]] != EMPTY:
        raise f"{action} is not valid"
    
    copy_board[action[0]][action[1]] = player(copy_board)
    return copy_board
    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontally check
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O
            else:
                return None
    
    # Vertically check
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == X:
                return X
            elif board[0][i] == O:
                return O
            else:
                return None

    # Diagonally check
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
        else:
            return None
    
    # Diagonally check
    if board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] == X:
            return X
        elif board[2][0] == O:
            return O
        else:
            return None
    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X:
        return True
    elif winner(board) == O:
        return True

    for i in range(3):
        for j in range(3):
            if  board[i][j] == EMPTY:
                return False
    return True
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == O:
            return -1
        elif winner(board) == X:
            return 1
        else:
            return 0

    #raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            value, move = max_value(board)
            return move
        else:
            value, move = min_value(board)
            return move
    

    #raise NotImplementedError


def max_value(board):
    if terminal(board):
        return utility(board), None
    
    v = float('-inf')
    move = None
    for action in actions(board):
        value, act = min_value(result(board,action))
        if value > v:
            v = value
            move = action
            if v == 1:
                return v, move
    return v, move


def min_value(board):
    if terminal(board):
        return utility(board), None
    
    v = float('inf')
    move = None
    for action in actions(board):
        value, act = max_value(result(board,action))
        if value < v:
            v = value
            move = action
            if v == -1:
                return v, move
    return v, move
