import pygame
from token import token


class gameBoard:
    def __init__(self):
        self.noOfRedTokens = 12
        self.noOfWhiteTokens = 12
        self.noOfRedKings = 0
        self.noOfWhiteKings = 0
        self.turn = "Red"
        self.map = []

    def drawBoard(self, window):
        Color_Black = (0, 0, 0)
        Color_White = (255, 255, 255)
        Selected_color = Color_Black
        for i in range(0, 8):
            for j in range(0, 8):
                pygame.draw.rect(window, Selected_color, (i * 100, j * 100, 100, 100))
                if (Selected_color == Color_Black):
                    Selected_color = Color_White
                else:
                    Selected_color = Color_Black

            if (Selected_color == Color_Black):
                Selected_color = Color_White
            else:
                Selected_color = Color_Black

    def getToken(self, i, j):
        if self.map[i][j] is not None:
            return self.map[i][j]
        else:
            return None

    def getsHeuristicForWhite(self):
        weightonKing = 0.5
        factorForTokens = self.noOfWhiteTokens - self.noOfRedTokens
        factorForKings = self.noOfWhiteKings * weightonKing - self.noOfRedKings *(- weightonKing)
        return factorForTokens + factorForKings

    def getsHeuristicForRed(self):
        weightonKing = 0.5
        factorForTokens = self.noOfRedTokens - self.noOfWhiteTokens
        factorForKings = self.noOfRedKings * weightonKing - self.noOfWhiteKings *(- weightonKing)
        return factorForTokens + factorForKings

    def return_allTokensofColor(self, color):
        tokens_List = []
        for i in range (0,8):
            for j in range (0,8):
                if self.map[i][j] is not None:
                    if self.map[i][j].color == color:
                        tokens_List.append(self.map[i][j])
        return tokens_List

    def setTokens(self):
        Color_Red = (255, 0, 0)
        Color_White = (211, 211, 211)
        drawBool = False

        for i in range(0, 8):
            token_list = []
            for j in range(0, 8):
                if (i < 3 and drawBool == True):
                    token_list.append(token((i, j), Color_White))
                    drawBool = False
                elif (i > 4 and drawBool == True):
                    token_list.append(token((i, j), Color_Red))
                    drawBool = False
                else:
                    token_list.append(None)
                    drawBool = True
            self.map.append(token_list)
            if (i < 3 or i > 4):
                if (drawBool == True):
                    drawBool = False
                else:
                    drawBool = True

    def moveToken(self, newPosition, token):
        if (token.color == (255, 0, 0) and newPosition[0] == 0):
            if token.isKing == False:
                token.setKing()
                self.noOfRedKings = self.noOfRedKings + 1
        elif (token.color == (211, 211, 211) and newPosition[0] == 7):
            if token.isKing == False:
                token.setKing()
                self.noOfWhiteKings = self.noOfWhiteKings + 1
        self.map[token.postion[0]][token.postion[1]], self.map[newPosition[0]][newPosition[1]] = self.map[newPosition[0]][newPosition[1]], self.map[token.postion[0]][token.postion[1]]
        token.moveToken(newPosition)

    def removeToken(self, token):
        if token != None:
            self.map[token.postion[0]][token.postion[1]] = None
            if token.color == (255, 0, 0):
                self.noOfRedTokens = self.noOfRedTokens - 1
            elif token.color == (211, 211, 211):
                self.noOfWhiteTokens = self.noOfWhiteTokens - 1

    def drawTokens(self, window):

        for i in range(0, 8):
            for j in range(0, 8):
                if self.map[i][j] is not None:
                    self.map[i][j].drawToken(window)

    def draw_availableMoves(self, availableMoves, window):
        for x in availableMoves:
            (r, c) = x
            pygame.draw.circle(window, (255, 192, 203), ((c * 100 + 50), (r * 100 + 50)), 15)

    def printMap(self):

        for i in range(0, 8):
            for j in range(0, 8):
                if self.map[i][j] is not None:
                    print(self.map[i][j].color)
                else:
                    print("x")

    def getAvailableMovesForSelection(self, selectedToken):
        #Dict to store moves with respect to their jumped over trace
        availableMoves = {}


        nextColforleftMoves = selectedToken.postion[1] - 1
        nextColforrightMoves = selectedToken.postion[1] + 1
        rowofSelectiedToken = selectedToken.postion[0]
        
        ForwardDirection=1
        BackwardDirection =-1
        
        #King can move top left, top right, bottom left, bottom right diagonal blocks
        if selectedToken.isKing == True:
            availableMoves.update(self.move_Left(BackwardDirection, rowofSelectiedToken - 1, max(rowofSelectiedToken - 3, -1), nextColforleftMoves, selectedToken.color))
            availableMoves.update(self.move_Right(BackwardDirection, rowofSelectiedToken - 1, max(rowofSelectiedToken - 3, -1), nextColforrightMoves,selectedToken.color))
            availableMoves.update(self.move_Left(ForwardDirection, rowofSelectiedToken + 1, min(rowofSelectiedToken + 3, 8), nextColforleftMoves, selectedToken.color))
            availableMoves.update(self.move_Right(ForwardDirection, rowofSelectiedToken + 1, min(rowofSelectiedToken + 3, 8), nextColforrightMoves, selectedToken.color))

        #Red can move bottom left, bottom right diagonal blocks
        if selectedToken.color == (255, 0, 0):
            availableMoves.update(self.move_Left(BackwardDirection, rowofSelectiedToken - 1, max(rowofSelectiedToken - 3, -1), nextColforleftMoves, selectedToken.color))
            availableMoves.update(self.move_Right(BackwardDirection, rowofSelectiedToken - 1, max(rowofSelectiedToken - 3, -1), nextColforrightMoves, selectedToken.color))

        #White can move top left, top right diagonal blocks
        if selectedToken.color == (211, 211, 211):
            availableMoves.update(self.move_Left(ForwardDirection, rowofSelectiedToken + 1, min(rowofSelectiedToken + 3, 8), nextColforleftMoves, selectedToken.color))
            availableMoves.update(self.move_Right(ForwardDirection, rowofSelectiedToken + 1, min(rowofSelectiedToken + 3, 8), nextColforrightMoves, selectedToken.color))

        return availableMoves

    def move_Left(self, direction, inital_row, final_row, next_box_col, color, jumped_over=[]):

        previousJumpedOver = []
        availableMoves = {}

        for row in range(inital_row, final_row, direction):
            #Exploring out of bound blocks
            if next_box_col < 0:
                break
            else:
                Token = self.getToken(row, next_box_col)

                if Token == None: #Empty Block
                    if jumped_over and not previousJumpedOver:
                        #breaking condition: if empty block but already played an move by jumping over enemy token
                        break
                    elif jumped_over:
                        #if jumped over enemy block then add it to moves
                        availableMoves[(row, next_box_col)] = previousJumpedOver + jumped_over
                    elif not previousJumpedOver:
                        #breaking condition: if already played a move then add it to moves
                        availableMoves[(row, next_box_col)] = previousJumpedOver
                        break
                    else:
                        availableMoves[(row, next_box_col)] = previousJumpedOver

                    #if jumped over enemy block then we can check for next enemy block in the track
                    if previousJumpedOver:
                        if direction == 1:
                            r = min(row + 3, 8)
                        elif direction == -1:
                            r = max(row - 3, 0)

                        availableMoves.update(self.move_Left(direction, (row + direction), r, next_box_col - 1, color, previousJumpedOver))
                        availableMoves.update( self.move_Right(direction, (row + direction), r, next_box_col + 1, color, previousJumpedOver))
                        break

                #if same color then we cannot move ahead
                elif Token.color == color:
                    break

                #if enemy color then add it to jumped over
                elif Token.color != color:
                    previousJumpedOver = [Token]

                #update col position for next move towards left
                next_box_col = next_box_col - 1

        return availableMoves

    def move_Right(self, direction, inital_row, final_row, next_box_col, color, jumped_over=[]):

        previousJumpedOver = []
        availableMoves = {}

        for row in range(inital_row, final_row, direction):
            #Exploring out of bound blocks
            if next_box_col >= 8:
                break
            else:
                Token = self.getToken(row, next_box_col)

                if Token == None:
                    if jumped_over and not previousJumpedOver:
                        # breaking condition: if empty block but already played an move by jumping over enemy token
                        break
                    elif jumped_over:
                        #if jumped over enemy block then add it to moves
                        availableMoves[(row, next_box_col)] = previousJumpedOver + jumped_over
                    elif not previousJumpedOver:
                        # breaking condition: if already played a move then add it to moves
                        availableMoves[(row, next_box_col)] = previousJumpedOver
                        break
                    else:
                        availableMoves[(row, next_box_col)] = previousJumpedOver

                    # if jumped over enemy block then we can check for next enemy block in the track
                    if previousJumpedOver:
                        if direction == 1:
                            r = min(row + 3, 8)
                        elif direction == -1:
                            r = max(row - 3, 0)

                        availableMoves.update(self.move_Left(direction, (row + direction), r, next_box_col - 1, color, previousJumpedOver))
                        availableMoves.update(self.move_Right(direction, (row + direction), r, next_box_col + 1, color, previousJumpedOver))
                        break

                # if same color then we cannot move ahead
                elif Token.color == color:
                    break

                # if enemy color then add it to jumped over
                elif Token.color != color:
                    previousJumpedOver = [Token]

                # update col position for next move towards left
                next_box_col = next_box_col + 1
        return availableMoves

    def return_WinStatus(self):
        if self.noOfRedTokens == 0:
            return ("WHITE WINS")
        elif self.noOfWhiteTokens == 0:
            return ("RED WINS")
        else:
            return None

    def save_game(self):
        print("Enter Filename:")
        filename = str(input())+(".txt")
        f = open(filename, "w")
        f.write(str(self.noOfRedTokens))
        f.write(" ")
        f.write(str(self.noOfWhiteTokens))
        f.write(" ")
        f.write(str(self.noOfRedKings))
        f.write(" ")
        f.write(str(self.noOfWhiteKings))
        f.write(" ")
        f.write(self.turn)
        f.write(" ")

        for x in range (0,8):
            for y in range (0,8):
                if self.map[x][y] is None:
                    f.write("skip")
                    f.write(" ")
                else:
                    f.write(str(self.map[x][y].postion[0]))
                    f.write(" ")
                    f.write(str(self.map[x][y].postion[1]))
                    f.write(" ")
                    f.write(str(self.map[x][y].color[0]))
                    f.write(" ")
                    f.write(str(self.map[x][y].color[1]))
                    f.write(" ")
                    f.write(str(self.map[x][y].color[2]))
                    f.write(" ")
                    f.write(str(self.map[x][y].isKing))
                    f.write(" ")


        f.close()

    def load_game(self):
        print("Enter Filename:")
        filename = str(input())+(".txt")
        f = open(filename, "r")
        content=f.read()
        content = content.split()
        print (content)
        self.noOfRedTokens=int(content[0])
        self.noOfWhiteTokens =int( content[1])
        self.noOfRedKings = int(content[2])
        self.noOfWhiteKings = int(content[3])
        self.turn = content[4]

        index = 5

        for x in range (0,8):
            for y in range (0,8):
                if content[index] == "skip":
                    self.map[x][y]=None
                    index=index+1
                else:
                    pos_0 = int(content[index])
                    index += 1
                    pos_1 = int(content[index])
                    index += 1
                    col_0 = int(content[index])
                    index += 1
                    col_1 = int(content[index])
                    index += 1
                    col_2 = int(content[index])
                    index += 1
                    isKing = content[index]
                    index += 1

                    self.map[x][y]=token((pos_0, pos_1), (col_0,col_1,col_2))
                    if isKing == "True":
                        self.map[x][y].isKing=True


        f.close()


