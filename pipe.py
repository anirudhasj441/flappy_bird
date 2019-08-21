from  main import *
import pygame

def mainGame():
    score = 0
    playerX = int(SCREENWIDTH/5)
    playerY = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    basex=0
    basey=int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()) 

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipe = [
        {'x':SCREENWIDTH + 200,'y': newPipe1[0]['y']},
        {'x':SCREENWIDTH + 200 + (SCREENWIDTH/2),'y': newPipe2[1]['y']},
    ]

    lowerPipe = [
        {'x':SCREENWIDTH + 200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH + 200 + (SCREENWIDTH/2),'y':newPipe2[1]['y']},
    ]
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccY = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and evnt.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerY > 0:
                    playerVelY = playerFlapAccY
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerX , playerY , upperPipe , lowerPipe)

        if crashTest:
            return

        playerMidPos = playerX + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipe:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos< pipeMidPos + 4:
                score += 1
                print('your score is',score)
                GAME_SOUNDS['point'].play()

            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False
            
            playerHeight = GAME_SPRITES['player'].get_height()
            playerY = playerY + min(playerVelY , basey - playerY - playerHeight)


            for upperPipe , lowerPipe in zip(upperPipe,lowerPipe):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX
    
            if 0<upperPipe[0]['x']<5:
                newpipe = getRandomPipe()
                upperPipe.append(newpipe[0])
                lowerPipe.append(newpipe[1])
                


            if upperPipe[0]['x'] < - GAME_SPRITES['pipe'][0].get_width():
                upperPipe.pop(0)
                lowerPipe.pop(0)

            SCREEN.blit(GAME_SPRITES['background'],(0,0))
            for upperPipe , lowerPipe in zip(upperPipe,lowerPipe):
                SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
                SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))

            SCREEN.blit(GAME_SPRITES['base'],(basex, basey))
            SCREEN.blit(GAME_SPRITES['player'],(playerX, playerY))

            myDigits = [int(x) for x in list(str(score))]
            width = 0 
            xOffset = (SCREENWIDTH - width)/2

            for digit in myDigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit], (xOffset,SCREENHEIGHT* 0.12))
                xOffset = (SCREENWIDTH - width)/2
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)


def getRandomPipe():
    pipeHeight = int(GAME_SPRITES['pipe'][0].get_height())
    offset = int(SCREENHEIGHT/3)
    y2 = offset+random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipex = int(SCREENHEIGHT + 10)
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x':pipex,'y':-y1},
        {'x':pipex,'y':y2}
    ]
    return pipe

GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
mainGame()