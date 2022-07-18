from copy import deepcopy
import game
import checkersBoard
import pygame

class MinimaxMoves:
    def __init__(self):
        #here possible moves will contain actual boards (nodes of minimax tree) with possible moves
        self.possibleMoves=[]

    def set_possible_moves(self, board, color):
        #get all tokens of the player
        for token in board.return_allTokensofColor(color):
            #now for each token we have select it and get the available moves
            availableMovesforToken = board.getAvailableMovesForSelection(token)
            #get moves and jumped over nodes
            for move, jumped_over in availableMovesforToken.items():
                new_board = deepcopy(board)
                board_afterMoves = self.make_moveOnBoard(new_board, new_board.getToken(token.postion[0],token.postion[1]), move, jumped_over)
                self.possibleMoves.append(board_afterMoves)

        return self.possibleMoves

    def return_possibleMoves(self):
        return deepcopy(self.possibleMoves)
    
    def make_moveOnBoard(self, board, token, position, jumped_over):
        #take move
        board.moveToken((position[0], position[1]), token)
        #remove all the Tokens that were jumped over
        board = self.remove_JumpedOverTokens(board,jumped_over)
        return deepcopy(board)

    def remove_JumpedOverTokens(self,board,jumped_over):
        #if jumped over tokens then remove
        if jumped_over:
            for x in jumped_over:
                board.removeToken(x)
        return deepcopy(board)