# Date: 03/05/2023 (last updated)
# Name: Martin Jimenez

from cmu_graphics import *
from random import *
from collections import deque

app.stepsPerSecond = 10
isPaused = False

grid = [
    [1] * 20,
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] + [0] * 18 + [1],
    [1] * 20]

for x in range(20):
    Line(20 * x, 0, 20 * x, 400, lineWidth=1)
for y in range(20):
    Line(0, 20 * y, 400, 20 * y, lineWidth=1)

border = Polygon(0, 0, 400, 0, 400, 400, 0, 400, 0, 20, 20, 20, 20, 380, 380, 380, 380, 20, 0, 20)
score = Label(1, 50, 10, fill='white')
path = []

snakeHead = Rect(40, 20, 20, 20, fill='blue', border='black', borderWidth=1)
snakeBody = [Rect(20, 20, 20, 20, fill='green', border='black', borderWidth=1)]
appleSeed = []

# high score: [(200, 20), (340, 20), (120, 260), (60, 240), (340, 200), (340, 200), (200, 20), (140, 220), (40, 20), (220, 20), (120, 300), (200, 200), (260, 120), (160, 200), (20, 260), (340, 120), (100, 340), (20, 60), (320, 340), (320, 340), (60, 240), (120, 220), (100, 320), (20, 220), (60, 140), (140, 320), (100, 220), (320, 140), (340, 180), (140, 200), (60, 300), (60, 300), (180, 300), (340, 120), (140, 220), (140, 220), (320, 180), (240, 100), (320, 40), (220, 60), (100, 20), (160, 220), (180, 180), (340, 80), (60, 20), (280, 320), (280, 320), (280, 80), (220, 160), (100, 140), (100, 20), (200, 100), (220, 280), (80, 140), (160, 320), (20, 80), (120, 40), (300, 100), (240, 320), (200, 140), (200, 140), (220, 60), (260, 120), (260, 120), (280, 100), (140, 20), (120, 40), (340, 80), (340, 80), (180, 140), (240, 100), (180, 280), (180, 280), (20, 220), (180, 220), (140, 60), (140, 60), (160, 240), (320, 40), (180, 320), (60, 20), (320, 340), (320, 340), (20, 80), (160, 300), (100, 60), (40, 300), (100, 80), (120, 100), (320, 100), (80, 180), (80, 180), (180, 140), (180, 140), (340, 60), (80, 220), (160, 340), (160, 340), (160, 340), (20, 200), (320, 20), (320, 20), (280, 120), (280, 60), (80, 40), (280, 80), (120, 100), (80, 300), (60, 280), (320, 280), (100, 340), (180, 220), (180, 220), (160, 20), (160, 20), (220, 320), (80, 40), (180, 340), (180, 340), (160, 120), (20, 200), (140, 140), (20, 180), (220, 40), (220, 40), (300, 120), (40, 220), (40, 220), (40, 220), (40, 220), (280, 320), (120, 120), (120, 120), (20, 40), (160, 240), (160, 240), (160, 240), (100, 140), (300, 280), (300, 280), (120, 300), (20, 300), (40, 180), (40, 180), (140, 20), (140, 20), (140, 20), (240, 300), (120, 220), (120, 220), (120, 220), (120, 220), (260, 340), (180, 340), (180, 340), (180, 340), (100, 20), (340, 120), (220, 260), (220, 260), (40, 40), (40, 40), (240, 320), (60, 260), (140, 200), (20, 40), (20, 40), (340, 300), (280, 320), (180, 340), (180, 300), (180, 300), (140, 320), (20, 300), (140, 280), (60, 340), (180, 280), (180, 280), (180, 280), (180, 280), (180, 280), (60, 20), (60, 20), (60, 20), (60, 20), (340, 20), (160, 80), (160, 80), (180, 280), (60, 320), (260, 60), (260, 60), (100, 60), (100, 60), (300, 100), (300, 100), (320, 100), (320, 100), (320, 100), (320, 100), (320, 100), (60, 120), (60, 120), (40, 40), (200, 100), (260, 180), (260, 180), (20, 120), (20, 120), (20, 120), (340, 80), (40, 20), (160, 340), (160, 340), (160, 340), (60, 280), (320, 200), (300, 280), (300, 280), (300, 280), (280, 260), (280, 260), (280, 260), (200, 300), (80, 320), (80, 320), (80, 240), (40, 280), (40, 280), (40, 280), (180, 340), (120, 320), (120, 320), (120, 80), (20, 20), (20, 20), (140, 300), (140, 300), (140, 40), (300, 40), (300, 40), (300, 40), (160, 20), (120, 40), (120, 40), (340, 340), (340, 340), (340, 340), (280, 340), (280, 340), (80, 20), (260, 20), (260, 20), (340, 60), (40, 260), (40, 260), (60, 320), (160, 40), (280, 20), (280, 20), (280, 20), (140, 260), (200, 240), (200, 240), (220, 220), (220, 220), (80, 80), (80, 80), (80, 80), (80, 80), (80, 80), (80, 80), (180, 240), (180, 240), (140, 140), (140, 140), (140, 140), (160, 260), (160, 260), (160, 260), (160, 260), (160, 260), (340, 20), (340, 20), (340, 20), (340, 20), (160, 60), (160, 60), (160, 60), (280, 120), (120, 300), (100, 300), (140, 240), (80, 40), (80, 40), (80, 40), (80, 40), (80, 40), (180, 40), (40, 160), (40, 160), (40, 120), (40, 120), (80, 20), (80, 20), (80, 20), (80, 20), (80, 20), (100, 40), (100, 40), (100, 40), (240, 40), (240, 40), (240, 40), (140, 20), (140, 20), (20, 40), (40, 120), (40, 120), (40, 120), (40, 120), (40, 120), (40, 120), (40, 240), (200, 340), (200, 340), (200, 340), (60, 300), (60, 300), (60, 300), (60, 300), (60, 300), (60, 300), (60, 300), (60, 300), (60, 300), (60, 300), (60, 300), (60, 300), (60, 300), (60, 300), (320, 220), (320, 220), (320, 220), (320, 220), (240, 200), (240, 200), (240, 200), (240, 200), (240, 200), (240, 200), (240, 200), (240, 200), (240, 200), (220, 260), (220, 260), (220, 260), (220, 260), (60, 180), (60, 180), (60, 180), (60, 180), (60, 120), (60, 120), (60, 120), (100, 340), (100, 340), (100, 340), (200, 300), (200, 300), (200, 300), (200, 300), (340, 260), (80, 300), (80, 300), (80, 300), (80, 300), (280, 340), (280, 340), (20, 240), (60, 320), (60, 320), (300, 240), (300, 240), (340, 220), (340, 220), (340, 260), (340, 260), (120, 240), (120, 240), (120, 240), (120, 240), (120, 240), (220, 260), (60, 40), (300, 220), (300, 220), (140, 200), (140, 200), (140, 200), (280, 20), (20, 60), (320, 320), (320, 320), (320, 320), (320, 320), (320, 320), (320, 320), (320, 320), (320, 320), (320, 320), (320, 320), (320, 320), (320, 320), (320, 320), (320, 320), (260, 300), (260, 300), (260, 300), (260, 300), (340, 320), (340, 320), (340, 320), (340, 320), (340, 320), (200, 340), (200, 340), (200, 340), (200, 340), (200, 340), (200, 340), (100, 320), (100, 320), (100, 320), (80, 280), (20, 120), (100, 280), (100, 280), (120, 20), (20, 20), (20, 20), (240, 300), (240, 300), (40, 60), (180, 340), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (80, 320), (120, 280), (120, 280), (120, 280), (120, 280), (20, 140), (20, 140), (200, 340), (200, 340), (200, 340), (200, 340), (200, 280), (200, 280), (320, 340), (320, 340), (320, 340), (320, 340), (320, 340), (320, 340), (320, 340), (320, 340), (320, 340), (320, 340), (320, 340), (340, 340), (340, 340), (40, 340), (40, 340), (40, 340), (40, 340), (40, 340), (40, 340), (40, 340), (40, 340), (40, 340), (260, 280), (260, 280), (260, 280), (260, 280), (260, 280), (220, 240), (220, 240), (220, 240), (220, 240), (220, 240), (280, 340), (220, 200), (220, 200), (220, 200), (220, 200), (220, 200), (100, 240), (100, 240), (100, 240), (100, 240), (160, 240), (160, 240), (160, 240), (160, 240), (160, 240), (160, 240), (160, 240), (160, 240), (160, 240), (340, 240), (340, 240), (340, 240), (340, 240), (340, 240), (340, 240), (340, 240), (340, 240), (280, 300), (280, 300), (160, 180), (160, 180), (160, 180), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (80, 160), (120, 240), (120, 240), (120, 240), (120, 240), (120, 240), (120, 240), (120, 240), (120, 240), (120, 240), (120, 240), (120, 240), (120, 240), (120, 240), (120, 240), (120, 240), (100, 240), (100, 240), (100, 240), (100, 240), (100, 240), (100, 240), (100, 240), (100, 240), (100, 240), (100, 240), (80, 300), (60, 280), (60, 280), (60, 280), (60, 280), (120, 280), (140, 160), (140, 160), (140, 160), (140, 160), (140, 160), (140, 160), (140, 160), (140, 160), (140, 160), (140, 160), (140, 160), (140, 160), (20, 100), (20, 100), (20, 100), (20, 100), (140, 220), (140, 220), (140, 220), (140, 220), (140, 220), (140, 220), (140, 220), (140, 220), (140, 220), (140, 220), (40, 280), (40, 280), (40, 280), (40, 280), (40, 280), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (160, 300), (160, 300), (160, 300), (160, 300), (20, 240), (20, 240), (20, 240), (20, 240), (20, 240), (260, 320), (260, 320), (260, 320), (60, 320), (60, 320), (60, 320), (240, 300), (240, 300), (240, 300), (220, 280), (220, 280), (220, 280), (220, 280), (220, 280), (120, 280), (120, 280), (120, 280), (120, 280), (120, 280), (120, 280), (120, 280), (120, 280), (120, 280), (120, 280), (120, 280), (120, 280), (300, 300), (300, 300), (300, 300), (300, 300), (300, 300), (300, 300), (300, 300), (300, 300), (260, 300), (260, 300), (260, 300), (260, 300), (320, 280), (320, 280), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (140, 320), (80, 260), (80, 260), (80, 260), (80, 260), (80, 260), (80, 260), (80, 260), (80, 260), (80, 260), (80, 260), (80, 260), (80, 260), (80, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (20, 260), (200, 340), (80, 340), (80, 340), (80, 340), (80, 340), (80, 340), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (100, 260), (40, 280), (40, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (60, 280), (80, 280), (40, 300), (40, 300), (40, 300), (40, 300), (40, 300), (40, 300), (40, 300), (40, 300), (220, 300), (220, 300), (220, 300), (220, 300), (220, 300), (220, 300), (220, 300), (220, 300), (180, 280), (180, 280), (180, 280), (180, 280), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (140, 300), (120, 320), (120, 320), (120, 320), (120, 320), (120, 320), (120, 320), (120, 320), (120, 320), (120, 320), (120, 320), (200, 340), (200, 340), (240, 340), (100, 260), (100, 260), (100, 260), (280, 320), (280, 320), (280, 320), (280, 320), (280, 320), (280, 320), (280, 320), (280, 320), (280, 320), (280, 320), (280, 320), (280, 320), (40, 320), (40, 320), (40, 320), (40, 320), (40, 320), (40, 320), (40, 320), (40, 320), (40, 220), (40, 220), (40, 220), (40, 220), (40, 220), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (120, 340), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 260), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (40, 180), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (60, 200), (80, 280), (80, 280), (80, 280), (80, 280), (80, 280), (80, 220), (80, 220), (80, 220), (80, 220), (80, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 220), (20, 180), (20, 180), (20, 180), (20, 180), (20, 180), (20, 180), (40, 280), (40, 280), (40, 280), (40, 280), (40, 280), (40, 280), (40, 280), (40, 280), (40, 280), (40, 280), (120, 220), (120, 220), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (60, 240), (40, 200), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220), (60, 220)]

