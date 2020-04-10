import pygame
import random
import sys
from pygame.locals import *
from itertools import cycle

FPS = 30

SCREEN_WIDTH = 388
SCREEN_HEIGHT = 612
PIPE_GAP = 100

BASE_Y = int(SCREEN_HEIGHT * 0.8)

IMAGES, SOUNDS = {}, {}


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("FlapPy Bird")

    # zuragnuudiig oruulj ireh
    # onoo haruulah toonuud
    IMAGES['numbers'] = (
        pygame.image.load("assets/sprites/0.png").convert_alpha(),
        pygame.image.load("assets/sprites/1.png").convert_alpha(),
        pygame.image.load("assets/sprites/2.png").convert_alpha(),
        pygame.image.load("assets/sprites/3.png").convert_alpha(),
        pygame.image.load("assets/sprites/4.png").convert_alpha(),
        pygame.image.load("assets/sprites/5.png").convert_alpha(),
        pygame.image.load("assets/sprites/6.png").convert_alpha(),
        pygame.image.load("assets/sprites/7.png").convert_alpha(),
        pygame.image.load("assets/sprites/8.png").convert_alpha(),
        pygame.image.load("assets/sprites/9.png").convert_alpha(),
    )
    # ariin fon
    IMAGES["background"] = pygame.image.load(
        "assets/sprites/background-day.png").convert()

    IMAGES['player'] = (
        pygame.image.load(
            "assets/sprites/yellowbird-upflap.png").convert_alpha(),
        pygame.image.load(
            "assets/sprites/yellowbird-midflap.png").convert_alpha(),
        pygame.image.load(
            "assets/sprites/yellowbird-downflap.png").convert_alpha(),
    )
    IMAGES['pipe'] = (
        pygame.transform.flip(
            pygame.image.load("assets/sprites/pipe-green.png").convert_alpha(),
            False, True),
        pygame.image.load("assets/sprites/pipe-green.png").convert_alpha(),
    )
    IMAGES["message"] = pygame.image.load(
        "assets/sprites/message.png").convert_alpha()

    IMAGES["gameover"] = pygame.image.load(
        "assets/sprites/gameover.png").convert_alpha()
    IMAGES["base"] = pygame.image.load("assets/sprites/base.png").convert()
# Хэрвээ windows үйлдэлийг систем бол way өргөтгөлтэй дуу байна
    if "win" in sys.platform:
        soundExt = ".wav"
    else:
        soundExt = ".ogg"

    SOUNDS["die"] = pygame.mixer.Sound("assets/audio/die" + soundExt)
    SOUNDS["point"] = pygame.mixer.Sound("assets/audio/point" + soundExt)
    SOUNDS["hit"] = pygame.mixer.Sound("assets/audio/hit" + soundExt)
    SOUNDS["swoosh"] = pygame.mixer.Sound("assets/audio/swoosh" + soundExt)
    SOUNDS["wing"] = pygame.mixer.Sound("assets/audio/wing" + soundExt)
    SOUNDS["theme"] = pygame.mixer.Sound("assets/audio/theme" + soundExt)
    while True:
        info = show_welcome_screen()
        info = play_game(info)
        show_game_over(info)


def show_welcome_screen():
    """Ehleliin delgetsnii animation
    """
    global SPEED, BASE_MAX_SHIFT
    SPEED = 4
    playerModel = cycle((0, 1, 2, 1))
    modelNumber = 0
    messageX = int((SCREEN_WIDTH - IMAGES["message"].get_width()) / 2)
    messageY = int(SCREEN_HEIGHT * 0.12)
    BASE_MAX_SHIFT = IMAGES["base"].get_width() - SCREEN_WIDTH
    baseX = 0
    currentAlt = {"alt": 0, "dir": 1}
    fpsCount = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                SOUNDS['wing'].play()
                return {
                    'playerY': set_alt(currentAlt),
                    'baseX': baseX
                }
        SCREEN.blit(IMAGES["background"], (0, 0))
        SCREEN.blit(IMAGES["base"], (-(baseX % BASE_MAX_SHIFT), BASE_Y))
        SCREEN.blit(IMAGES["message"], (messageX, messageY))
        SCREEN.blit(IMAGES["player"][modelNumber], (70, set_alt(currentAlt)))

        pygame.display.update()
        baseX += SPEED
        fpsCount += 1
        if fpsCount % 5 == 0:
            modelNumber = next(playerModel)
        FPSCLOCK.tick(FPS)


