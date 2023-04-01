import pygame
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random

def show_score(show_bottom_line=True):
    #main_surface.blit(status_bar, status_bar_rect)
    main_surface.blit(font.render(f"Ви з'їли: {score}", True, GREEN), (width - 200, 0) )
    main_surface.blit(font.render(f"Ненажери з'їли: {enemy_score}", True, VIOLET), (30, 0) )
    main_surface.blit(font.render(f"Ненажер: {len(enemies)}", True, YELLOW), (350, 0) )
    if show_bottom_line:
        message = "          Смачного!          "
        if score > (max_score / 3 * 2):
            message = "   Ненажери полюють на вас   "
        elif score > max_score / 3:
            message = "Ненажери полюють на астероїди"
        main_surface.blit(font.render(message, True, WHITE), (240, height - 40) )

def won_lost():

    main_surface.blit(bg, (0, 0))

    show_score(False)

    s = "***  На здоров'ячко!  ***"
    if not win:
        s = "***    Спробуй ще     ***"

    result_font = pygame.font.SysFont('monospace', 32)
    result_font.set_bold(True)
    main_surface.blit(result_font.render(s, True, YELLOW), (170, 280) )
    
    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        FPS.tick(15)

class Sprite:
    def __init__(self, image_file, left = 0, top = 0, speed = 0, view_range = 50):
        self.name = image_file
        self.sprite = pygame.image.load(image_file).convert_alpha()

        # Set width and height
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

        # Set Rect

        self.left = left
        self.top = top

        self.rect = pygame.Rect(self.left, self.top, *self.sprite.get_size())

        # Set speed
        self.speed = speed
        self.speedX = 0
        self.speedY = 0

        # Set view range
        self.view_range = view_range

    def set_left(self, left):
        self.left = left
        self.rect = pygame.Rect(self.left, self.top, *self.sprite.get_size())

    def set_top(self, top):
        self.top = top
        self.rect = pygame.Rect(self.left, self.top, *self.sprite.get_size())

    def center(self, screen_width, screen_height):
        self.rect.centerx = int(screen_width / 2)
        self.rect.centery = int(screen_height / 2)

    def set_random_direction(self, screen_width, screen_height):
        # Set speed and direction
        self.speed = random.randint(2, 5)

        vertical = random.randint(0, 1)
        if vertical:
            self.speedX = 0
            up = random.randint(0, 1)
            if up:
                self.speedY = -self.speed
            else:
                self.speedY = self.speed
        else:
            self.speedY = 0
            left = random.randint(0, 1)
            if left:
                self.speedX = -self.speed
            else:
                self.speedX = self.speed

        if vertical:
            # If moving down, place to the top of the screen
            if self.speedY > 0:
                self.top = -self.sprite.get_height()
            # If moving up, place to the bottom of the screen
            else:
                self.top = screen_height


        # If moving right, place to the left of the screen
        if self.speedX > 0:
            self.left = -self.sprite.get_width()
        # If moving right, place to the right of the screen
        else:
            self.left = screen_width


    def collides(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def sees(self, sprite):
        self.view_rect = pygame.Rect(self.rect.left - self.view_range,\
            self.rect.top - self.view_range,\
            self.rect.right + self.view_range,\
            self.rect.bottom + self.view_range)

        return self.view_rect.colliderect(sprite.rect)

    def turn_to(self, sprite):
        dX = sprite.get_left() - self.get_left()
        dY = sprite.get_top() - self.get_top()
        if dX < 0: # other is at the left
            self.speedX = -self.speed
        elif dX > 0: # other is at the right
            self.speedX = self.speed
        else:
            self.speedX = 0

        if dY < 0: # other is at the top
            self.speedY = -self.speed
        elif dY > 0: # other is at the bottom
            self.speedY = self.speed
        else:
            self.speedY = 0

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_left(self):
        return self.rect.left

    def get_top(self):
        return self.rect.top

    def get_right(self):
        return self.rect.right

    def get_bottom(self):
        return self.rect.bottom

    def move(self):
        self.rect = self.rect.move(self.speedX * self.speed, self.speedY * self.speed)
        # print(f'Moving {self.name} {self.speedX * self.speed}, {self.speedY * self.speed} at {self.left}, {self.top}')

    def stop(self):
        self.speedX = 0
        self.speedY = 0

    def blit(self, surface):
        surface.blit(self.sprite, self.rect)

    def set_random_speed(self):
        self.speed = random.randint(2, max_speed)

    def set_speed(self, speed):
        self.speed = speed

def create_enemy():
    fname = 'meanie.png'
    sprite = Sprite(fname)
    sprite.set_left(width)
    sprite.set_top(random.randint(0, height - sprite.get_height()))
    sprite.speedX = -1
    sprite.set_random_speed()
    # print(f'Created enemy moving {sprite.speedX}, {sprite.speedY} at {sprite.left}, {sprite.top}')
    return sprite

def create_bonus():
    fname = 'bonus.png'
    sprite = Sprite(fname)
    sprite.set_left(random.randint(0, width - sprite.get_width()))
    sprite.set_top(-sprite.get_height())
    sprite.speedY = 1
    sprite.set_random_speed()
    # print(f'Created bonus moving {sprite.speedX}, {sprite.speedY} at {sprite.left}, {sprite.top}')
    return sprite


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

font = pygame.font.SysFont('monospace', 20)
font.set_bold(True)

# Main surface setup
screen = width, height = 800, 600
main_surface = pygame.display.set_mode(screen)

bg = pygame.transform.scale(pygame.image.load('bg.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

max_speed = 3

# Player setup
player = Sprite('player.png', 0, 0, max_speed)
player.center(width, height)

# Score ribbon
# status_bar = pygame.Surface((width, 40))
# status_bar.fill(YELLOW)
# status_bar_rect = status_bar.get_rect()

# Enemies setup
CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_ENEMY_INTERVAL = 1500
CREATE_ENEMY_STEP = 50
pygame.time.set_timer(CREATE_ENEMY, CREATE_ENEMY_INTERVAL)
enemies = []
enemy_view_range = 100
MAX_ENEMIES = 10

# Bonuses setup
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)
bonuses = []

score = 0
max_score = 42
enemy_score = 0
win = False
game_over = False

### Game loop ###

# TODO: more meanies, faster move
# TODO: animate sprites

is_working = True
while is_working:
    if game_over:
        won_lost()

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY and len(enemies) < MAX_ENEMIES:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

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
    player.blit(main_surface)

    show_score()

    # Process enemies

    for enemy in enemies:
        # Turn to the first bonus in the view field
        # Over 2/3: meanies go to player
        if score > max_score / 3 * 2 and enemy.sees(player):
            enemy.turn_to(player)
        # Over 1/3: meanies go to bonuses
        elif score > max_score / 3:
            for bonus in bonuses:
                if enemy.sees(bonus):
                    enemy.turn_to(bonus)
                    break
                           
        enemy.move()

        enemy.blit(main_surface)

        if enemy.get_right() < 0 or enemy.get_bottom() < 0 or enemy.get_left() > width or enemy.get_top() > height:
            enemies.pop(enemies.index(enemy))
        # If the same enemy collides both with the left border and the player
        elif player.collides(enemy):
            # print(f'Player collides with {enemy.get_left()}, {enemy.get_top()}')
            enemies.pop(enemies.index(enemy))
            score -= 1
            if score < 0:
                game_over = True
                score = 0
                

    # Process bonuses

    for bonus in bonuses:
        bonus.move()

        bonus.blit(main_surface)

        if bonus.get_right() < 0 or bonus.get_bottom() < 0 or bonus.get_left() > width or bonus.get_top() > height:
            bonuses.pop(bonuses.index(bonus))

        elif player.collides(bonus):
            bonuses.pop(bonuses.index(bonus))
            score += 1
            CREATE_ENEMY_INTERVAL -= CREATE_ENEMY_STEP
            if CREATE_ENEMY_INTERVAL <= 600:
                CREATE_ENEMY_INTERVAL = 600
            pygame.time.set_timer(CREATE_ENEMY, CREATE_ENEMY_INTERVAL)

            if score >= max_score:
                win = True
                game_over = True

        else:
            for enemy in enemies:
                if bonus.collides(enemy):
                    if bonus in bonuses:
                        bonuses.pop(bonuses.index(bonus))
                        enemy_score += 1
                        if enemy_score >= max_score:
                            show_score()
                            game_over = True

    # Process keys

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_DOWN] and player.get_bottom() < height:
         player.speedY = player.speed
    elif pressed_keys[K_UP] and player.get_top() > 0:
         player.speedY = -player.speed

    if pressed_keys[K_LEFT] and player.get_left() > 0:
         player.speedX = -player.speed
    elif pressed_keys[K_RIGHT] and player.get_right() < width:
         player.speedX = player.speed
    player.move()
    player.stop()

    # Redraw the game
    pygame.display.flip()

