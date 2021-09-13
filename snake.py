import pygame
from pygame.locals import*
import random
import time


SIZE = 30
bg_color = (12, 61, 61)


class Resources:
    def __init__(self) -> None:
        self.Sprites = {
            "apple": pygame.image.load("./resources/apple.png").convert(),
            "block": pygame.image.load("./resources/Rectangle.png").convert()}


class Apple:
    def __init__(self, parent_screen, resources: Resources):
        self.parent_screen = parent_screen
        self.food = resources.Sprites["apple"]
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.food, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 22) * SIZE
        self.y = random.randint(0, 12) * SIZE


class Snake:
    def __init__(self, parent_screen, length: int, resources: Resources):
        self.parent_screen = parent_screen
        self.block = resources.Sprites["block"]
        self.dir_up = 0
        self.dir_down = 1
        self.dir_left = 2
        self.dir_right = 3

        self.direction = self.dir_down
        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length

    def draw(self):
        self.parent_screen.fill(bg_color)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = self.dir_left

    def move_right(self):
        self.direction = self.dir_right

    def move_up(self):
        self.direction = self.dir_up

    def move_down(self):
        self.direction = self.dir_down

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == self.dir_left:
            self.x[0] -= SIZE

        if self.direction == self.dir_right:
            self.x[0] += SIZE

        if self.direction == self.dir_up:
            self.y[0] -= SIZE

        if self.direction == self.dir_down:
            self.y[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 500))
        self.resources = Resources()
        self.snake = Snake(self.surface, 1, self.resources)
        self.snake.draw()
        self.apple = Apple(self.surface, self.resources)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface, 1, self.resources)
        self.apple = Apple(self.surface, self.resources)

    def collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(
            f"SCORE: {self.snake.length*10}", True, (255, 255, 255))
        self.surface.blit(score, (800, 0))
        detail = font.render(
            "Eat fruit avoid collision avoid borders", True, (255, 255, 255))
        self.surface.blit(detail, (0, 0))

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.collision(
                self.snake.x[0],
                self.snake.y[0],
                self.apple.x,
                self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        for i in range(2, self.snake.length):
            if self.collision(
                    self.snake.x[0],
                    self.snake.y[0],
                    self.snake.x[i],
                    self.snake.y[i]):
                raise "unwanted collision"

        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 500):
            raise "border collide"

    def game_over(self):
        self.surface.fill(bg_color)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(
            f"Game is over! Your score is {self.snake.length*10}", True, (255, 255, 255))
        self.surface.blit(line1, (220, 200))
        line2 = font.render(
            "To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (220, 250))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.game_over()
                pause = True
                self.reset()
            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
