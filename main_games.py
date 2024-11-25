import pygame
import sys
import subprocess
import os

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT = 100, 100

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Меню игр")

# Шрифт
font = pygame.font.Font(None, 74)

# Загрузка и масштабирование изображений
def load_and_scale_image(path):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT))
    return image

# Загрузка изображений
images = {
    "  Пингпонг": pygame.image.load("pingpong.png"),
    "Змейка": pygame.image.load("snake.png"),
    "Тетрис": pygame.image.load("tetris.png"),
    "Выжить": pygame.image.load("war.png"),
}

# Кнопки
buttons = [
    {"text": "  Пингпонг", "action": "smallpingpong.py"},
    {"text": "Змейка", "action": "smallzmeika.py"},
    {"text": "Тетрис", "action": "smalltetris.py"},
    {"text": "Выжить", "action": "smallwar.py"},
    {"text": "Выход", "action": "exit"},
]

def draw_menu():
    screen.fill(BLACK)  # Изменяем цвет фона на чёрный
    y_offset = 100
    for index, button in enumerate(buttons):
        # Если кнопка "Выход", то текст будет красным
        if button["text"] == "Выход":
            text_color = RED
        else:
            text_color = WHITE
        
        text = font.render(button["text"], True, text_color)
        rect = text.get_rect(center=(WIDTH // 2, y_offset))
        screen.blit(text, rect)
        button["rect"] = rect  # Сохраняем прямоугольник для проверки кликов

        # Отображение изображения
        if button["text"] in images:
            image = images[button["text"]]
            image_rect = image.get_rect(center=(WIDTH // 2 - 150, y_offset))
            screen.blit(image, image_rect)

        y_offset += 100
    pygame.display.flip()


def main():
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левый клик мыши
                    mouse_pos = pygame.mouse.get_pos()
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["action"] == "exit":
                                pygame.quit()
                                sys.exit()
                            else:
                                if os.path.exists(button["action"]):
                                    subprocess.Popen(['python', button["action"]])
                                else:
                                    print(f"Файл {button['action']} не найден.")

        draw_menu()
        clock.tick(FPS)

if __name__ == "__main__":
    main()