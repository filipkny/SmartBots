import pygame
from pygame.locals import *
from Defaults import *
import Player as p
import NN_class

class Game(object):
    def __init__(self,  VISUALS_SCORE = True,
                        VISUALS_PLAYER = True,
                        SOUND_EFFECTS = True,
                        VISUALS_MAP = True,
                        MANUAL_PLAY = False):


        self.VISUALS_SCORE = VISUALS_SCORE
        self.VISUALS_PLAYER = VISUALS_PLAYER
        self.SOUND_EFFECTS = SOUND_EFFECTS
        self.VISUALS_MAP = VISUALS_MAP
        self.MANUAL_PLAY = MANUAL_PLAY


    def main(self, nn_weights):
        # print("Im at main and these are my weights")
        print(nn_weights[0])

        self.FPSCLOCK,self.SCREEN = self.initPygame()
        self.SOUND, self.IMAGES = loadPygameDefaults(self.SOUND_EFFECTS)
        self.IMAGES, self.HITMASKS = loadImages()

        while True:
            player = p.Player()
            self.showWelcomeAnimation(player)
            crashInfo = self.mainGame(player, nn_weights)
            gameover, fitness = showGameOverScreen(crashInfo, player)
            if gameover:
                # print("Game is over with player dying at " + str(fitness) + "fitness")
                print(fitness)
                return fitness

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
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    # make first flap sound and return values for mainGame
                    if self.SOUND_EFFECTS:
                        self.SOUND['wing'].play()
                    return
        else:
            if player.keepPlaying:
                return

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
            self.pygameEventLoop(player)

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

    def mainGame(self,player, weights):
        loops = 0
        score = 0
        player.playerIndex = 0
        loopIter = 0

        upperPipes, lowerPipes = self.createNewPipes()

        pipeVelX = -4

        # Init neural network and respective weight vectors
        w1 = weights[:12]
        w2 = [weights[12:]]
        nn = Neural_net(w1, w2)

        while True:
            loops += 1
            player.jumping = False

            ind = self.getFirstPipeIndex(lowerPipes, player)

            # Compute distance in X between bird and first pipe ahead
            xdiff = lowerPipes[ind]['x'] - player.playerx  # TODO shouldnt this be total x distance?

            # Compute the distance in Y between bird and the middle of the first pipe crossing
            h_middle = lowerPipes[ind]['y'] + 210  # 210 because the gap is always 420
            ydiff = player.playery - 200 - h_middle / 5
            # print(abs(player.playery - (lowerPipes[ind]['y'] )))/100.
            # Create input vector for the neural network
            X = [xdiff, ydiff]
            ydiff = player.playery - lowerPipes[ind]['y'] + 50
            # print(player.playery - lowerPipes[ind]['y'] + 50)
            fitness = -abs(loops * pipeVelX) + abs(ydiff) / 5
            # print("X fitness coordinate is " + str(abs(loops * pipeVelX)) + " // Y fitness coordinate is " + str(abs(ydiff)))
            # print(fitness)
            # Forward propagation of NN to get the command for bird
            nn.forwardprop(X)
            y_nn = nn.get_y()

            if y_nn > 0.5:
                player.jumping = True

            if MANUAL_PLAY:
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
                    #  print("Im jumping at y: ", player.playery)
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
                    fitness -= 200
                    if SOUND_EFFECTS:
                        SOUNDS['point'].play()

            if score >= 1:
                print(score)
                print("Im trained")

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
                SCREEN.blit(IMAGES['background'], (0, 0))

                for uPipe, lPipe in zip(upperPipes, lowerPipes):
                    SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                    SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

                SCREEN.blit(IMAGES['base'], (player.basex, BASEY))

            showScore(score)

            visibleRot = player.checkRotationThreshold()
            playerSurface = pygame.transform.rotate(IMAGES['player'][player.playerIndex], visibleRot)
            if VISUALS_PLAYER:
                SCREEN.blit(playerSurface, (player.playerx, player.playery))

            pygame.display.update()
            FPSCLOCK.tick(FPS)

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
