import pygame
import game
import checkersBoard
import MinmaxAlgorithm
pygame.init()

def game_reset(checkersGame):
    checkersGame.gameReset()
    return checkersGame

#Game Loop
def gameLoop(window):
    checkersGame=game.game(window)

    finish = False
    gameClock = pygame.time.Clock()
    while(not finish):

        gameClock.tick(60)
        font = pygame.font.Font('arialbd.ttf', 32)
        fontBig = pygame.font.Font('arialbd.ttf', 42)
        text1 = fontBig.render('CHECKERS', True, (255,255,255), (21,0,10))
        text2 = font.render('   WHITE TOKENS: '+ str(checkersGame.gameBoard.noOfWhiteTokens)+'   ', True, (255, 255, 255), (21, 0, 10))
        text3 = font.render('   RED TOKENS: '+ str(checkersGame.gameBoard.noOfRedTokens)+'   ', True, (255, 255, 255), (21, 0, 10))
        Turn="WHITE"
        if(checkersGame.colorTurn==(255,0,0)):
            Turn="RED"
        text4 = font.render('   PLAYER TURN: ' + Turn +'   ', True, (255, 255, 255),(21, 0, 10))

        textRect = text1.get_rect()
        textRect.center = (1000, 100)
        window.blit(text1, textRect)
        textRect = text2.get_rect()
        textRect.center = (1000, 200)
        window.blit(text2, textRect)
        textRect = text3.get_rect()
        textRect.center = (1000, 260)
        window.blit(text3, textRect)
        textRect = text4.get_rect()
        textRect.center = (1000, 320)
        window.blit(text4, textRect)
        text7 = font.render("TO SAVE PRESS (S)", True, (255, 255, 255), (21, 0, 10))
        textRect = text7.get_rect()
        textRect.center = (1000, 500)
        window.blit(text7, textRect)
        text8 = font.render("TO LOAD PRESS (L)", True, (255, 255, 255), (21, 0, 10))
        textRect = text8.get_rect()
        textRect.center = (1000, 560)
        window.blit(text8, textRect)


        if checkersGame.return_WinStatus() is not None:
            text5 = font.render(checkersGame.return_WinStatus(), True, (255, 255, 255), (21, 0, 10))
            textRect = text5.get_rect()
            textRect.center = (1000, 380)
            window.blit(text5, textRect)
            text6 = font.render("PRESS (R) TO RESET", True, (255, 255, 255), (21, 0, 10))
            textRect = text6.get_rect()
            textRect.center = (1000, 440)
            window.blit(text6, textRect)
            checkersGame.updateDisplay()
            check = True
            while check:
                for newEvents in pygame.event.get():
                    if newEvents.type == pygame.QUIT:
                        finish = True
                    if newEvents.type == pygame.KEYDOWN:
                        if newEvents.key == pygame.K_r:
                            game_reset(checkersGame)
                            window.fill((21, 0, 10))
                            checkersGame.updateDisplay()
                            check = False

        if checkersGame.colorTurn == (211, 211, 211):
            value, newBoard = MinmaxAlgorithm.minmax(checkersGame.getboard(), 3, (211, 211, 211),float('-inf'),float('inf'), checkersGame)
            checkersGame.autoMove(newBoard)
        #Event Management
        for newEvents in pygame.event.get():
            if newEvents.type == pygame.QUIT:
                finish = True
            if newEvents.type == pygame.MOUSEBUTTONDOWN:
                selectedTokenPos = getPositionfromMouseCordinates(pygame.mouse.get_pos())
                if (selectedTokenPos!=None):
                    checkersGame.selectBox(selectedTokenPos[0],selectedTokenPos[1])
            if newEvents.type == pygame.KEYDOWN:
                if newEvents.key == pygame.K_s:
                    font3 = pygame.font.Font('arialbd.ttf', 20)
                    text8 = font3.render("ENTER FILENAME IN CONSOLE", True, (255, 255, 255), (21, 0, 10))
                    textRect = text8.get_rect()
                    textRect.center = (1000, 700)
                    window.blit(text8, textRect)
                    checkersGame.updateDisplay()
                    checkersGame.save_game()
                    text8 = font3.render("                                                       ", True, (255, 255, 255), (21, 0, 10))
                    textRect = text8.get_rect()
                    textRect.center = (1000, 700)
                    window.blit(text8, textRect)
                    checkersGame.updateDisplay()
            if newEvents.type == pygame.KEYDOWN:
                if newEvents.key == pygame.K_l:
                    font3 = pygame.font.Font('arialbd.ttf', 20)
                    text8 = font3.render("ENTER FILENAME IN CONSOLE", True, (255, 255, 255), (21, 0, 10))
                    textRect = text8.get_rect()
                    textRect.center = (1000, 700)
                    window.blit(text8, textRect)
                    checkersGame.updateDisplay()
                    checkersGame.load_game()
                    text8 = font3.render("                                                       ", True, (255, 255, 255), (21, 0, 10))
                    textRect = text8.get_rect()
                    textRect.center = (1000, 700)
                    window.blit(text8, textRect)
                    checkersGame.updateDisplay()


        checkersGame.updateDisplay()


    pygame.quit()

def getPositionfromMouseCordinates(position):
    if position[0]<=800 and position[1]<=800:
        return (position[1]//100 , position[0]//100)
    else:
        return None

windowSize = (1200,800)
window = pygame.display.set_mode(windowSize)
window.fill((21, 0, 10))
pygame.display.set_caption('AI Project: 19L-0917 19L-0949')
gameLoop(window)



