from Defaults import *
import Player as p
from NN_class import Neural_net
import pygame
import time

class Game(object):
    def __init__(self,  VISUALS_SCORE = True,
                        VISUALS_PLAYER = True,
                        SOUND_EFFECTS = False,
                        VISUALS_MAP = True,
                        MANUAL_PLAY = True,
                        AI_PLAY = False,
                        plotDataFile = "PlotData.txt",
                        flappyDataFile = "FlappyData.txt"):


        self.VISUALS_SCORE = VISUALS_SCORE
        self.VISUALS_PLAYER = VISUALS_PLAYER
        self.SOUND_EFFECTS = SOUND_EFFECTS
        self.VISUALS_MAP = VISUALS_MAP
        self.MANUAL_PLAY = MANUAL_PLAY
        self.AI_PLAY = AI_PLAY
        self.RETURN_FIT = self.AI_PLAY
        self.runs = 0
        self.max_score = 0
        self.current_score = 0
        self.total_fitness = 0
        self.acc = []
        self.plotDataFile = plotDataFile
        self.flappyDataFile = flappyDataFile

    def main(self, nn_weights):
        self.FPSCLOCK,self.SCREEN = self.initPygame()
        self.SOUND, self.IMAGES = loadPygameDefaults(self.SOUND_EFFECTS)
        self.IMAGES, self.HITMASKS = loadImages()

        while True:
            player = p.Player()

            # Full game intro or jump straight into the action
            if self.MANUAL_PLAY:
                self.showWelcomeAnimation(player)
                crashInfo = self.mainGame(player, nn_weights)
                gameover, fitness = self.showGameOverScreen(crashInfo, player)
                print(fitness)
            else:
                gameover, fitness = self.mainGame(player, nn_weights)

            if gameover:
                self.total_fitness += fitness
                algorithm_fitness = abs(100000/(fitness+0.00001))

                # If new high score update and write
                if self.current_score > self.max_score:
                    self.max_score = self.current_score
                    self.writeNewHighScore(nn_weights)

                # Write this score
                self.writePlotData()
                if self.runs % 100 == 0:
                    self.printProgress(algorithm_fitness)

                return algorithm_fitness

    def printProgress(self,fit):
        print("Game number " + str(self.runs) +
              " is over with average fitness now of  " + str(fit) +
              " and maximum score of " + str(self.max_score))

    def writeNewHighScore(self, weights):
        with open(self.flappyDataFile, 'a') as file:
            output = "Run number: " + str(self.runs) + \
                     " with new high score: " + str(self.current_score) + \
                     "and weights "
            file.write(output)
            self.writeWeights(file, weights)
            file.write("\n")

    def stopSimulation(self,nn_weights):
        with open(self.flappyDataFile, 'a') as file:
            output = "Run number: " + str(self.runs) + \
                     " with new high score: " + str(self.current_score) + \
                     "and weights "

            self.writeWeights(file, nn_weights)

    def calculateAverage(self, array, fit):
        if len(array) < 10:
            array.append(fit)
        else:
            array.pop()
            array.append(fit)
        return sum(array)/10.

    def writePlotData(self):
        with open(self.plotDataFile, 'a') as file:
            output = str(self.runs) + "," +  str(self.current_score) +"\n"
            file.write(output)

    def writeWeights(self, file, weights):
        for weight in weights:
            file.write(str(weight)+",")

    # Initiate all pygame related functions
    def initPygame(self):
        pygame.init()  # del
        FPSCLOCK = pygame.time.Clock()  # del
        SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  # del
        pygame.display.set_caption('Flappy Bird')  # del
        return FPSCLOCK,SCREEN

    def pygameEventLoop(self, player):
        if self.MANUAL_PLAY:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    # make first flap sound and return values for mainGame
                    if self.SOUND_EFFECTS:
                        self.SOUND['wing'].play()
                    return True
        else:
            if player.keepPlaying:
                return True

    def showPlayerMapWelcome(self,player):
        if self.VISUALS_PLAYER:
            self.SCREEN.blit(IMAGES['player'][player.playerIndex],
                        (player.playerx, player.playery + player.playerShmVals['val']))

        if self.VISUALS_MAP:
            # draw sprites
            self.SCREEN.blit(IMAGES['background'], (0, 0))
            self.SCREEN.blit(IMAGES['message'], (IMAGES['messagex'], IMAGES['messagey']))
            self.SCREEN.blit(IMAGES['base'], (player.basex, BASEY))

    def showWelcomeAnimation(self,player):
        """Shows welcome screen animation of flappy bird"""

        # iterator used to change playerIndex after every 5th iteration
        loopIter = 0
        while True:
            # Event loop waiting for action
            exitStartScreen = self.pygameEventLoop(player)
            if exitStartScreen:
                return

            # Adjust playery, playerIndex, basex
            if (loopIter + 1) % 5 == 0:
                player.updatePlayerIndex()

            loopIter = (loopIter + 1) % 30


            player.updateBasex()
            player.playerShm()

            # Show map and player on canvas if enabled
            self.showPlayerMapWelcome(player)

            # Update canvas
            pygame.display.update()
            self.FPSCLOCK.tick(FPS)

    def createNewPipes(self):
        # get 2 new pipes to add to upperPipes lowerPipes list
        newPipe1 = self.getRandomPipe()
        newPipe2 = self.getRandomPipe()

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
        return upperPipes, lowerPipes

    def getFirstPipeIndex(self, lowerPipes, player):
        # Get index of first pipe ahead of bird
        for i in range(len(lowerPipes)):
            if lowerPipes[i]['x'] > player.playerx:
                ind = i
                return ind

    def pygameEventLoopAction(self, player):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                if player.playery > -2 * IMAGES['player'][0].get_height():
                    player.playerVelY = player.playerFlapAcc
                    player.playerFlapped = True
                    if self.SOUND_EFFECTS:
                        SOUNDS['wing'].play()

    def autoPlay(self,player):
        if player.jumping == True:
            if player.playery > -2 * IMAGES['player'][0].get_height():
                player.playerVelY = player.playerFlapAcc
                player.playerFlapped = True
                if self.SOUND_EFFECTS:
                    SOUNDS['wing'].play()

    def checkCrash(self, player, upperPipes, lowerPipes):
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
                uCollide = self.pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
                lCollide = self.pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

                if lCollide or uCollide:
                    return [True, False]

        return [False, False]

    def pixelCollision(self, rect1, rect2, hitmask1, hitmask2):
        """Checks if two objects collide and not just their rects"""
        rect = rect1.clip(rect2)

        if rect.width == 0 or rect.height == 0:
            return False

        x1, y1 = rect.x - rect1.x, rect.y - rect1.y
        x2, y2 = rect.x - rect2.x, rect.y - rect2.y

        for x in xrange(rect.width):
            for y in xrange(rect.height):
                if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                    return True
        return False

    def checkScore(self, player, score, fitness, upperPipes):
        playerMidPos = player.playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                fitness += 200
                if self.SOUND_EFFECTS:
                    SOUNDS['point'].play()
                return score
            else:
                return score

    def movePipesToLeft(self,upperPipes, lowerPipes, pipeVelX ):
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

    def addNewPipe(self, upperPipes, lowerPipes):
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = self.getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

    def removeFirstPipe(self, upperPipes, lowerPipes):
        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

    def drawSprites(self, upperPipes, lowerPipes, player):
        # draw sprites
        if self.VISUALS_MAP:
            self.SCREEN.blit(IMAGES['background'], (0, 0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                self.SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                self.SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            self.SCREEN.blit(IMAGES['base'], (player.basex, BASEY))

    def showScore(self, score):
        """displays score in center of screen"""
        scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0 # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += IMAGES['numbers'][digit].get_width()

        Xoffset = (SCREENWIDTH - totalWidth) / 2

        for digit in scoreDigits:
            if self.VISUALS_SCORE:
                self.SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
            Xoffset += IMAGES['numbers'][digit].get_width()

    def getRandomPipe(self):
        """returns a randomly generated pipe"""
        # y of gap between upper and lower pipe
        gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
        gapY += int(BASEY * 0.2)
        pipeHeight = IMAGES['pipe'][0].get_height()
        pipeX = SCREENWIDTH + 10

        return [
            {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
            {'x': pipeX, 'y': gapY + PIPEGAPSIZE},  # lower pipe
        ]


    def showGameOverScreen(self, crashInfo, player):
        score = crashInfo['score']
        player.playerx = SCREENWIDTH * 0.2
        player.playerAccY = 2
        player.playerVelRot = 7

        upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

        # play hit and die sounds
        if self.SOUND_EFFECTS:
            SOUNDS['hit'].play()
            if not crashInfo['groundCrash']:
                SOUNDS['die'].play()

        while True:
            if self.MANUAL_PLAY:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                        if player.playery + player.playerHeight >= BASEY - 1:
                            return True, crashInfo['fitness']
            else:
                if player.keepPlaying:
                    return True, crashInfo['fitness']

            player.shiftY()
            player.changeVelocity()
            player.rotateIfPipeCrash(crashInfo['groundCrash'])

            if self.VISUALS_MAP:
                # draw sprites
                self.SCREEN.blit(IMAGES['background'], (0, 0))

                for uPipe, lPipe in zip(upperPipes, lowerPipes):
                    self.SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                    self.SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

                self.SCREEN.blit(IMAGES['base'], (player.basex, BASEY))
            self.showScore(score)

            if self.VISUALS_PLAYER:
                playerSurface = pygame.transform.rotate(IMAGES['player'][1], player.playerRot)
                self.SCREEN.blit(playerSurface, (player.playerx, player.playery))

            self.FPSCLOCK.tick(FPS)
            pygame.display.update()

    def checkRotation(self, player):
        visibleRot = player.checkRotationThreshold()
        playerSurface = pygame.transform.rotate(IMAGES['player'][player.playerIndex], visibleRot)
        if self.VISUALS_PLAYER:
            self.SCREEN.blit(playerSurface, (player.playerx, player.playery))

    def mainGame(self,player, weights):
        #for 125 gap
        #weights = [-0.0594198806233,-0.0928772585862,-0.0634353826706,0.00430478583734,-0.0591339936073,0.0258900974363,0.0116359267351,0.0522146665544,-0.0431392905702,-0.0940026589862,0.0219763526729,-0.0566111423025,-0.0111163846122,0.0725690045081,-0.0251950711604,0.0107707205978,0.0151301321867,-0.0951135849001]

        self.runs += 1

        # Initalize needed constants
        loops = 0
        score = 0
        loopIter = 0
        pipeVelX = -4
        upperPipes, lowerPipes = self.createNewPipes()

        # Initiate neural network and respective weight vectors
        divider = 4
        if self.AI_PLAY:
            w1 = weights[:divider]
            w2 = [weights[divider:]]
            nn = Neural_net(w1, w2, 2, 2)

        fitness2 = 0
        gameon = True

        while gameon:
            # This is necessary for pygame not to crash
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            loops += 1                                      # Count loops to check distance
            player.jumping = False                          # Reset player jump action
            ind = self.getFirstPipeIndex(lowerPipes, player)# Get the index of the first pipe

            # Compute distance in X between bird and first pipe ahead,
            # in Y between bird and the middle of the first pipe crossing
            xdiff = lowerPipes[ind]['x'] - player.playerx
            middle = lowerPipes[ind]['y'] - PIPEGAPSIZE/2 - 20
            ydiff = player.playery - middle

            X = [xdiff, ydiff]

            # Calculate current fittness
            fitness = abs(loops * pipeVelX)# - abs(ydiff)
            # Forward propagation of NN to get the command for bird
            if self.AI_PLAY:
                nn.forwardprop(X)
                y_nn = nn.get_y()
                if y_nn > 0.5:
                    player.jumping = True

            # Jump or not jump
            if self.MANUAL_PLAY:
                self.pygameEventLoopAction(player)
            else:
                self.autoPlay(player)

            # Check if crash
            crashTest = self.checkCrash({'x': player.playerx, 'y': player.playery, 'index': player.playerIndex},
                                   upperPipes, lowerPipes)
            if self.MANUAL_PLAY:
                if crashTest[0]:
                    return {
                        'groundCrash': crashTest[1],
                        'upperPipes': upperPipes,
                        'lowerPipes': lowerPipes,
                        'score': score,
                        'fitness': fitness,
                    }
            else:
                if crashTest[0]:
                    return True, fitness


            # Check score
            score = self.checkScore(player, score, fitness, upperPipes)
            self.current_score = score
            if score>1000:
                self.stopSimulation(weights)
                return True,fitness

            # playerIndex basex change
            if (loopIter + 1) % 3 == 0:
                player.updatePlayerIndex()

            loopIter = (loopIter + 1) % 30

            # Update some positions
            player.liveUpdateBasex()
            player.rotatePlayer()
            player.movePlayer()
            player.playerHeight = IMAGES['player'][player.playerIndex].get_height()
            player.updateY()

            # move pipes, add new pipe when first pipe is about to touch left of screen
            self.movePipesToLeft(upperPipes, lowerPipes, pipeVelX)
            self.addNewPipe(upperPipes, lowerPipes)
            self.removeFirstPipe(upperPipes, lowerPipes)
            self.drawSprites(upperPipes, lowerPipes, player)
            self.showScore(score)
            self.checkRotation(player)

            # Makes hitspots black
            # pipeW = IMAGES['pipe'][0].get_width()
            # pipeH = IMAGES['pipe'][0].get_height()
            # uPipeRect = pygame.Rect(upperPipes[0]['x'], upperPipes[0]['y'], pipeW, pipeH)
            # lPipeRect = pygame.Rect(lowerPipes[0]['x'], lowerPipes[0]['y'], pipeW, pipeH)
            # playerRect = pygame.Rect(player.playerx,
            #                          player.playery,
            #                          IMAGES['player'][0].get_width(),
            #                          IMAGES['player'][0].get_height())
            # pygame.draw.rect(self.SCREEN, (0, 0, 0), playerRect, 0)
            # pygame.draw.rect(self.SCREEN,(0,0,0),uPipeRect,0)
            # pygame.draw.rect(self.SCREEN,(0,0,0),lPipeRect,0)

            pygame.display.update()
            self.FPSCLOCK.tick(FPS)

#
# game = Game(MANUAL_PLAY=False, AI_PLAY=True, plotDataFile="nan", flappyDataFile="nan")
# while True:
#     nn_weights = [0.0110004575674, -0.0465292480022, -0.0152230882772, 0.00718892342379, -0.0409277586902,
#                   0.028221629367]
#     game.main(nn_weights)