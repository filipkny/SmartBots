from itertools import cycle
from Defaults import *


class Player(object):
    def __init__(self):
        self.playerIndex = 0 # index of player to blit on screen
        self.playerIndexGen = cycle([0, 1, 2, 1])
        self.playerx = int(SCREENWIDTH * 0.2)
        self.playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)
        self.playerShmVals = {'val': 0, 'dir': 1}
        self.basex = 0
        self.baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()
        self.playerVelY = -5  # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY = 10  # max vel along Y, max descend speed
        self.playerMinVelY = -8  # min vel along Y, max ascend speed
        self.playerAccY = 1  # players downward accleration
        self.playerRot = 45  # player's rotation
        self.playerVelRot = 3  # angular speed
        self.playerRotThr = 20  # rotation threshold
        self.playerFlapAcc = -9 # players speed on flapping
        self.playerFlapped = False  # True when player flaps
        self.playerHeight = 0
        self.jumping = True
        self.keepPlaying = True

    def updatePlayerIndex(self):
        self.playerIndex = next(self.playerIndexGen)

    def playerShm(self):
        """oscillates the value of playerShm['val'] between 8 and -8"""
        if abs(self.playerShmVals['val']) == 8:
            self.playerShmVals['dir'] *= -1

        if self.playerShmVals['dir'] == 1:
            self.playerShmVals['val'] += 1
        else:
            self.playerShmVals['val'] -= 1

    def updateBasex(self):
        # amount by which base can maximum shift to left
        self.basex = -((-self.basex + 4) % self.baseShift)

    def liveUpdateBasex(self):
        self.basex = -((-self.basex + 100) % self.baseShift)

    def rotatePlayer(self):
        if self.playerRot > -90:
            self.playerRot -= self.playerVelRot

    def movePlayer(self):
        # player's movement
        if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
            self.playerVelY += self.playerAccY
        if self.playerFlapped:
            self.playerFlapped = False
            # more rotation to cover the threshold (calculated in visible rotation)
            self.playerRot = 45

    def updateY(self):
        self.playery += min(self.playerVelY, BASEY - self.playery - self.playerHeight)

    def checkRotationThreshold(self):
        # Player rotation has a threshold
        visibleRot = self.playerRotThr
        if self.playerRot <= self.playerRotThr:
            visibleRot = self.playerRot

        return visibleRot

    def shiftY(self):
        # player y shift
        if self.playery + self.playerHeight < BASEY - 1:
            self.playery += min(self.playerVelY, BASEY - self.playery - self.playerHeight)

    def changeVelocity(self):
        # player velocity change
        if self.playerVelY < 15:
            self.playerVelY += self.playerAccY

    def rotateIfPipeCrash(self, pipeCrash):
        if not pipeCrash:
            if self.playerRot > -90:
                self.playerRot -= self.playerVelRot
