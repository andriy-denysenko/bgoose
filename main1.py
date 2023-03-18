import pygame
from pygame. constants import QUIT

pygame.init()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

COLORS = WHITE, RED, GREEN, BLUE

screen = width, height = 800, 600

main_surface = pygame.display.set_mode(screen)
main_surface_color = (BLACK)

ball = pygame.Surface((20, 20))
ball_color_index = 0
ball_color = COLORS[ball_color_index]
ball.fill(ball_color)
ball_rect = ball.get_rect()
ball_speed = [-1, -1]

is_working = True
while is_working:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
    # It's cheaper to redraw the ball rectangle than the whole main surface
    # Erase the ball
    ball.fill(main_surface_color)
    main_surface.blit(ball, ball_rect)

    # Check for collision
    if ball_rect.left < 1 or ball_rect.right >= width:
        ball_speed[0] = - ball_speed[0]
        ball_color_index = ball_color_index + 1 if ball_color_index < 3 else 0
        ball_color = COLORS[ball_color_index]

    if ball_rect.top < 1 or ball_rect.bottom >= height:
        ball_speed[1] = - ball_speed[1]
        ball_color_index = ball_color_index + 1 if ball_color_index < 3 else 0
        ball_color = COLORS[ball_color_index]

    # Move the ball
    ball_rect = ball_rect.move(ball_speed)

    # Draw the ball
    ball.fill(ball_color)
    main_surface.blit(ball, ball_rect)

    # Redraw the game
    pygame.display.flip()

# System calls pygame.quit() itself