#appleSeed = []
#snakeHead = Rect(, , 20, 20, fill='blue', border='black', borderWidth=1)
#snakeBody = []
#for body in snakeBody:
#    body.fill = 'green'
#    body.border = 'black'
#    body.borderWidth = 1

apple = Rect(200, 20, 20, 20, fill='red', border='black', borderWidth=1)
if appleSeed:
    apple.left = appleSeed[len(snakeBody) - 1][0]
    apple.top = appleSeed[len(snakeBody) - 1][1]
    score.value = len(snakeBody)

newAppleSeed = [(apple.left, apple.top)]

snakeHead.direction = 'right'


def gameOver():
    Label('GAME OVER', 200, 200, size=50, fill='red')
    print('Apple seed:', newAppleSeed)
    print('Snake head:', snakeHead)
    print('Snake body:', snakeBody)
    app.stop()


def dfs(grid, start, goal):
    visited = set()
    stack = [start]
    parentMap = {}
    rows, cols, = len(grid), len(grid[0])

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)

            x, y = node[0], node[1]

            if ((x > 0) and (x < rows - 1) and (y > 0) and (y < cols - 1) and (grid[x][y]) == goal):
                return (x, y), parentMap

            if (x > 0) and (grid[x - 1][y] not in (1, 2, 3)) and ((x - 1, y) not in visited):
                stack.append((x - 1, y))
                parentMap[(x - 1, y)] = ((x, y), 'up')
            if (x < rows - 1) and (grid[x + 1][y] not in (1, 2, 3)) and ((x + 1, y) not in visited):
                stack.append((x + 1, y))
                parentMap[(x + 1, y)] = ((x, y), 'down')
            if (y > 0) and (grid[x][y - 1] not in (1, 2, 3)) and ((x, y - 1) not in visited):
                stack.append((x, y - 1))
                parentMap[(x, y - 1)] = ((x, y), 'left')
            if (y < cols - 1) and (grid[x][y + 1] not in (1, 2, 3)) and ((x, y + 1) not in visited):
                stack.append((x, y + 1))
                parentMap[(x, y + 1)] = ((x, y), 'right')

    return None, None