def play_game(info):
    ##########
    FLAP_ACC = -9  # dalawch deweh huch
    MAX_VEL = 10  # dooshoo unah max hurd
    playerVelY = -9  # playeriin shiljih hurd
    ROT_VEL = 3  # playeriin dooshoo ergeh hurd
    gravity = 1  # gazarin tatah huchni hurdatgal
    ROT_THRESH = 20  # deeshee ergeh max untsog
    MAX_ROT = 45  # deeshee ergeh hyzgaar
    MIN_ROT = -90  # dooshoo ergeh hyzgaar
    #####
    baseX = info['baseX']
    playerModel = cycle((0, 1, 2, 1))
    modelNumber = 0
    fpsCount = 0
    score = 0
    playerX, playerY = 70, info['playerY']
    playerHeight = IMAGES['player'][modelNumber].get_height()
    player_angle = MAX_ROT
    pipes = []
    pipes.append(get_pipe())
    pipes.append(get_pipe())
    pipes[0]['x'] = SCREEN_WIDTH / 2 + 200
    pipes[1]['x'] = SCREEN_WIDTH + 200
    pipeRects = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if playerY > -2 * playerHeight:
                    SOUNDS['wing'].play()
                    playerVelY = FLAP_ACC
                    player_angle = MAX_ROT

        # onoo shalgah
        score = check_score(score, playerX, pipes)
        # Hurdnii hyzgaariig dawaagui bol unah hurdatgalig nem
        if playerVelY < MAX_VEL:
            playerVelY += gravity
        playerY += min(playerVelY, BASE_Y - playerY - playerHeight)

        if pipes[0]['x'] < - IMAGES['pipe'][0].get_width():
            del(pipes[0])
        if 0 < pipes[0]['x'] < 5:
            pipes.append(get_pipe())

        # ergeltiin hyzgaarig dawagui bol ergeh untsgiig nem
        if player_angle > MIN_ROT:
            player_angle -= ROT_VEL
        angle = min(player_angle, ROT_THRESH)

        # Animation heseg
        SCREEN.blit(IMAGES["background"], (0, 0))

        for pipe in pipes:
            pipe['x'] -= SPEED
            upperRect = SCREEN.blit(
                IMAGES["pipe"][0], (int(pipe['x']), int(pipe['yUpper'])))
            lowerRect = SCREEN.blit(
                IMAGES["pipe"][1], (int(pipe['x']), int(pipe['yLower'])))
            upperRect = upperRect.inflate(-7, -7)
            lowerRect = lowerRect.inflate(-7, -7)
            pipeRects.append(upperRect)
            pipeRects.append(lowerRect)

        # show score
        show_score(score)
        baseRect = SCREEN.blit(
            IMAGES["base"], (-(baseX % BASE_MAX_SHIFT), BASE_Y))
        playerSurface = pygame.transform.rotate(
            IMAGES["player"][modelNumber], angle)
        playerRect = SCREEN.blit(playerSurface, (playerX, playerY))
        playerRect = playerRect.inflate(-9, -12)

        # check collision
        if check_collision(playerRect, pipeRects) != -1:
            return {
                'type': 'hit',
                'playerX': playerX,
                'playerY': playerY,
                'playerVelY': playerVelY,
                'modelNumber': modelNumber,
                'angle': angle,
                'pipes': pipes,
                'baseX': baseX,
                'score': score,
                'playerHeight': playerHeight
            }
        if check_fall(playerRect, baseRect) == True:
            return {
                'type': 'fall',
                'playerX': playerX,
                'playerY': playerY,
                'playerVelY': playerVelY,
                'modelNumber': modelNumber,
                'angle': angle,
                'pipes': pipes,
                'baseX': baseX,
                'score': score,
                'playerHeight': playerHeight
            }
        pipeRects.clear()
        pygame.display.update()
        baseX += SPEED
        fpsCount += 1
        if fpsCount % 5 == 0:
            modelNumber = next(playerModel)
        FPSCLOCK.tick(FPS)


