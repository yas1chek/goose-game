import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import os
import random

#window size:
H = 700
W = 1250

#colour constants:
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)

#pygame initialisation
pygame.init()

main_display = pygame.display.set_mode((W, H))
FONT = pygame.font.SysFont("verdana", 20)
FPS = pygame.time.Clock()

#background settings:
bg = pygame.transform.scale(pygame.image.load("background.png"), (W, H))
bgX1 = 0
bgX2 = bg.get_width()
bgMove = 3

#player settings:
IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)
playerSize = (20, 20)
player = pygame.image.load("player.png").convert_alpha()
playerRect = player.get_rect()
#player control:
playerMoveDown = [0, 4]
playerMoveRight = [4, 0]
playerMoveUp = [0, -4]
playerMoveLeft = [-4, 0]

#enemy settings & random spawn:
def createEnemy():
    enemySize = (30, 30)
    enemy = pygame.image.load("enemy.png").convert_alpha()
    enemyRect = pygame.Rect(W, random.randint(50, H-70), *enemySize)
    enemyMove = [random.randint(-8,-4), 0]
    return [enemy, enemyRect, enemyMove]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []

#bonus settings & random spawn:
def createBonus():
    bonusSize = (10, 10)
    bonus = pygame.image.load("bonus.png").convert_alpha()
    bonusRect = pygame.Rect(random.randint(20, W-70), 40, *bonusSize)
    bonusMove = [0, random.randint(2, 6)]
    return [bonus, bonusRect, bonusMove]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)
bonuses = []

#player's images change settings:
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 100)
scoreTxt = "Points: "
score = 0
imageIndex = 0
#game settings:
playing = True
while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
#creating sprites:
        if event.type == CREATE_ENEMY:
            enemies.append(createEnemy())
        if event.type == CREATE_BONUS:
            bonuses.append(createBonus())
#changind player's images:
        if event.type == CHANGE_IMAGE:
            player = pygame. image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[imageIndex]))
            imageIndex += 1
            if imageIndex >= len(PLAYER_IMAGES):
                imageIndex = 0
#moving background:
    bgX1 -= bgMove
    bgX2 -= bgMove

    if bgX1 < -bg.get_width():
        bgX1 = bg.get_width()
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_display.blit(bg, (bgX1, 0))
    main_display.blit(bg, (bgX2, 0))

#controls:
    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and playerRect.bottom < H:
        playerRect = playerRect.move(playerMoveDown)

    if keys[K_RIGHT] and playerRect.right < W:
        playerRect = playerRect.move(playerMoveRight)

    if keys[K_UP] and playerRect.top > 0:
        playerRect = playerRect.move(playerMoveUp)

    if keys[K_LEFT] and playerRect.left > 0:
        playerRect = playerRect.move(playerMoveLeft)

#showing sprites:
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
#loosing event:
        if playerRect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
#scoring event:
        if playerRect.colliderect(bonus[1]):
            score += 5
            bonuses.pop(bonuses.index(bonus))

#score count placement:
    main_display.blit(FONT.render(str(score), True, BLACK), (W-50, 20))
    main_display.blit(FONT.render(str(scoreTxt), True, BLACK), (W-130, 20))
    main_display.blit(player, playerRect)

    pygame.display.flip()

#deletimg enemies & bonuses:
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
    for bonus in bonuses:
        if bonus[1].left < 0:
            bonuses.pop(bonuses.index(bonus))