def bfs(grid, start, goal):
    visited = set()
    dq = deque([start])
    parentMap = {}
    rows, cols, = len(grid), len(grid[0])

    while dq:
        node = dq.pop()
        if node not in visited:
            visited.add(node)

            x, y = node[0], node[1]

            if ((x > 0) and (x < rows - 1) and (y > 0) and (y < cols - 1) and (grid[x][y]) == goal):
                return (x, y), parentMap

            if (x > 0) and (grid[x - 1][y] not in (1, 2)) and ((x - 1, y) not in visited):
                dq.appendleft((x - 1, y))
                parentMap[(x - 1, y)] = ((x, y), 'up')
            if (x < rows - 1) and (grid[x + 1][y] not in (1, 2)) and ((x + 1, y) not in visited):
                dq.appendleft((x + 1, y))
                parentMap[(x + 1, y)] = ((x, y), 'down')
            if (y > 0) and (grid[x][y - 1] not in (1, 2)) and ((x, y - 1) not in visited):
                dq.appendleft((x, y - 1))
                parentMap[(x, y - 1)] = ((x, y), 'left')
            if (y < cols - 1) and (grid[x][y + 1] not in (1, 2)) and ((x, y + 1) not in visited):
                dq.appendleft((x, y + 1))
                parentMap[(x, y + 1)] = ((x, y), 'right')

    return None, None


