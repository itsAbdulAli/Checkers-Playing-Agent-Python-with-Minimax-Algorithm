from copy import deepcopy
import MinimaxMoves

negInfinity = float('-inf')
posInfinity = float('inf')


# Minimax Algorithm

def minmax(board, treeDepthLimit, playerMax_White, alpha, beta, game):
    
    # Base Case - if Reached the child (specified treeDepthLimit of the tree or winning node)
    if treeDepthLimit == 0:
        return game.getsHeuristicForWhite(), board
    if board.return_WinStatus() is not None:
        return game.getsHeuristicForWhite(), board

    # The Max Player tends to maximize the score
    if playerMax_White:
        # Initially no Optimal Move and Max's Score equals to negative infinity

        OptimalMove = None
        maxScore = negInfinity

        # Obtaining all possible children for the given node
        Nodes = MinimaxMoves.MinimaxMoves()
        Nodes.set_possible_moves(board, (211, 211, 211))
        PossibleMoves = Nodes.return_possibleMoves()

        for move in PossibleMoves:
            # Getting the score for that node
            score,m = minmax(move, treeDepthLimit - 1, False, alpha, beta, game)

            # maximizing the score
            maxScore = max(maxScore, score)

            # alpha selects the max
            alpha = max(alpha, maxScore)

            if checkAlphaBetaPruning(alpha, beta):
                print("Branch Trimmed")
                break

            # incase score's same
            if maxScore == score:
                OptimalMove = move

        return maxScore, OptimalMove

    else:
        # The Min Player tends to minimize the score
        # Initially no Optimal Move and Min's Score equals to positive infinity
        OptimalMove = None
        minScore = posInfinity
        
        # Obtaining all possible children for the given node
        Nodes = MinimaxMoves.MinimaxMoves()
        Nodes.set_possible_moves(board, (255, 0, 0))
        PossibleMoves = Nodes.return_possibleMoves()

        for move in PossibleMoves:
            # Getting the score for that node
            score,m = minmax(move, treeDepthLimit - 1, True, alpha, beta, game)
            # minimizing the score
            minScore = min(minScore, score)
            #beta selects the min
            beta = min(beta, minScore)

            if checkAlphaBetaPruning(alpha, beta):
                print("Branch Trimmed")
                break
            #incase score's same
            if minScore == score:
                OptimalMove = move
        return minScore, OptimalMove


def checkAlphaBetaPruning(alpha, beta):
    if beta <= alpha:
        return True
    else:
        return False
