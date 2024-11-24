import pygame
import random
import sys

# Константы
WIDTH, HEIGHT = 800, 600
PLAYER_RADIUS = 15
ENEMY_SIZE = 20
ENEMY_SPAWN_RATE = 30  # каждые 30 кадров
SPEED = 5

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра на выживание")

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = SPEED
        self.dy = 0

    def move(self):
        self.x += self.dx
        self.y += self.dy

 # Проверка на границы окна
        if self.x - PLAYER_RADIUS < 0:
            self.x = PLAYER_RADIUS
            self.dx = -self.dx
        elif self.x + PLAYER_RADIUS > WIDTH:
            self.x = WIDTH - PLAYER_RADIUS
            self.dx = -self.dx

        if self.y - PLAYER_RADIUS < 0:
            self.y = PLAYER_RADIUS
            self.dy = -self.dy
        elif self.y + PLAYER_RADIUS > HEIGHT:
            self.y = HEIGHT - PLAYER_RADIUS
            self.dy = -self.dy

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), PLAYER_RADIUS)

class Enemy:
    def __init__(self):
        self.x = random.randint(ENEMY_SIZE, WIDTH - ENEMY_SIZE)
        self.y = random.randint(ENEMY_SIZE, HEIGHT - ENEMY_SIZE)

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, ENEMY_SIZE, ENEMY_SIZE))

class SurvivalGame:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.spawn_timer = 0

    def spawn_enemy(self):
        self.enemies.append(Enemy())

    def check_collisions(self):
        player_rect = pygame.Rect(self.player.x - PLAYER_RADIUS, self.player.y - PLAYER_RADIUS, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2)
        for enemy in self.enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, ENEMY_SIZE, ENEMY_SIZE)
            if player_rect.colliderect(enemy_rect):
                return True
        return False

    def play(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.player.dx = 0
                self.player.dy = -SPEED
            elif keys[pygame.K_DOWN]:
                self.player.dx = 0
                self.player.dy = SPEED
            elif keys[pygame.K_LEFT]:
                self.player.dx = -SPEED
                self.player.dy = 0
            elif keys[pygame.K_RIGHT]:
                self.player.dx = SPEED
                self.player.dy = 0

            self.player.move()

            if self.spawn_timer == ENEMY_SPAWN_RATE:
                self.spawn_enemy()
                self.spawn_timer = 0
            else:
                self.spawn_timer += 1

            if self.check_collisions():
                print("Game Over!")
                pygame.quit()
                sys.exit()

            screen.fill(WHITE)
            self.player.draw()
            for enemy in self.enemies:
                enemy.draw()
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = SurvivalGame()
    game.play()