def findPath(goal, start, parentMap):
    curr = goal
    path = []
    while curr != start:
        curr, direction = parentMap[curr]
        path.append(direction)
    return path


def snakePath(path, goal):
    global isPaused

    tail = False
    if not path:
        start = int(snakeHead.top / 20), int(snakeHead.left / 20)
        xy, parentMap = bfs(grid, start, goal)
        if xy is not None:
            path = findPath(xy, start, parentMap)
            path.reverse()

            newGrid = grid.copy()
            for i in range(len(newGrid)):
                newGrid[i] = grid[i].copy()

            if len(path) < len(snakeBody):
                print(path)
                changeX = int(snakeHead.left/20)
                changeY = int(snakeHead.top/20)

                for i in range(len(path)):
                    p = path[i]

                    if i == len(path) - 1:
                        pass
                    else:
                        if p == 'left':
                            changeX -= 1
                        elif p == 'right':
                            changeX += 1
                        elif p == 'up':
                            changeY -= 1
                        elif p == 'down':
                            changeY += 1

                        print(changeX, changeY)
                        newGrid[changeY][changeX] = 2

                for body in snakeBody:
                    if snakeBody.index(body) < len(path) - 1:
                        newGrid[int(body.top/20)][int(body.left/20)] = 0
                    else:
                        newGrid[int(body.top / 20)][int(body.left / 20)] = 5
                        break

                for g in newGrid:
                    print(g)

                fStart = int(apple.top / 20), int(apple.left / 20)
                goal = 5
                xy, parentMap = dfs(newGrid, fStart, goal)
                if xy is not None:
                    print('FOUND TAIL')
                else:
                    print('COULD NOT FIND TAIL')
                    tail = True
        else:
            tail = True

        if tail:
            print('Couldnt find goal', score.value)
            highPath = []
            for body in snakeBody:
                grid[int(body.top / 20)][int(body.left / 20)] = 5
                xy, parentMap = dfs(grid, start, 5)

                if xy is not None:
                    path = findPath(xy, start, parentMap)
                    path.reverse()
                    if path:
                        path.pop(-1)

                    if len(path) >= snakeBody.index(body) + 1:
                        print('Option', snakeBody.index(body), 'taken with', len(path), 'directions')
                        break
                    else:
                        print('Rejected option', snakeBody.index(body), 'with', len(path), 'directions')
                        if len(path) > len(highPath):
                            highPath = path

                if snakeBody.index(body) == len(snakeBody) - 1:
                    path = highPath
                    print('Best option chosen with', len(path), 'directions')
                    break

                grid[int(body.top / 20)][int(body.left / 20)] = 1

            for g in grid:
                print(g)

    return path


