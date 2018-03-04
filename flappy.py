import random
import sys

import pygame
from pygame.locals import *
from Defaults import *
import Player as p
from NN_class import Neural_net
import numpy as np

try:
    xrange
except NameError:
    xrange = range

VISUALS_SCORE = True
VISUALS_PLAYER = True
SOUND_EFFECTS = False
VISUALS_MAP = True
MANUAL_PLAY = False

GLOBAL_FIT = 0

def main(NN_weights):
#    print("Im at main and these are my weights")
   # print(NN_weights)
    global SCREEN, FPSCLOCK
    #pygame.init() #del
    FPSCLOCK = pygame.time.Clock()#del
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))#del
    #pygame.display.set_caption('Flappy Bird')#del

    SOUND, IMAGES = loadPygameDefaults(SOUND_EFFECTS)

    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # select random player sprites
        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )

        # select random pipe sprites
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.rotate(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )

        # hismask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # hitmask for player
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )


        player = p.Player()
        movementInfo = showWelcomeAnimation(player)
        crashInfo = mainGame(player, NN_weights)
        gameover,fitness = showGameOverScreen(crashInfo, player)
        if gameover:
            print("Game is over with fitness")
            print(fitness)
            return fitness


def showWelcomeAnimation(player):
    """Shows welcome screen animation of flappy bird"""

    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    #messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    while True:
        if MANUAL_PLAY:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    # make first flap sound and return values for mainGame
                    if SOUND_EFFECTS:
                        SOUNDS['wing'].play()
                    return
        else:
            if player.keepPlaying:
                return

        # adjust playery, playerIndex, basex
        if (loopIter + 1) % 5 == 0:
           player.updatePlayerIndex()

        loopIter = (loopIter + 1) % 30
        player.updateBasex()

        # Not sure what this does?
        player.playerShm()

        if VISUALS_PLAYER:
            SCREEN.blit(IMAGES['player'][player.playerIndex],
                        (player.playerx, player.playery + player.playerShmVals['val']))
        if VISUALS_MAP:
            # draw sprites
            SCREEN.blit(IMAGES['background'], (0,0))
            SCREEN.blit(IMAGES['message'], (messagex, messagey))
            SCREEN.blit(IMAGES['base'], (player.basex, BASEY))

        #pygame.display.update()
        #FPSCLOCK.tick(FPS)


def mainGame(player, weights):
    loops = 0

    score = 0
    player.playerIndex = 0
    loopIter = 0

    player.playerx = int(SCREENWIDTH * 0.2)

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]


    pipeVelX = -4

    w1 = weights[:12]
    w2 = [weights[12:]]
    nn = Neural_net(w1, w2)

    while True:
        #print("im playing")
        loops = loops + 1

        #Get index of first pipe ahead of bird
        for i in range(len(lowerPipes)):
            if lowerPipes[i]['x'] > player.playerx:
                ind = i
                break
            
        #Compute distance in X between bird and first pipe ahead
        xdiff = lowerPipes[i]['x'] - player.playerx
        
        #Compute the distance in Y between bird and the middle of the first pipe crossing
        h_middle = lowerPipes[i]['y'] + 210 #210 because the gap is always 420
        ydiff = player.playery - h_middle
        
        #Create input vector for the neural network
        X = [xdiff,ydiff]

        fitness = loops * pipeVelX + abs(ydiff)
        #Forward propagation of NN to get the command for bird
        nn.forwardprop(X)
        y_nn = nn.get_y()
        
        if y_nn > 0.5:
           player.jumping = True
        

        if MANUAL_PLAY:
            #player.jumping = neuralNetwork.getAction() THIS IS WHERE API DECIDES WHAT TO DO
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):

                    if player.playery > -2 * IMAGES['player'][0].get_height():
                        player.playerVelY = player.playerFlapAcc
                        player.playerFlapped = True
                        if SOUND_EFFECTS:
                            SOUNDS['wing'].play()

        else:
            if player.jumping == True:
                #print("Im jumping at ")
               # print(fitness)
                if player.playery > -2 * IMAGES['player'][0].get_height():
                    player.playerVelY = player.playerFlapAcc
                    player.playerFlapped = True
                    if SOUND_EFFECTS:
                        SOUNDS['wing'].play()

        # check for crash here
        crashTest = checkCrash({'x': player.playerx, 'y': player.playery, 'index': player.playerIndex},
                               upperPipes, lowerPipes)
        if crashTest[0]:
            return {
                'groundCrash': crashTest[1],
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'fitness': fitness,
            }

        # check for score
        playerMidPos = player.playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                if SOUND_EFFECTS:
                    SOUNDS['point'].play()


        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            player.updatePlayerIndex()

        loopIter = (loopIter + 1) % 30

        player.liveUpdateBasex()
        player.rotatePlayer()
        player.movePlayer()

        player.playerHeight = IMAGES['player'][player.playerIndex].get_height()
        player.updateY()

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # draw sprites
        if VISUALS_MAP:
            SCREEN.blit(IMAGES['background'], (0,0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            SCREEN.blit(IMAGES['base'], (player.basex, BASEY))

       # showScore(score)

        visibleRot = player.checkRotationThreshold()
        playerSurface = pygame.transform.rotate(IMAGES['player'][player.playerIndex], visibleRot)
        if VISUALS_PLAYER:
            SCREEN.blit(playerSurface, (player.playerx, player.playery))

        # pygame.display.update()
        # FPSCLOCK.tick(FPS)

def showGameOverScreen(crashInfo, player):

    score = crashInfo['score']
    player.playerx = SCREENWIDTH * 0.2
    player.playerAccY = 2
    player.playerVelRot = 7

    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    # play hit and die sounds
    if SOUND_EFFECTS:
        SOUNDS['hit'].play()
        if not crashInfo['groundCrash']:
            SOUNDS['die'].play()

    while True:
        if MANUAL_PLAY:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if player.playery + player.playerHeight >= BASEY - 1:
                        return True, crashInfo['fitness']
        else:
            if player.keepPlaying:
                return True, crashInfo['fitness']

        player.shiftY()
        player.changeVelocity()
        player.rotateIfPipeCrash(crashInfo['groundCrash'])

        if VISUALS_MAP:
            # draw sprites
            SCREEN.blit(IMAGES['background'], (0,0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            SCREEN.blit(IMAGES['base'], (player.basex, BASEY))
        showScore(score)

        if VISUALS_PLAYER:
            playerSurface = pygame.transform.rotate(IMAGES['player'][1], player.playerRot)
            SCREEN.blit(playerSurface, (player.playerx,player.playery))

        FPSCLOCK.tick(FPS)
        pygame.display.update()


# TODO initialize seed here so that we can keep track of it
def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        if VISUALS_SCORE:
            SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

if __name__ == '__main__':

    keepPlaying = True
    while keepPlaying:
        GLOBAL_FIT, keepPlaying = main("empty")
        #print(GLOBAL_FIT)