def show_game_over(info):
    playerX = info['playerX']
    playerY = info['playerY']
    playerVelY = info['playerVelY']
    modelNumber = info['modelNumber']
    angle = info['angle']
    pipes = info['pipes']
    baseX = info['baseX']
    score = info['score']
    playerHeight = info['playerHeight']
    MIN_ROT = -90
    MAX_VEL = 10
    ROT_VEL = 7
    gravity = 2
    gameOverX = (SCREEN_WIDTH - IMAGES["gameover"].get_width()) / 2
    # duu gargah
    SOUNDS['hit'].play()
    if info['type'] == 'hit':
        SOUNDS['die'].play()

    # towch darah
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                return
    # unagaah
        if playerVelY < MAX_VEL:
            playerVelY += gravity
        playerY += min(playerVelY, BASE_Y - playerY - playerHeight)
    # ergeldeh
        if info['type'] == 'hit':
            if angle > MIN_ROT:
                angle -= ROT_VEL

    # Animation heseg
        SCREEN.blit(IMAGES["background"], (0, 0))

        for pipe in pipes:
            upperRect = SCREEN.blit(
                IMAGES["pipe"][0], (int(pipe['x']), int(pipe['yUpper'])))
            lowerRect = SCREEN.blit(
                IMAGES["pipe"][1], (int(pipe['x']), int(pipe['yLower'])))
        # show score
        show_score(score)
        baseRect = SCREEN.blit(
            IMAGES["base"], (-(baseX % BASE_MAX_SHIFT), BASE_Y))
        playerSurface = pygame.transform.rotate(
            IMAGES["player"][modelNumber], angle)
        playerRect = SCREEN.blit(playerSurface, (playerX, playerY))
        SCREEN.blit(IMAGES["gameover"], (int(gameOverX), SCREEN_HEIGHT * 0.3))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def set_alt(currentAlt):
    playerY = int((SCREEN_HEIGHT - IMAGES["player"][0].get_height()) / 2)

    if abs(currentAlt["alt"]) == 16:
        currentAlt["dir"] *= -1
    if currentAlt["dir"] == 1:
        currentAlt["alt"] += 1
    else:
        currentAlt["alt"] -= 1

    alt = playerY + currentAlt["alt"]

    return alt


def get_pipe():
    pipe_height = IMAGES['pipe'][0].get_height()
    x = SCREEN_WIDTH + 10
    yLower = random.randint(int(SCREEN_HEIGHT * 0.4), int(SCREEN_HEIGHT * 0.6))
    yUpper = yLower - PIPE_GAP - pipe_height

    return {'x': x, 'yLower': int(yLower), 'yUpper': int(yUpper)}
    SOUNDS['wing'].play()


def check_score(score, playerX, pipes):
    '''Onoo shalgadag function

    Parameters:
        score (int) - odoogin onoo

    Return:
        int - Onoo

    Preconditions:
        None
    '''

    playerMidX = int((playerX + IMAGES['player'][0].get_width()) / 2)
    pipeMidX = 0

    for pipe in pipes:
        pipeMidX = int((pipe['x'] + IMAGES['pipe'][0].get_width()) / 2)
        if pipeMidX < playerMidX < pipeMidX + 3:
            SOUNDS['point'].play()
            return score + 1
    return score


def show_score(score):

    scoreDigits = str(score)
    width = 0
    for digit in scoreDigits:
        width += IMAGES['numbers'][int(digit)].get_width()
    offset = (SCREEN_WIDTH - width) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][int(digit)],
                    (int(offset), int(SCREEN_HEIGHT * 0.2)))
        offset += IMAGES['numbers'][int(digit)].get_width()


def check_fall(playerRect, baseRect):
    return playerRect.colliderect(baseRect)


def check_collision(playerRect, pipeRects):
    return playerRect.collidelist(pipeRects)


if __name__ == "__main__":
    main()