def genApple(apple, grid):
    global appleSeed

    if appleSeed:
        try:
            apple.left = appleSeed[len(snakeBody) - 1][0]
            apple.top = appleSeed[len(snakeBody) - 1][1]
        except:
            appleSeed = []
            genApple(apple, grid)
    else:
        apple.left = randrange(0, 17) * 20 + 20
        apple.top = randrange(0, 17) * 20 + 20

    if snakeHead.hits(apple.centerX, apple.centerY):
        print('Apple spawned on head', score.value)
        if appleSeed:
            appleSeed.pop(len(snakeBody) - 1)
        genApple(apple, grid)

    for body in snakeBody:
        if body.hits(apple.centerX, apple.centerY):
            print('Apple spawned on body', score.value)
            if appleSeed:
                appleSeed.pop(len(snakeBody) - 1)
            genApple(apple, grid)

    newApple = (apple.left, apple.top)
    newAppleSeed.append(newApple)


def onKeyPress(key):
    global isPaused

    if key == 'left':
        if app.stepsPerSecond == 1:
            print('Cannot lower speed past', app.stepsPerSecond)
        else:
            app.stepsPerSecond -= 1
            print('Lowered speed', app.stepsPerSecond)

    if key == 'right':
        app.stepsPerSecond += 1
        print('Increased speed', app.stepsPerSecond)

    if key == 'space':
        if isPaused:
            isPaused = False
        else:
            isPaused = True
            print('Paused the game')

    if key == 'G':
        print('Current grid:')
        for g in grid:
            print(g)

    if key == 'E':
        print('Terminated game early')
        gameOver()


