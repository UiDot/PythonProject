import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Избегай столкновения")
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

player_size = 50
player_x = 375
player_y = 275
player_speed = 5

enemy_width = 60
enemy_height = 40
enemy_x = random.randint(0, 800 - enemy_width)
enemy_y = random.randint(0, 600 - enemy_height)
enemy_speed_x = random.choice([-5, 5])
enemy_speed_y = random.choice([-5, 5])

clock = pygame.time.Clock()
FPS = 75

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + player_size < 800:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y + player_size < 600:
        player_y += player_speed

    enemy_x += enemy_speed_x
    enemy_y += enemy_speed_y

    if enemy_x <= 0 or enemy_x+enemy_width >= 800:
        enemy_speed_x = -enemy_speed_x
    if enemy_y <= 0 or enemy_y+enemy_height >= 600:
        enemy_speed_y = -enemy_speed_y

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)

    if player_rect.colliderect(enemy_rect):
        print('Вы проиграли!')
        pygame.quit()
        sys.exit()

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player_rect)
    pygame.draw.rect(screen, RED, enemy_rect)
    pygame.display.flip()

    clock.tick(FPS)
