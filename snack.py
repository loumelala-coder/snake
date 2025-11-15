import pygame
import random
import sys
pygame.init()
WIDTH, HEIGHT = 300, 300
GRID_SIZE = 10
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self.snake_coords = [[14, 14]]
        self.apple_coords = [random.randint(0, GRID_WIDTH - 1) for _ in range(2)]
        self.vector = {
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0)
        }
        self.direction = self.vector[pygame.K_RIGHT]
        self.next_direction = self.direction
        self.game_over = False

    def set_apple(self):
        self.apple_coords = [random.randint(0, GRID_WIDTH - 1) for _ in range(2)]
        while self.apple_coords in self.snake_coords:
            self.apple_coords = [random.randint(0, GRID_WIDTH - 1) for _ in range(2)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in self.vector:
                    new_direction = self.vector[event.key]
                    if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
                        self.next_direction = new_direction

    def coord_check(self, coord):
        return coord % GRID_WIDTH
    def update(self):
        if self.game_over:
            return
        self.direction = self.next_direction
        x, y = self.snake_coords[0]
        dx, dy = self.direction
        x = self.coord_check(x + dx)
        y = self.coord_check(y + dy)
        if [x, y] in self.snake_coords:
            self.game_over = True
            return
        if x == self.apple_coords[0] and y == self.apple_coords[1]:
            self.set_apple()
        else:
            self.snake_coords.pop()
        self.snake_coords.insert(0, [x, y])
    def draw(self):
        self.screen.fill(BLACK)
        apple_rect = pygame.Rect(
            self.apple_coords[0] * GRID_SIZE,
            self.apple_coords[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(self.screen, RED, apple_rect)

        for segment in self.snake_coords:
            segment_rect = pygame.Rect(
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(self.screen, GREEN, segment_rect)
        if self.game_over:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)
        pygame.display.flip()
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
if __name__ == "__main__":
    game = Game()
    game.run()