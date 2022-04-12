import random
import sys #we'll use sys.exit
import pygame
from pygame.locals import *
import pygame.freetype

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = "gallery/sprites/nemi.png"
BACKGROUND = "gallery/sprites/background.png"
PIPE = "gallery/sprites/pipe.png"
    
    
def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES["player"].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES["message"].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            #if the user clicks on cros button, or  presses escape close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            #if the user presses space or upkey, start the game
            elif event.type== KEYDOWN and (event.key== K_SPACE or event.key== K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES["background"],(0, 0))
                SCREEN.blit(GAME_SPRITES["player"],(playerx, playery))
                SCREEN.blit(GAME_SPRITES["message"],(messagex, messagey))
                SCREEN.blit(GAME_SPRITES["base"],(basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    basex = 0
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES["player"].get_height())/2)

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes=[
        {'x':SCREENWIDTH+200, "y": newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+SCREENWIDTH/2, "y": newPipe2[0]['y']}
    ]
    lowerPipes=[
        {'x':SCREENWIDTH+200, "y": newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+SCREENWIDTH/2, "y": newPipe2[1]['y']}
    ]
    pipeVelx = -4
    playerVely = -9
    playerMaxVely = 10
    playerMinVely = -8
    playerAccY = 1

    playerFlapAccv = -8 #velocity(acc) while flapping
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE ):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery>0:   
                    playerVely= playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS["wing"].play()
        
        #below function returns true if player crashed 
        crashtest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashtest==True:
            return
        
        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<=playerMidPos<pipeMidPos+4:
                score+=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
        
        if playerVely<playerMaxVely and not playerFlapped:
            playerVely+=playerAccY

        if playerFlapped:
            playerFlapped=False
        
        playerHeight = GAME_SPRITES["player"].get_height()
        playery = playery + min(playerVely, GROUNDY-playery-playerHeight)

        #move pipes to the left
        for upperPipe,lowerPipe in  zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipeVelx
            lowerPipe['x']+=pipeVelx

        #add a new pipe when the first pipe is about to cross the left part of the screen
        if 0<upperPipes[0]['x']<5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        #if the  pipe is out of the screen remove it
        if upperPipes[0]['x']<-GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #let's blit our spirites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe,lowerPipe in  zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'],lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset+=GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes): 
    
    playerHeight=GAME_SPRITES["player"].get_height()
    playerWidth = GAME_SPRITES['player'].get_width()
    if playery>=GROUNDY-playerHeight:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        pipeWidth = GAME_SPRITES['pipe'][0].get_width()
        if (playery< pipeHeight + pipe['y']) and playerx>abs(pipe['x']-playerWidth) and playerx<abs (pipe["x"]+pipeWidth-playerWidth/3):
            GAME_SOUNDS['hit'].play()
            return True
    
    for pipe in lowerPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        pipeWidth = GAME_SPRITES['pipe'][0].get_width()
        if (playery+playerHeight-playerHeight/8>pipe['y']) and playerx>abs(pipe['x']-playerWidth) and playerx<abs (pipe["x"]+pipeWidth-playerWidth/3):
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    pipeheight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset +  random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeheight - y2 + offset
    
    pipe = [
        {'x':pipex, 'y' : -y1},
        {'x' : pipex, 'y' : y2}
    ]
    return pipe

def holdOn():
    while True:
        GAME_FONT = pygame.freetype.SysFont("arial", 18)
        # or just "render_to" the target surface.
        GAME_FONT.render_to(SCREEN, (40, 40), "PRESS ANY KEY TO CONTINUE!", (0, 0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == KEYDOWN:
                return


if __name__== '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Azaan')
    GAME_SPRITES['numbers']=(
        pygame.image.load("gallery/sprites/0.png").convert_alpha(),
        pygame.image.load("gallery/sprites/1.png").convert_alpha(), 
        pygame.image.load("gallery/sprites/2.png").convert_alpha(),
        pygame.image.load("gallery/sprites/3.png").convert_alpha(),
        pygame.image.load("gallery/sprites/4.png").convert_alpha(),
        pygame.image.load("gallery/sprites/5.png").convert_alpha(),
        pygame.image.load("gallery/sprites/6.png").convert_alpha(),
        pygame.image.load("gallery/sprites/7.png").convert_alpha(),
        pygame.image.load("gallery/sprites/8.png").convert_alpha(),
        pygame.image.load("gallery/sprites/9.png").convert_alpha()
    )
    GAME_SPRITES['message']=pygame.image.load("gallery/sprites/message1.png").convert_alpha()
    GAME_SPRITES['base']=pygame.image.load("gallery/sprites/base.png").convert_alpha()
    GAME_SPRITES['pipe']=(
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SOUNDS['die']=pygame.mixer.Sound("gallery/audio/die.wav")
    GAME_SOUNDS['hit']=pygame.mixer.Sound("gallery/audio/hit.wav")
    GAME_SOUNDS['point']=pygame.mixer.Sound("gallery/audio/point.wav")
    GAME_SOUNDS['wing']=pygame.mixer.Sound("gallery/audio/wing.wav")
    GAME_SOUNDS['swoosh']=pygame.mixer.Sound("gallery/audio/swoosh.wav")    
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
        holdOn()        



#Note to self: For alpha transparency, like in . png images, use the convert_alpha() method after loading so that the image has per pixel transparency. pygame may not always be built to support all image formats. At minimum it will support uncompressed BMP .




