import pygame
import random
import math

from pygame import mixer

# Initialize pygame
pygame.init()

# creating a screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.jpg')

#background sound
mixer.music.load('bgmusic.wav')
mixer.music.set_volume(0.035)
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Tiêu diệt minh râu")

# Player
player_img = pygame.image.load(('battleship.png'))
player_X = 370
player_Y = 480
playerX_change = 0

# Enemy
enemy_img = []
enemy_X = []
enemy_Y = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):

    enemy_img.append(pygame.image.load('villain.png'))
    enemy_X.append(random.randint(0, 735))
    enemy_Y.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# bullet
bullet_img = pygame.image.load(('bullet.png'))
bullet_X = 0
bullet_Y = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'

#Score

score_value = 0
font = pygame.font.Font('8bit.ttf', 32)

textX = 10
textY = 10

#Game over
over_font = pygame.font.Font('8bit.ttf', 64)

def show_score(x,y):
    score = font.render('Score :' + str(score_value),True, (255,255,255))
    screen.blit(score, (x, y))

def game_over():
    over_text = over_font.render('YOU SUCK', True, (255, 255, 255))
    screen.blit(over_text, (250, 250))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


def player(x, y):
    screen.blit(player_img, (x, y))  # draw ont he screen


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def isCollision(enemy_X, enemy_Y, bullet_X, bullet_Y):
    distance = math.sqrt((math.pow(enemy_X - bullet_X, 2)) + (math.pow(enemy_Y - bullet_Y, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.set_volume(0.035)
                    bullet_sound.play()
                    bullet_X = player_X
                    fire_bullet(bullet_X, bullet_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # screen color from 0 to 255
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    # 5 = 5 + -0.1 -> 5= 5 - 0.1
    # 5 = 5 + 0.1
    player_X += playerX_change

    if player_X <= 0:
        player_X = 0
    elif player_X >= 736:
        player_X = 736
    player_X += playerX_change

    #Enemy movement
    for i in range(num_of_enemies):
        if enemy_Y[i] > 440:
            for j in range(num_of_enemies):
                enemy_Y[j] = 2000
            game_over()
            break

        enemy_X[i] += enemyX_change[i]
        if enemy_X[i] <= 0:
            enemyX_change[i] = 0.3
            enemy_Y += enemyY_change
        elif enemy_X[i] >= 736:
            enemyX_change[i] = -0.3
            enemy_Y[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.set_volume(0.035)
            explosion_sound.play()
            bullet_Y = 480
            bullet_state = 'ready'
            score_value += 1
            enemy_X[i] = random.randint(0, 735)
            enemy_Y[i] = random.randint(50, 150)

        enemy(enemy_X[i], enemy_Y[i], i)



    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 480
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire_bullet(bullet_X, bullet_Y)
        bullet_Y -= bulletY_change

    enemy_X += enemyX_change

    player(player_X, player_Y)
    show_score(textX, textY)
    pygame.display.update()
