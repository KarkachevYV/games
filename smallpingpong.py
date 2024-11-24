import pygame
import sys

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED_X = 3
BALL_SPEED_Y = 3

# Классы для ракетки и мяча
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, direction):
        if direction == "up" and self.rect.top > 0:
            self.rect.y -= PADDLE_SPEED
        elif direction == "down" and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PADDLE_SPEED

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Проверка столкновения с верхней и нижней границей
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1  # Изменяем направление движения по вертикали

# Основной класс игры
class PingPongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ping Pong Game")
        self.clock = pygame.time.Clock()
        self.paddle = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()
        self.font = pygame.font.SysFont(None, 55)
        self.score = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.paddle.move("up")
            if keys[pygame.K_DOWN]:
                self.paddle.move("down")

            self.ball.move()

            # Проверка столкновения мяча с ракеткой
            if self.ball.rect.colliderect(self.paddle.rect):
                self.ball.speed_x *= -1  # Отразить мяч
                self.score += 1  # Увеличить счет

            # Проверка выхода мяча за границы экрана
            if self.ball.rect.left <= 0:
                print(f"Game Over! Your score: {self.score}")
                pygame.quit()
                sys.exit()
            elif self.ball.rect.right >= SCREEN_WIDTH:
                self.ball.speed_x *= -1  # Отразить мяч, если он выходит с правой стороны

            self.screen.fill((0, 0, 0))  # Очистка экрана
            pygame.draw.rect(self.screen, (255, 255, 255), self.paddle.rect)  # Ракетка
            pygame.draw.ellipse(self.screen, (255, 0, 0), self.ball.rect)  # Мяч

            # Отображение счета
            score_surface = self.font.render(str(self.score), True, (255, 255, 255))
            self.screen.blit(score_surface, (SCREEN_WIDTH // 2, 20))

            pygame.display.flip()  # Обновление экрана
            self.clock.tick(60)  # Ограничение FPS

# Запуск игры
if __name__ == "__main__":
    game = PingPongGame()
    game.run()