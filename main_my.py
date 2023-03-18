import pygame
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random

### Setup ###

pygame.init()
FPS = pygame.time.Clock()

# Constants

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

SPRITE = 0
SPRITE_RECT = 1
SPRITE_SPEED = 2

# Main surface setup
screen = width, height = 800, 600
main_surface = pygame.display.set_mode(screen)
main_surface.fill(BLACK)

# Ball setup
ball = pygame.Surface((20, 20))
ball.fill(WHITE)
ball_rect = ball.get_rect()
ball_speed = 5

def create_sprite(stype):
    '''Creates a sprite of a specified type'''
    sprite = pygame.Surface((20, 20))
    sprite_speed = random.randint(2, 5)
    sprite_rect = None

    if stype == 'enemy':
        sprite.fill(RED)
        sprite_rect = pygame.Rect(width, random.randint(0, height - 20), *sprite.get_size())
    else:
        sprite.fill(GREEN)
        sprite_rect = pygame.Rect(random.randint(0, width - 20), -20, *sprite.get_size())
    
    return [sprite, sprite_rect, sprite_speed]

# Enemies setup
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []

# Bonuses setup
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)
bonuses = []

### Game loop ###

is_working = True
while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_sprite('enemy'))
        if event.type == CREATE_BONUS:
            bonuses.append(create_sprite('bonus'))

    # Fill the main surface
    main_surface.fill(BLACK)

    # Draw the ball
    main_surface.blit(ball, ball_rect)

    # Process enemies

    for enemy in enemies:
        enemy[SPRITE_RECT] = enemy[SPRITE_RECT].move(-enemy[SPRITE_SPEED], 0)
        main_surface.blit(enemy[SPRITE], enemy[SPRITE_RECT])

        if enemy[SPRITE_RECT].left < 0:
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[SPRITE_RECT]):
            enemies.pop(enemies.index(enemy))

    # Process bonuses

    for bonus in bonuses:
        bonus[SPRITE_RECT] = bonus[SPRITE_RECT].move(0, bonus[SPRITE_SPEED])
        main_surface.blit(bonus[SPRITE], bonus[SPRITE_RECT])

        if bonus[SPRITE_RECT].bottom < 0:
            bonuses.pop(bonuses.index(bonus))

        if ball_rect.colliderect(bonus[SPRITE_RECT]):
            bonuses.pop(bonuses.index(bonus))

    # Process keys

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_DOWN] and not ball_rect.bottom >= height:
         ball_rect = ball_rect.move(0, ball_speed)
    elif pressed_keys[K_UP] and not ball_rect.top <= 0:
         ball_rect = ball_rect.move(0, -ball_speed)

    if pressed_keys[K_LEFT] and not ball_rect.left <= 0:
         ball_rect = ball_rect.move(-ball_speed, 0)
    elif pressed_keys[K_RIGHT] and not ball_rect.right >= width:
         ball_rect = ball_rect.move(ball_speed, 0)

    # Redraw the game
    pygame.display.flip()

