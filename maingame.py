##Import Libraries
import pygame, sys, time, random, os

#Import my own files
import gfx, scores
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
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

##Define some Fonts
monitorFont         = pygame.font.Font("{}/fonts/consola.ttf".format(PATH), 17)
monitorFontBold     = pygame.font.Font("{}/fonts/consolab.ttf".format(PATH), 17)
monitorFontBig      = pygame.font.Font("{}/fonts/consola.ttf".format(PATH), 62)
monitorFontBigBold  = pygame.font.Font("{}/fonts/consolab.ttf".format(PATH), 62)

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
def chooseNew():
    choice = random.choice(ALLKEYS)
    return choice if not choice == previousKey else chooseNew()

##Game States:
OpeningScreen = True
CountDown = False
MainGame = False
GameOver = False
NameScreen = False
ScoresScreen = False
ScoresReset = False

##Game State Modifiers - Used to set variables
First = True

while True:
    ## -- These will always be drawn, so only put the code once.
    screen.blit(background, [0, 0]) #Metal background
    pygame.draw.rect(screen, BLACK, [140, 80, 720, 355]) #Screen

    if OpeningScreen: ## ------ OPENING SCREEN
        if First: ##If it's the first run through the while-loop, set variables
            memehack = False
            explainText = [ #list of lines to draw as a block
                ">>> In this game, you will have to press keys as they turn red on",
                ">>> the keyboard you see below you.",
                ">>> You have 30 seconds, although each key you press will",
                ">>> earn you 0.5 extra.",
                ">>> You can make 5 mistakes, the sixth will make you lose.",
                ">>> Press any key when you are ready to continue."
            ]
            First = False

        ## -- Event Detecion
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit(), sys.exit()
                elif event.key == pygame.K_BACKQUOTE: memehack = not memehack
                elif pygame.key.name(event.key) in ALLKEYS or event.key == pygame.K_SPACE:
                    OpeningScreen = False
                    First = True
                    CountDown = True

        ## -- Drawing Code
        screen.blit(gfx.keys(keyboard=KEYBOARD, color=LIGHTRED), [162, 532]) #Keyboard

        for i, line in enumerate(explainText, 0):
            screen.blit(monitorFont.render(line, True, WHITE), [160, 100 + (20 * i)])

    elif CountDown: ## ------ COUNTDOWN SCREEN
        if First:
            waitTime = 3.14 #why not
            startTime = time.time()
            First = False

        ## -- Event Detecion
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit(), sys.exit()
                elif event.key == pygame.K_BACKQUOTE: memehack = not memehack

        ## -- Game Logic
        elapsed = time.time() - startTime

        ## -- Drawing Code
        screen.blit(gfx.keys(keyboard=KEYBOARD, color=LIGHTRED), [162, 532]) #Keyboard
        rounded = int(((waitTime - elapsed) * 100 + 0.5))/100
        screen.blit(monitorFont.render(">>> Starting in {}".format(rounded), True, WHITE), [160, 100])
        screen.blit(monitorFont.render("seconds.", True, WHITE), [350, 100]) #Done in two lines to fix jitter

        ## -- Break Conditions
        if elapsed > waitTime:
            CountDown = False
            First = True
            MainGame = True

    elif MainGame: ## ------ MAIN GAME SCREEN
        if First:
            previousKey = None
            correctKey = chooseNew()
            hits = 0
            startTime = time.time()
            timer = 30
            strikes = 0;
            maxStrikes = 5;
            First = False

        pressedKey = None

        ## -- Event Detecion
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit(), sys.exit()
                elif event.key == pygame.K_BACKQUOTE: memehack = not memehack
                else: pressedKey = pygame.key.name(event.key)

        ## -- Game logic
        elapsed = time.time() - startTime
        if pressedKey in ALLKEYS: #If they press a QWERTY key
            if pressedKey == correctKey:
                hits += 1
                timer += 0.5
                if not memehack: right.play()
                else: rightmeme.play()
            elif pressedKey != correctKey:
                strikes += 1
                if not memehack: wrong.play()
                else: wrongmeme.play()
            previousKey = correctKey
            correctKey = chooseNew()

        ## -- Drawing Code
        screen.blit(gfx.keys(keyboard=KEYBOARD, correct=correctKey), [162, 532]) #Keyboard
        screen.blit(monitorFont.render(">>> You have {0:0<5} seconds left!".format(int((timer - elapsed)*100+0.5)/100), True, WHITE), [160, 100])
        c = LIGHTRED if strikes == maxStrikes else WHITE
        screen.blit(monitorFont.render(">>> You've made {0} {1} so far!".format(strikes, "mistake" if strikes == 1 else "mistakes"), True, c), [160, 120])
        screen.blit(monitorFont.render("Time:", True, WHITE), [360, 250]) #"Time Left:"
        screen.blit(gfx.timer(elapse=elapsed, maxTime=timer, radius=80), [500-80, 260-80]) #Stopwatch
        screen.blit(monitorFont.render("Mistakes Remaining:", True, WHITE), [250 + (500/100), 365 - (25*2/3)]) #"Mistakes Left:"
        screen.blit(gfx.lifebar(width=500, height=25, mistakes=strikes, maxAllowed=maxStrikes), [250, 365]) #Healthbar

        ## -- Break Conditions
        if elapsed > timer or strikes > maxStrikes:
            score = (hits * (round(elapsed*1.75)))-(strikes * 100)
            MainGame = False
            First = True
            GameOver = True

    elif GameOver: ## ------ EVENT RUNDOWN // GAMEOVER
        if First:
            if score < 0:
                shames = [
                    ">>> Less than 0? {}? You really suck, dude.",
                    ">>> Good grief, you're worse than I thought.",
                    ">>> Try harder, next time, okay?",
                    ">>> {}? Jeez, you stink."
                ]
                shametext = shames[random.randint(0, 3)]
            timeTaken = int((elapsed * 100 + 0.5))/100
            startTime = time.time()
            First = False

        ## -- Event Detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit(), sys.exit()
                elif (pygame.key.name(event.key) in ALLKEYS or event.key == pygame.K_SPACE) and elapsed > 0.45: #Wait a bit before being able to leave
                    GameOver = False
                    First = True
                    NameScreen = True

        ## -- Game logic
        elapsed = time.time() - startTime

        ## -- Drawing Code
        screen.blit(gfx.keys(keyboard=KEYBOARD, color=LIGHTRED), [162, 532]) #Keyboard
        screen.blit(monitorFont.render(">>> You managed to hit {} keys correctly.".format(hits), True, WHITE), [160, 140])
        screen.blit(monitorFont.render(">>> You stayed alive for {} seconds.".format(timeTaken), True, WHITE), [160, 160])
        c = YELLOW if score > 0 else LIGHTRED
        screen.blit(monitorFont.render(">>> Your final score is: {}.".format(score), True, c), [160, 240])
        screen.blit(monitorFont.render(">>> You made a total of {0} {1}.".format(strikes, "mistake" if strikes == 1 else "mistakes"), True, WHITE), [160, 180])
        screen.blit(monitorFont.render(">>> Press Space to continue.", True, WHITE), [160, 360])
        failText = "You made one too many mistakes!" if strikes == maxStrikes else "You're out of time!"
        screen.blit(monitorFont.render(failText, True, WHITE), [160, 100])
        if score < 0: screen.blit(monitorFont.render(shametext.format(score), True, WHITE), [160, 260])

    elif NameScreen: ## ------ ARCADE STYLE NAME-GET
        if First:
            pressedKeys = []
            name = ['A', 'A', 'A']
            pos = 0
            First = False

        ## -- Event Detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit(), sys.exit()
                elif (event.key == pygame.K_BACKSPACE or event.key == pygame.K_LEFT) and pos > 0: pos -= 1
                elif event.key == pygame.K_RIGHT and pos < 2: pos += 1
                elif pygame.key.name(event.key) in ALLKEYS:
                    pressedKeys.append(pygame.key.name(event.key))
                    name[pos] = pygame.key.name(event.key).upper()
                    if pos < 2: pos += 1
                elif event.key == pygame.K_RETURN: ## -- Break Conditions
                    name = "".join(name)
                    NameScreen = False
                    First = True
                    ScoresScreen = True
            elif event.type == pygame.KEYUP:
                if pygame.key.name(event.key) in ALLKEYS:
                    pressedKeys = [keys for keys in pressedKeys if keys != pygame.key.name(event.key)]
                    # ^^ remove the un-pressed key

        ## -- Drawing Code
        screen.blit(gfx.keys(keyboard=KEYBOARD, correct=pressedKeys), [162, 532]) #Keyboard
        screen.blit(monitorFont.render(">>> Type your initials/name. This will be used to keep track of highscores.", True, WHITE), [160, 100])
        screen.blit(monitorFont.render(">>> Press Enter to accept.", True, WHITE), [160, 120])
        for i, letter in enumerate(name):
            if i == pos:
                c = YELLOW
                font = monitorFontBigBold
            else:
                c = WHITE
                font = monitorFontBig
            screen.blit(font.render(letter.upper(), True, c), [415 + (50 * i), 220])

    elif ScoresScreen: ## ------ HIGH SCORES SCREEN
        if First:
            index = scores.insertScore(score=score, name=name)
            ## ^This will both insert the score and get the place at which it is in the list
            SCORES = scores.load()
            memehack = False
            First = False

        ## -- Event Detecion
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_n: pygame.quit(), sys.exit()
                elif event.key == pygame.K_y:
                    First = True
                    OpeningScreen = True
                    ScoresScreen = False
                elif event.key == pygame.K_r:
                    First = True
                    ResetScreen = True
                    ScoresScreen = False

        ## -- Game Logic

        ## -- Drawing Code
        screen.blit(gfx.keys(keyboard=KEYBOARD, color=LIGHTRED), [162, 532]) #Keyboard
        screen.blit(monitorFont.render(">>> Highscores are:", True, WHITE), [160, 100])
        for i, line in enumerate(SCORES, 0):
            if i == index:
                c = YELLOW
                font = monitorFontBold
            else:
                c = WHITE
                font = monitorFont
            screen.blit(font.render(">>> {0:>3} {1:<5} --- {2}".format(str(i + 1) + ".", line['amount'], line['name']), True, c), [160, 140 + (20 * i)])
        screen.blit(monitorFont.render(">>> Do you want to play again? Press either 'Y' or 'N'.", True, WHITE), [160, 360])
        screen.blit(monitorFont.render(">>> Do you want to reset the highscores? Press 'R' if you do.", True, WHITE), [160, 380])

    elif ResetScreen: ##  ------ SCORES RESET
        if First:
            bools = {
                'y': False,
                'e': False,
                's': False
            }
            First = False

        ## -- Event Detecion
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit(), sys.exit()
                elif pygame.key.name(event.key) in bools.keys():
                    bools[pygame.key.name(event.key)] = True
                elif event.key == pygame.K_c:
                    First = True
                    ResetScreen = False
                    ScoresScreen = True
            elif event.type == pygame.KEYUP:
                if pygame.key.name(event.key) in bools.keys():
                    bools[pygame.key.name(event.key)] = False

        ## -- Game Logic
        if all(bools.values()):
            scores.reset()
            score = 0
            name = None
            First = True
            ResetScreen = False
            ScoresScreen = True

        ## -- Drawing Code
        screen.blit(gfx.keys(keyboard=KEYBOARD, correct=[key for key, value in bools.items() if value]), [162, 532]) #Keyboard
        screen.blit(monitorFont.render(">>> Are you extra, super sure? If you are, hold down 'Y', 'E', and 'S'", True, WHITE), [160, 100])
        screen.blit(monitorFont.render(">>> all at the same time. Press 'C' to cancel.", True, WHITE), [160, 120])
        for i, letter in enumerate(bools):
            if bools[letter]:
                c = YELLOW
                font = monitorFontBigBold
            else:
                c = WHITE
                font = monitorFontBig
            screen.blit(font.render(letter.upper(), True, c), [415 + (50 * i), 220])

    if memehack: screen.blit(monitorFontBold.render(">>> MEME HACK ACTIVATED", True, RED), [0, 0])
    ## -- Push those commands to the display
    pygame.display.flip()
    clock.tick(60) ## FPS
