import pygame
import time
import random

# Константы
WIDTH, HEIGHT = 800, 600
SEGMENT_SIZE = 20
FPS = 10  # frames per second

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (0, SEGMENT_SIZE)  # Изначально движется вниз
        self.prev_positions = []  # Список для хранения предыдущих позиций

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Проверка на выход за границы и изменение направления
        if new_head[0] < 0:  # Выход налево
            new_head = (0, head_y)
            self.direction = (SEGMENT_SIZE, 0)  # Идем вправо
        elif new_head[0] >= WIDTH:  # Выход направо
            new_head = (WIDTH - SEGMENT_SIZE, head_y)
            self.direction = (-SEGMENT_SIZE, 0)  # Идем влево
        elif new_head[1] < 0:  # Выход вверх
            new_head = (head_x, 0)
            self.direction = (0, SEGMENT_SIZE)  # Идем вниз
        elif new_head[1] >= HEIGHT:  # Выход вниз
            new_head = (head_x, HEIGHT - SEGMENT_SIZE)
            self.direction = (0, -SEGMENT_SIZE)  # Идем вверх

        # Добавляем текущую позицию головы в список предыдущих позиций
        self.prev_positions.append(new_head)

        # Если список превышает длину тела змейки, удаляем старые позиции
        if len(self.prev_positions) > len(self.body):
            self.prev_positions.pop(0)

        self.body.insert(0, new_head)
        self.body.pop()  # Удаляем последний сегмент

    def change_direction(self, new_direction):
        # Запрещаем разворот на 180 градусов
        if (self.direction[0] * -1, self.direction[1] * -1) != new_direction:
            self.direction = new_direction

    def grow(self):
        # Добавляем новый сегмент в конец
        self.body.append(self.body[-1])

    def draw(self, surface):
        # Рисуем след
        for pos in self.prev_positions:
            pygame.draw.rect(surface, (0, 255, 0), (pos[0], pos[1], SEGMENT_SIZE, SEGMENT_SIZE))

        # Рисуем текущую змею
        for segment in self.body:
            pygame.draw.rect(surface, (0, 255, 0), (segment[0], segment[1], SEGMENT_SIZE, SEGMENT_SIZE))


class Gate:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, SEGMENT_SIZE * 3, SEGMENT_SIZE)  # Размер ворот

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)  # Рисуем ворота красным цветом


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.gates = self.create_gates(3)  # Создаем 3 ворот
        self.score = 0  # Начальный счет
        self.running = True
        self.paused = False  # Флаг для паузы

    def create_gates(self, count):
        gates = []
        for _ in range(count):
            x = random.randint(0, (WIDTH // SEGMENT_SIZE - 3)) * SEGMENT_SIZE
            y = random.randint(0, (HEIGHT // SEGMENT_SIZE - 1)) * SEGMENT_SIZE
            gates.append(Gate(x, y))
        return gates

    def check_gate_collision(self):
        head = self.snake.body[0]
        for gate in self.gates:
            if gate.rect.collidepoint(head):
                return gate
        return None

    def play(self):
        while self.running:
            self.handle_events()
            if not self.paused:  # Двигаем змею только если игра не на паузе
                self.snake.move()
                collided_gate = self.check_gate_collision()

                if collided_gate:
                    if (self.snake.direction[0] > 0 or self.snake.direction[1] > 0):
                        self.score += 1  # Увеличиваем счет
                    else:
                        self.snake.direction = (-self.snake.direction[0], -self.snake.direction[1])  # Меняем направление
                    self.gates.remove(collided_gate)  # Удаляем ворота после прохождения
                    if len(self.gates) == 0:  # Если все ворота пройдены
                        self.running = False  # Конец игры

            self.draw()
            self.clock.tick(FPS)
            time.sleep(0.1)  # Задержка для управления скоростью игры

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -SEGMENT_SIZE))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, SEGMENT_SIZE))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-SEGMENT_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((SEGMENT_SIZE, 0))
                elif event.key == pygame.K_SPACE:  # Проверка на пробел
                    self.paused = not self.paused  # Переключаем состояние паузы

    def draw(self):
        self.screen.fill((0, 0, 0))  # Чёрный фон
        self.snake.draw(self.screen)
        for gate in self.gates:
            gate.draw(self.screen)
        self.display_score()  # Отображаем счет
        pygame.display.flip()  # Обновляем экран

    def display_score(self):
        font = pygame.font.SysFont(None, 35)
        score_surface = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))  # Отображаем счет в верхнем левом углу


# Пример запуска игры
if __name__ == "__main__":  # Исправлено с name на __name__
    game = SnakeGame()
    game.play()
    pygame.quit()