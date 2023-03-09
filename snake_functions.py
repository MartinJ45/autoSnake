from cmu_graphics import *
from random import *


class Snake:
    def __init__(self, left, top, size):
        self.left = left
        self.top = top
        self.size = size

        self.length = 0
        self.direction = 'right'

        self.snake_head = Rect(self.left, self.top, self.size, self.size, fill='blue', border='black', borderWidth=1)
        self.snake_body = []

    def get_snake_head(self):
        return self.snake_head

    def get_snake_body(self):
        return self.snake_body

    def set_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.snake_body:
            self.snake_body.append(Rect(self.left, self.top, self.size, self.size, fill='green', border='black', borderWidth=1))
            self.snake_body[0].visible = False
            self.snake_body.pop(0)

        if self.direction == 'up':
            self.snake_head.centerY -= self.size
        if self.direction == 'down':
            self.snake_head.centerY += self.size
        if self.direction == 'left':
            self.snake_head.centerX -= self.size
        if self.direction == 'right':
            self.snake_head.centerX += self.size

        self.left = self.snake_head.left
        self.top = self.snake_head.top

    def add_body(self):
        if len(self.snake_body) == 0:
            self.snake_body.insert(0, Rect(self.left, self.top, self.size, self.size, fill='green', border='black',borderWidth=1))
        else:
            self.snake_body.insert(0, Rect(self.snake_body[0].left, self.snake_body[0].top, self.size, self.size, fill='green', border='black', borderWidth=1))

    def is_dead(self):
        if int(self.left/self.size) in (0, self.size-1) or int(self.top/self.size) in (0, self.size-1):
            return True

        if len(self.snake_body) <= 1:
            return False

        for body in self.snake_body:
            if body.hits(self.snake_head.centerX, self.snake_head.centerY):
                return True

        return False


class Apple:
    def __init__(self, left, top, size):
        self.left = left
        self.top = top
        self.size = size

        self.apple = Rect(self.left, self.top, self.size, self.size, fill='red', border='black', borderWidth=1)

    def get_apple(self):
        return self.apple

    def gen_apple(self, snake_head, snake_body):
        self.left = randrange(1, self.size-1) * self.size
        self.top = randrange(1, self.size-1) * self.size
        self.apple.left = self.left
        self.apple.top = self.top

        for body in snake_body:
            if body.hits(self.apple.centerX, self.apple.centerY):
                self.gen_apple(snake_head, snake_body)

        if snake_head.hits(self.apple.centerX, self.apple.centerY):
            self.gen_apple(snake_head, snake_body)
