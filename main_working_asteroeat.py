import pygame
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random

def show_score():
    main_surface.blit(font.render(str(score), True, GREEN), (width - 100, 0) )
    main_surface.blit(font.render(str(enemy_score), True, VIOLET), (100, 0) )

def won_lost():

    main_surface.blit(bg, (0, 0))

    show_score()

    s = "***  На здоров'ячко!  ***"
    if not win:
        s = "***    Скуштуй ще     ***"

    result_font = pygame.font.SysFont('Verdana', 32)
    main_surface.blit(result_font.render(s, True, YELLOW), (200, 280) )
    
    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(15) 

def create_sprite(stype):
    '''Creates a sprite of a specified type'''
    sprite = pygame.Surface((20, 20))
    sprite_speed = random.randint(2, 5)
    if random.randint(0, 1):
        sprite_speed = -sprite_speed

    sprite_rect = None

    #TODO: make a sprite appear from the left/right/top/bottom
    #TODO: and make speed for each sprite

    sprite_direction_vertical = False
    if random.randint(0, 1):
        sprite_direction_vertical = True

    if stype == 'enemy':
        sprite = pygame.image.load('meanie.png').convert_alpha()
    else:
        sprite = pygame.image.load('bonus.png').convert_alpha()

    left, top = 0, 0

    if sprite_direction_vertical:
        left = random.randint(0, width - sprite.get_width())
        if sprite_speed > 0:
            top  = -sprite.get_height()
        else:
            top = height
    else:
        top = random.randint(0, height - sprite.get_height())
        if sprite_speed > 0:
            left  = -sprite.get_width()
        else:
            left = width

    sprite_rect = pygame.Rect(left, top, *sprite.get_size())
    
    return [sprite, sprite_rect, sprite_speed, sprite_direction_vertical]

### Setup ###

pygame.init()
pygame.display.set_caption("АстероЇд")
pygame.display.set_icon(pygame.image.load('player.png'))
FPS = pygame.time.Clock()

# Constants

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 78, 153, 67
VIOLET = 163, 77, 253
YELLOW = 232, 253, 77

SPRITE = 0
SPRITE_RECT = 1
SPRITE_SPEED = 2
SPRITE_DIRECTION_VERTICAL = 3

clock = pygame.time.Clock()

font = pygame.font.SysFont('Verdana', 20)

# Main surface setup
screen = width, height = 800, 600
main_surface = pygame.display.set_mode(screen)

bg = pygame.transform.scale(pygame.image.load('bg.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

# Player setup
player = pygame.image.load('player.png').convert_alpha()
player_rect = pygame.Rect(int(width / 2) - int(player.get_width() / 2), int(height / 2) - int(player.get_height() / 2), *player.get_size())
player_speed = 5

# Enemies setup
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []

# Bonuses setup
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)
bonuses = []

score = 0
max_score = 3
enemy_score = 0
win = False
game_over = False

### Game loop ###

is_working = True
while is_working:
    if game_over:
        won_lost()

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_sprite('enemy'))
        if event.type == CREATE_BONUS:
            bonuses.append(create_sprite('bonus'))

    # Fill the main surface
    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    # Draw the player
    main_surface.blit(player, player_rect)

    show_score()

    # Process enemies

    for enemy in enemies:
        # Check if an asteroid is near and change direction

        

        # Continue moving if the enemy does not see asteroids
        if enemy[SPRITE_DIRECTION_VERTICAL]:
            enemy[SPRITE_RECT] = enemy[SPRITE_RECT].move(0, enemy[SPRITE_SPEED])
        else:
            enemy[SPRITE_RECT] = enemy[SPRITE_RECT].move(enemy[SPRITE_SPEED], 0)

        main_surface.blit(enemy[SPRITE], enemy[SPRITE_RECT])

        if enemy[SPRITE_RECT].right < 0:
            enemies.pop(enemies.index(enemy))
        # If the same enemy collides both with the left border and the player
        elif player_rect.colliderect(enemy[SPRITE_RECT]):
            enemies.pop(enemies.index(enemy))
            score -= 1
            if score < 0:
                game_over = True
                score = 0
                

    # Process bonuses

    for bonus in bonuses:
        if bonus[SPRITE_DIRECTION_VERTICAL]:
            bonus[SPRITE_RECT] = bonus[SPRITE_RECT].move(0, bonus[SPRITE_SPEED])
        else:
            bonus[SPRITE_RECT] = bonus[SPRITE_RECT].move(bonus[SPRITE_SPEED], 0)

        main_surface.blit(bonus[SPRITE], bonus[SPRITE_RECT])

        if bonus[SPRITE_RECT].left > width:
            bonuses.pop(bonuses.index(bonus))

        elif player_rect.colliderect(bonus[SPRITE_RECT]):
            bonuses.pop(bonuses.index(bonus))
            score += 1
            if score >= max_score:
                win = True
                game_over = True

        else:
            for enemy in enemies:
                if bonus[SPRITE_RECT].colliderect(enemy[SPRITE_RECT]):
                    if bonus in bonuses:
                        bonuses.pop(bonuses.index(bonus))
                        enemy_score += 1
                        if enemy_score >= max_score:
                            show_score()
                            game_over = True

    # Process keys

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
         player_rect = player_rect.move(0, player_speed)
    elif pressed_keys[K_UP] and not player_rect.top <= 0:
         player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
         player_rect = player_rect.move(-player_speed, 0)
    elif pressed_keys[K_RIGHT] and not player_rect.right >= width:
         player_rect = player_rect.move(player_speed, 0)

    # Redraw the game
    pygame.display.flip()

