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

class Sprite:
    def __init__(self, image_file):
        self.sprite = pygame.image.load(image_file).convert_alpha()

        # Set horizontal speed and direction
        self.speedX = random.randint(-5, 5)

        # Set vertical speed and direction
        self.speedY = random.randint(-5, 5)

        self.rect = None
        left, top = 0, 0

        if self.speedX > 0:
            left = -self.sprite.get_width()
        else:
            left = width

        if self.speedY > 0:
            top = -self.sprite.get_height()
        else:
            top = height

        self.rect = pygame.Rect(left, top, *self.sprite.get_size())

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_left(self):
        return self.rect.left

    def get_top(self):
        return self.rect.top

    def move(self):
        self.rect = self.rect.move(self.speedX, self.speedY)


def create_sprite(stype):
    fname = 'meanie.png'
    if stype != 'enemy':
        fname = 'bonus.png'
    return Sprite(fname)

# def create_sprite1(stype):
#     '''Creates a sprite of a specified type'''
#     sprite = None
#     sprite_speed = random.randint(2, 5)
#     if random.randint(0, 1):
#         sprite_speed = -sprite_speed

#     sprite_rect = None

#     sprite_direction_vertical = False
#     if random.randint(0, 1):
#         sprite_direction_vertical = True

#     if stype == 'enemy':
#         sprite = pygame.image.load('meanie.png').convert_alpha()
#     else:
#         sprite = pygame.image.load('bonus.png').convert_alpha()

#     left, top = 0, 0

#     if sprite_direction_vertical:
#         left = random.randint(0, width - sprite.get_width())
#         if sprite_speed > 0:
#             top  = -sprite.get_height()
#         else:
#             top = height
#     else:
#         top = random.randint(0, height - sprite.get_height())
#         if sprite_speed > 0:
#             left  = -sprite.get_width()
#         else:
#             left = width

#     sprite_rect = pygame.Rect(left, top, *sprite.get_size())
    
#     return [sprite, sprite_rect, sprite_speed, sprite_direction_vertical]

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
enemy_view_range = 100

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
        # Calculate the view range
        minX = enemy.get_left() - enemy_view_range
        minY = enemy.get_top() - enemy_view_range

        rangeW = enemy_view_range * 2 + enemy.get_width()
        rangeH = enemy_view_range * 2 + enemy.get_height()

        view_range = pygame.Rect(minX, minY, rangeW, rangeH)

        # Check if an asteroid is near and change direction to the nearest
        nearest_bonus = None
        mindX = enemy_view_range
        mindY = enemy_view_range

        for bonus in bonuses:
            if bonus.rect.colliderect(view_range):
                dX = bonus.get_left() - enemy.get_left()
                dY = bonus.get_top() < enemy.get_top()
                if mindX > dX and mindY > dY:
                    mindX = dX
                    mindY = dY
                    nearest_bonus = bonus
        
        if nearest_bonus:
            if mindX < 0 and enemy.speedX > 0:
                enemy.speedX = - enemy.speedX
            elif mindX > 0 and enemy.speedX < 0:
                enemy.speedX = - enemy.speedX

            if mindY < 0 and enemy.speedY > 0:
                enemy.speedY = - enemy.speedY
            elif mindY > 0 and enemy.speedY < 0:
                enemy.speedY = - enemy.speedY


        enemy.move()

        main_surface.blit(enemy.sprite, enemy.rect)

        if enemy.rect.right < 0:
            enemies.pop(enemies.index(enemy))
        # If the same enemy collides both with the left border and the player
        elif player_rect.colliderect(enemy.rect):
            enemies.pop(enemies.index(enemy))
            score -= 1
            if score < 0:
                game_over = True
                score = 0
                

    # Process bonuses

    for bonus in bonuses:
        bonus.move()

        main_surface.blit(bonus.sprite, bonus.rect)

        if bonus.get_left() > width:
            bonuses.pop(bonuses.index(bonus))

        elif player_rect.colliderect(bonus.rect):
            bonuses.pop(bonuses.index(bonus))
            score += 1
            if score >= max_score:
                win = True
                game_over = True

        else:
            for enemy in enemies:
                if bonus.rect.colliderect(enemy.rect):
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

