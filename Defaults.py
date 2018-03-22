import pygame
import sys
import random

FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512

# amount by which base can maximum shift to left
PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap2.png',
        'assets/sprites/redbird-midflap2.png',
        'assets/sprites/redbird-downflap2.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        'assets/sprites/bluebird-upflap2.png',
        'assets/sprites/bluebird-midflap2.png',
        'assets/sprites/bluebird-downflap2.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap2.png',
        'assets/sprites/yellowbird-midflap2.png',
        'assets/sprites/yellowbird-downflap2.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/background-day2.png',
    'assets/sprites/background-night2.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green2.png',
    'assets/sprites/pipe-red2.png',
)


def loadPygameDefaults(SOUND_EFFECTS):
   #  numbers sprites for score display
   IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/02.png').convert_alpha(),
        pygame.image.load('assets/sprites/12.png').convert_alpha(),
        pygame.image.load('assets/sprites/22.png').convert_alpha(),
        pygame.image.load('assets/sprites/32.png').convert_alpha(),
        pygame.image.load('assets/sprites/42.png').convert_alpha(),
        pygame.image.load('assets/sprites/52.png').convert_alpha(),
        pygame.image.load('assets/sprites/62.png').convert_alpha(),
        pygame.image.load('assets/sprites/72.png').convert_alpha(),
        pygame.image.load('assets/sprites/82.png').convert_alpha(),
        pygame.image.load('assets/sprites/92.png').convert_alpha()
    )

#  game over sprite
   IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover2.png').convert_alpha()
    #  message sprite for welcome screen
   IMAGES['message'] = pygame.image.load('assets/sprites/message2.png').convert_alpha()
    #  base (ground) sprite
   IMAGES['base'] = pygame.image.load('assets/sprites/base2.png').convert_alpha()
   IMAGES['messagex'] = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
   IMAGES['messagey'] = int(SCREENHEIGHT * 0.12)
   if SOUND_EFFECTS:
        # sounds
     if 'win' in sys.platform:
        soundExt = '.wav'
     else:
        soundExt = '.ogg'

     SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die' + soundExt)
     SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit' + soundExt)
     SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point' + soundExt)
     SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
     SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing' + soundExt)


     return SOUNDS,IMAGES
   else:
     return "empty",IMAGES

def loadImages():
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

    return IMAGES,HITMASKS

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask