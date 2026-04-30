import pygame
import sys
import random

# Initialize
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 800
BLOCK_SIZE = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("Arial", 25)


class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = (BLOCK_SIZE, 0)
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_dir):
        # Prevent reverse movement
        dx, dy = self.direction
        ndx, ndy = new_dir

        if (dx + ndx, dy + ndy) != (0, 0):
            self.direction = new_dir

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))

    def check_collision(self):
        head = self.body[0]

        # Wall collision
        if (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT
        ):
            return True

        # Self collision
        if head in self.body[1:]:
            return True

        return False


class Food:
    def __init__(self):
        self.position = self.spawn()

    def spawn(self):
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        return (x, y)

    def draw(self):
        pygame.draw.rect(screen, RED, (*self.position, BLOCK_SIZE, BLOCK_SIZE))


def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("Arial", size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)


def start_screen():
    while True:
        screen.fill(BLACK)
        draw_text("SNAKE GAME", 40, GREEN, WIDTH // 2, HEIGHT // 3)
        draw_text("Press SPACE to Start", 25, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Press ESC to Quit", 20, WHITE, WIDTH // 2, HEIGHT // 2 + 40)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def game_over_screen(score):
    while True:
        screen.fill(BLACK)
        draw_text("GAME OVER", 40, RED, WIDTH // 2, HEIGHT // 3)
        draw_text(f"Score: {score}", 30, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Press R to Restart", 25, WHITE, WIDTH // 2, HEIGHT // 2 + 40)
        draw_text("Press ESC to Quit", 20, WHITE, WIDTH // 2, HEIGHT // 2 + 80)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def game_loop():
    snake = Snake()
    food = Food()
    score = 0
    speed = 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -BLOCK_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, BLOCK_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-BLOCK_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((BLOCK_SIZE, 0))

        snake.move()

        # Check food collision
        if snake.body[0] == food.position:
            snake.grow = True
            food.position = food.spawn()
            score += 1
            speed += 0.5  # Increase difficulty

        # Check collisions
        if snake.check_collision():
            return score

        # Drawing
        screen.fill(BLACK)
        snake.draw()
        food.draw()

        # Score display
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(speed)


def main():
    while True:
        start_screen()
        score = game_loop()
        game_over_screen(score)


if __name__ == "__main__":
    main()