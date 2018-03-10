import pygame
import sys
FPS = 20000
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