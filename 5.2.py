import pygame

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 400, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Привет, я люблю питон")

# Определение цветов
SKY_BLUE = (135, 206, 235)   # Голубой для фона
BROWN = (139, 69, 19)        # Коричневый для досок
GRAY = (128, 128, 128)       # Серый для чередующихся досок

# Основной цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Заливка фона голубым (небо)
    window.fill(SKY_BLUE)

    # Параметры забора
    board_width = 20   # Ширина одной доски
    board_height = 150 # Высота одной доски
    gap = 10           # Расстояние между досками

    # Цикл для рисования чередующихся досок
    for i, x in enumerate(range(0, WIDTH, board_width + gap)):
        # Чередуем цвет: если i чётное, используем коричневый, если нечётное — серый
        color = BROWN if i % 2 == 0 else GRAY
        pygame.draw.rect(window, color, (x, HEIGHT - board_height - 50, board_width, board_height))

    # Обновление экрана
    pygame.display.flip()

pygame.quit()


