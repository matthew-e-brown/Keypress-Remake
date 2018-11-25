##Import Libraries
import pygame, sys, time, random, os

#Import my own files
import gfx
from colors import *

##Initialize
pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.init()

PATH = os.path.dirname(os.path.abspath(__file__))

WIDTH    = 1000
HEIGHT   = 800

size    = (WIDTH, HEIGHT)
screen  = pygame.display.set_mode(size, 0, 32)

pygame.display.set_caption("Keypress Game 2.0")

clock = pygame.time.Clock()

##Define some Fonts
monitorFont         = pygame.font.Font("{0}/fonts/consola.ttf".format(PATH), 17)
minitorFontBold     = pygame.font.Font("{0}/fonts/consolab.ttf".format(PATH), 17)
monitorFontBig      = pygame.font.Font("{0}/fonts/consola.ttf".format(PATH), 62)
monitorFontBigBold  = pygame.font.Font("{0}/fonts/consolab.ttf".format(PATH), 62)

##Define some Sounds
wrong = pygame.mixer.Sound("wrong.wav")
right = pygame.mixer.Sound("right.wav")
rightmeme = pygame.mixer.Sound("right-meme.wav")
wrongmeme = pygame.mixer.Sound("wrong-meme.wav")

##Define some Images
background = pygame.image.load("metal-texture.png").convert()

##Define some Variables
global KEYBOARD, ALLKEYS
KEYBOARD = {
    0: ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',],
    1: ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    2: ['z', 'x', 'c', 'v', 'b', 'n', 'm']
}
ALLKEYS = [key for rows in KEYBOARD.values() for key in rows] #Just a list of every key

##Define some Functions
def getRow(key, keyboard):
    for row, keys in keyboard.items():
        if key in keys: return row

def chooseNew():
    choice = random.choice(ALLKEYS)
    return choice if not choice == previousKey else chooseNew()

##Game States:
OpeningScreen = False
CountDown = False
MainGame = True
GameOver = False

##Game State Modifiers - Used to set variables
Opening1 = True
Counter1 = True
MainGame1 = True
GameOver1 = True

while True:
    if MainGame:
        if MainGame1: ##If it's the first run through the while-loop, set variables
            memehack = False
            previousKey = None
            correctKey = chooseNew()
            hits = 0
            startTime = time.time()
            timer = 30
            strikes = 0;
            maxStrikes = 5;
            MainGame1 = False

        pressedKey = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit(), sys.exit()
                elif event.key == pygame.K_BACKQUOTE: memehack = not memehack
                else: pressedKey = pygame.key.name(event.key)

        ## -- Game logic
        elapsed = time.time() - startTime
        if pressedKey != None:
            if pressedKey == correctKey:
                hits += 1
                if not memehack: right.play()
                else: rightmeme.play()
            elif pressedKey != correctKey:
                strikes += 1
                if not memehack: wrong.play()
                else: wrongmeme.play()
            previousKey = correctKey
            correctKey = chooseNew()


        ## -- Drawing code
        screen.blit(background, [0, 0])
        pygame.draw.rect(screen, BLACK, [140, 80, 720, 355])
        screen.blit(gfx.keys(keyboard=KEYBOARD, correct=correctKey), [162, 532])
        screen.blit(gfx.timer(elapse=elapsed, maxTime=30, radius=80), [500-80, 260-80])
        screen.blit(gfx.lifebar(width=500, height=25, mistakes=strikes, maxAllowed=maxStrikes), [250, 365])

        ## -- Push those commands to the display
        pygame.display.flip()
        clock.tick(60) ## FPS

        if elapsed > timer or strikes == maxStrikes: MainGame = False