def onStep():
    global path
    global snakeBody
    global isPaused

    if isPaused:
        return

    if border.hits(snakeHead.centerX, snakeHead.centerY):
        gameOver()
        return
    for body in snakeBody:
        if body.hits(snakeHead.centerX, snakeHead.centerY):
            gameOver()
            return

    snakeBody.append(Rect(snakeHead.left, snakeHead.top, 20, 20, fill='green', border='black', borderWidth=1))
    snakeBody[0].visible = False
    snakeBody.pop(0)

    if not path:
        for x in range(20):
            if x != 0 and x != 19:
                for y in range(20):
                    if y != 0 and y != 19:
                        if apple.hits(20 * x + 10, 20 * y + 10):
                            grid[y][x] = 9
                        elif border.hits(20 * x + 10, 20 * y + 10):
                            grid[y][x] = 1
                        else:
                            grid[y][x] = 0
                        for body in snakeBody:
                            if body.hits(20 * x + 10, 20 * y + 10):
                                grid[y][x] = 1
                                break
                        if snakeHead.hits(20 * x + 10, 20 * y + 10):
                            grid[y][x] = 3

    path = snakePath(path, 9)
    try:
        snakeHead.direction = path[0]
        path.pop(0)
    except:
        pass

    if snakeHead.direction == 'right':
        snakeHead.centerX += 20
    if snakeHead.direction == 'left':
        snakeHead.centerX -= 20
    if snakeHead.direction == 'up':
        snakeHead.centerY -= 20
    if snakeHead.direction == 'down':
        snakeHead.centerY += 20

    if apple.hits(snakeHead.centerX, snakeHead.centerY):
        snakeBody.append(Rect(snakeBody[-1].left, snakeBody[-1].top, 20, 20, fill='green', border='black', borderWidth=1))
        score.value = len(snakeBody)
        genApple(apple, grid)

cmu_graphics.run()


'''
def snakePath(path, goal):
    global isPaused

    tail = False
    if not path:
        start = int(snakeHead.top / 20), int(snakeHead.left / 20)
        xy, parentMap = bfs(grid, start, goal)
        if xy is not None:
            path = findPath(xy, start, parentMap)
            path.reverse()
            print(path)
            if len(path) < len(snakeBody):
                changeX = int(snakeHead.left/20)
                changeY = int(snakeHead.top/20)

                for i in range(len(path)):
                    p = path[i]

                    if i == len(path) - 1:
                        pass
                    else:
                        if p == 'left':
                            changeX -= 1
                        elif p == 'right':
                            changeX += 1
                        elif p == 'up':
                            changeY -= 1
                        elif p == 'down':
                            changeY += 1

                        print(changeX, changeY)
                        grid[changeY][changeX] = 2

                for body in snakeBody:
                    if snakeBody.index(body) < len(path):
                        grid[int(body.top/20)][int(body.left/20)] = 0

                for g in grid:
                    print(g)

                start = int(snakeHead.top / 20), int(snakeHead.left / 20)
                xy, parentMap = bfs(grid, start, goal)
                if xy is not None:
                    pass
                else:
                    tail = True
        else:
            tail = True

        if tail:
            print('Couldnt find goal', score.value)
            highPath = []
            for body in snakeBody:
                grid[int(body.top / 20)][int(body.left / 20)] = 5
                xy, parentMap = dfs(grid, start, 5)

                if xy is not None:
                    path = findPath(xy, start, parentMap)
                    path.reverse()

                    if len(path) > snakeBody.index(body):
                        print('Option', snakeBody.index(body), 'taken with', len(path), 'directions')
                        break
                    else:
                        print('Rejected option', snakeBody.index(body), 'with', len(path), 'directions')
                        if len(path) > len(highPath):
                            highPath = path

                if snakeBody.index(body) == len(snakeBody) - 1:
                    path = highPath
                    print('Best option chosen with', len(path), 'directions')
                    break

                grid[int(body.top / 20)][int(body.left / 20)] = 1

            for g in grid:
                print(g)

    return path
'''
