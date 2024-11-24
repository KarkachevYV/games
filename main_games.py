import pygame
import sys
import subprocess
import os

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Меню игр")

# Шрифт
font = pygame.font.Font(None, 74)

# Кнопки
buttons = [
    {"text": "Пинг-понг", "action": "smallpingpong.py"},
    {"text": "Змейка", "action": "smallzmeika.py"},
    {"text": "Тетрис", "action": "smalltetris.py"},
    {"text": "Игра на выживыание", "action": "smallwar.py"},
    {"text": "Выход", "action": "exit"},
]

def draw_menu():
    screen.fill(WHITE)
    y_offset = 100
    for index, button in enumerate(buttons):
        text = font.render(button["text"], True, BLACK)
        rect = text.get_rect(center=(WIDTH // 2, y_offset))
        screen.blit(text, rect)
        button["rect"] = rect  # Сохраняем прямоугольник для проверки кликов
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