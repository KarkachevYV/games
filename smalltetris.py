import pygame
import random

# Определяем размеры окна
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30

# Определяем цвета
COLORS = {
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
}

class TetrisPiece:
    def __init__(self):
        self.shape = [[1, 1, 1], [0, 1, 0]]  # Пример фигуры
        self.color = random.choice(list(COLORS.values()))  # Случайный цвет
        self.x = 4  # Начальная позиция по x
        self.y = 0  # Начальная позиция по y

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]  # Поворот фигуры

class TetrisGame:
    def __init__(self):
        self.current_piece = TetrisPiece()
        self.board = [[0 for _ in range(WINDOW_WIDTH // BLOCK_SIZE)] for _ in range(WINDOW_HEIGHT // BLOCK_SIZE)]
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fall_time = 0
        self.fall_speed = 500  # Скорость падения в миллисекундах
        self.last_rotate_time = 0  # Время последнего вращения
        self.rotate_delay = 200  # Задержка между вращениями в миллисекундах

    def draw_board(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                color = COLORS['black'] if self.board[y][x] == 0 else self.board[y][x]
                pygame.draw.rect(self.screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(self.screen, COLORS['black'], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        # Отрисовка текущей фигуры
        for y, row in enumerate(self.current_piece.shape):
            for x, value in enumerate(row):
                if value:
                    pygame.draw.rect(self.screen, self.current_piece.color,
                                     ((self.current_piece.x + x) * BLOCK_SIZE, (self.current_piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    def check_collision(self, dx=0, dy=0):
        for y, row in enumerate(self.current_piece.shape):
            for x, value in enumerate(row):
                if value:
                    new_x = self.current_piece.x + x + dx
                    new_y = self.current_piece.y + y + dy
                    if new_x < 0 or new_x >= len(self.board[0]) or new_y >= len(self.board) or self.board[new_y][new_x]:
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, value in enumerate(row):
                if value:
                    self.board[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color

    def remove_full_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_to_remove = len(self.board) - len(new_board)
        new_board = [[0 for _ in range(len(self.board[0]))] for _ in range(lines_to_remove)] + new_board
        self.board = new_board

    def drop_piece(self):
        if not self.check_collision(dy=1):
            self.current_piece.y += 1
        else:
            self.merge_piece()
            self.remove_full_lines()
            self.current_piece = TetrisPiece()
            if self.check_collision():
                self.running = False  # Игра окончена

    def handle_input(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_LEFT] and not self.check_collision(dx=-1):
            self.current_piece.x -= 1
        if keys[pygame.K_RIGHT] and not self.check_collision(dx=1):
            self.current_piece.x += 1
        if keys[pygame.K_DOWN]:
            self.drop_piece()  # Ускоренное падение
        if keys[pygame.K_UP] and current_time - self.last_rotate_time > self.rotate_delay:
            self.current_piece.rotate()
            if self.check_collision():
                self.current_piece.rotate()  # Возврат, если столкновение
            self.last_rotate_time = current_time

    def play(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_input()

            # Обновление времени падения
            self.fall_time += self.clock.tick(30)
            if self.fall_time > self.fall_speed:
                self.drop_piece()
                self.fall_time = 0

            self.screen.fill(COLORS['black'])
            self.draw_board()
            pygame.display.flip()

if __name__ == "__main__":
    game = TetrisGame()
    game.play()