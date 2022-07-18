import pygame
import checkersBoard


class game:
    def __init__(self, window):
        self.window = window
        self.gameBoard = checkersBoard.gameBoard()
        self.gameBoard.setTokens()
        self.selectedBox = None
        self.availableMovesforSelection = {}
        self.colorTurn = (255, 0, 0)
        self.gameBoard.turn="Red"


    def gameReset(self):
        self.gameBoard = checkersBoard.gameBoard()
        self.gameBoard.setTokens()
        self.selectedBox = None
        self.availableMovesforSelection = {}
        self.colorTurn = (255, 0, 0)
        self.gameBoard.turn = "Red"

    def nextTurn(self):
        if self.colorTurn == (255, 0, 0):
            self.colorTurn = (211, 211, 211)
            self.gameBoard.turn = "White"
        elif self.colorTurn == (211, 211, 211):
            self.colorTurn = (255, 0, 0)
            self.gameBoard.turn = "Red"

    def updateDisplay(self):
        self.gameBoard.drawBoard(self.window)
        self.gameBoard.drawTokens(self.window)
        self.gameBoard.draw_availableMoves(self.availableMovesforSelection, self.window)
        pygame.display.update()

    def selectBox(self, r, c):
        if self.selectedBox is not None:
            # already a selected token
            # move that token to new position
            check = self.moveToken(r, c)
            if check == False:
                # not a valid move
                # try selecting again
                self.selectedBox = None
                self.availableMovesforSelection = {}
                self.selectBox(r, c)
            else:
                self.selectedBox = None
                self.availableMovesforSelection = {}
                self.nextTurn()


        elif self.selectedBox is None:
            # select a new token here
            selectedToken = self.gameBoard.getToken(r, c)
            if selectedToken is not None:
                if selectedToken.color == self.colorTurn:
                    self.selectedBox = selectedToken
                    self.availableMovesforSelection = self.gameBoard.getAvailableMovesForSelection(selectedToken)
                    return True
                else:
                    self.selectedBox = None
                    self.availableMovesforSelection = {}

        return False

    def moveToken(self, r, c):
        emptyToken = self.gameBoard.getToken(r, c)
        if self.selectedBox is not None and emptyToken is None and (r, c) in self.availableMovesforSelection:
            self.gameBoard.moveToken((r, c), self.selectedBox)
            tokensToRemove = self.availableMovesforSelection[(r, c)]
            self.removeTokens(tokensToRemove)
            return True
        else:
            return False

    def removeTokens(self,tokensToRemove):
        if tokensToRemove:
            for x in tokensToRemove:
                self.gameBoard.removeToken(x)


    def getboard(self):
        return self.gameBoard

    def autoMove(self, board):
        if board is not None:
            self.nextTurn()
            self.gameBoard = board


    def return_WinStatus(self):
        return self.gameBoard.return_WinStatus()

    def save_game(self):
        self.gameBoard.save_game()

    def load_game(self):
        self.gameBoard.load_game()
        if self.gameBoard.turn=="Red":
            self.colorTurn=(255,0,0)
        else:
            self.colorTurn=(211,211,211)

    def getsHeuristicForWhite(self):
        return self.gameBoard.getsHeuristicForWhite()

    def getsHeuristicForRed(self):
        return self.gameBoard.getsHeuristicForRed()