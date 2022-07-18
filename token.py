import pygame

class token:
    def __init__(self,position,color):
        self.postion = position
        self.color = color
        self.isKing = False

    def return_MovementDirection(self):
        Color_Red = (255, 0, 0)
        Color_White = (211, 211, 211)
        if self.color == Color_White:
            return -1
        elif self.color == Color_Red:
            return 1

    def drawToken(self, window):
        pygame.draw.circle(window, self.color, self.return_GraphicsCoordinates(), 30)
        if self.isKing == True:
            pygame.draw.circle(window, (255, 255, 0), self.return_GraphicsCoordinates(), 15)

    def setKing(self):
        self.isKing = True


    def return_GraphicsCoordinates(self):
        y = 100 * self.postion[0] + 50
        x = 100 * self.postion[1] + 50
        return (x,y)

    def moveToken(self,position):
        self.postion=position