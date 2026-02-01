import pygame
import random
import sys
import time

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JUMP")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Звуки
#aaaajump_sound = pygame.mixer.Sound("music/mixkit-losing-drums-2023.wav")

# Игрок
player = pygame.Rect(200, 500, 50, 50)
player_velocity = 0
gravity = 0.5

# Платформы
platforms = [pygame.Rect(random.randint(0, WIDTH - 100), i * 100, 100, 10) for i in range(6)]

# Скорость платформ
platform_speed = 2

# Счет
score = 0
font = pygame.font.SysFont("Arial", 24)


# Экран старта
def show_start_screen():
    screen.fill(WHITE)
    title_font = pygame.font.SysFont("Arial", 36, bold=True)
    title_text = title_font.render("Jump", True, BLUE)
    instructions = font.render("Press any key to start", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


# Основной цикл
clock = pygame.time.Clock()
running = True

# Показ экрана старта
show_start_screen()

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
        player.x += 5

    # Гравитация и движение игрока
    player_velocity += gravity
    player.y += player_velocity

    # Если игрок выходит за пределы экрана (падает вниз)
    if player.y > HEIGHT:
        running = False  # Завершаем игру

    # Если игрок прыгает на платформу
    for platform in platforms:
        if player.colliderect(platform) and player_velocity > 0:
            player_velocity = -10
            jump_sound.play()
            break

    # Перемещение платформ вниз
    for platform in platforms:
        platform.y += platform_speed

        # Удаление платформ за пределами экрана и добавление новых
        if platform.y > HEIGHT:
            platforms.remove(platform)
            new_platform = pygame.Rect(random.randint(0, WIDTH - 100), -10, 100, 10)
            platforms.append(new_platform)
            score += 10  # Увеличиваем счет за каждую пройденную платформу

    # Увеличение сложности: ускоряем платформы с ростом счета
    platform_speed = 2 + score // 100

    # Отрисовка игрока и платформ
    pygame.draw.rect(screen, BLUE, player)
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    # Отрисовка счета
    score_text = font.render(f"Счет: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

