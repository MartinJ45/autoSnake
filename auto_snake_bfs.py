# Date: 03/08/2023 (last updated)
# Name: Martin Jimenez

# This snake game uses the cmu_graphics library
from cmu_graphics import *
from random import *
from collections import deque

# The default game speed is 10; this value can be changed by pressing the
# left and right arrow keys
app.stepsPerSecond = 10
isPaused = False
isPlaying = False

# Grabs size input
msg = 'Enter the board length (default 18 or press ENTER)'
size = app.getTextInput(msg)
while not size.isdigit() or int(size) % 2 != 0 or int(size) > 200 or int(size) < 4:
    if size == '':
        size = 18
        break
    if not size.isdigit():
        msg = 'Enter the board length (enter a digit)'
    if int(size) % 2 != 0:
        msg = 'Enter the board length (only evens)'
    if int(size) > 200:
        msg = 'Enter the board length (max size 200)'
    if int(size) < 4:
        msg = 'Enter the board length (min size 4)'

    size = app.getTextInput(msg)

size = int(size)
blockSize = 400 / (size + 2)

# This is the grid that the snake uses
# 0 represents open space
# 1 represents the border or the snake body
# 2 represents the path the snake plans to take towards the apple
# 3 represents the snake head
# 5 is a goal representing the end of the tail (used when it cannot locate the apple)
# 9 is a goal representing the apple
grid = [
    [1] * (size + 2)
]

for i in range(size):
    grid.append([1] + [0] * size + [1])
grid.append([1] * (size + 2))

# Draws the background grid
gridBackground = Group()
for x in range(size + 2):
    gridBackground.add(Line(blockSize * x, 0, blockSize * x, 400, lineWidth=1))
for y in range(size + 2):
    gridBackground.add(Line(0, blockSize * y, 400, blockSize * y, lineWidth=1))

# Draws the border and score
border = Polygon(
    0,
    0,
    400,
    0,
    400,
    400,
    0,
    400,
    0,
    blockSize,
    blockSize,
    blockSize,
    blockSize,
    400 - blockSize,
    400 - blockSize,
    400 - blockSize,
    400 - blockSize,
    blockSize,
    0,
    blockSize)
score = Label(1, 50, blockSize / 2, fill='white', size=blockSize)

path = []

# This is the default start
# Replace this section of code with what is printed when pressing SHIFT +
# 'I' to resume/replicate a game
appleSeed = [(200, blockSize)]
snakeHead = Rect(
    blockSize * 2,
    blockSize,
    blockSize,
    blockSize,
    fill='blue',
    border='black',
    borderWidth=1)
snakeBody = [
    Rect(
        blockSize,
        blockSize,
        blockSize,
        blockSize,
        fill='green',
        border='black',
        borderWidth=1)]
#

# Correctly draws the apple
apple = Rect(
    200,
    blockSize,
    blockSize,
    blockSize,
    fill='red',
    border='black',
    borderWidth=1)

if appleSeed and len(snakeBody) > 1:
    apple.left = appleSeed[len(snakeBody)][0]
    apple.top = appleSeed[len(snakeBody)][1]

score.value = len(snakeBody)

newAppleSeed = appleSeed.copy()

# Determines which way the snake will go; starts off going right
snakeHead.direction = 'right'
snakeHead.prevDirection = 'right'


# Stops the program when the snake loses, wins, or if the game is ended early
def gameOver():
    # The max value it can achieve is 324 in an 18 by 18 grid
    if score.value == pow(size, 2) - 1:
        Label('YOU WIN', 200, 200, size=50, fill='lime')
    else:
        Label('GAME OVER', 200, 200, size=50, fill='red')

    # Prints the seed of the game, so the game can be replicated
    print('Copy and paste this code to save/replicate where the snake left off')
    print('appleSeed =', newAppleSeed)
    # Prints the snake's head
    print(
        f'snakeHead = Rect({snakeHead.left}, {snakeHead.top}, {blockSize}, {blockSize}, fill=\'blue\', border=\'black\', borderWidth=1)')
    # Prints the snake's body
    print('snakeBody = [', end='')
    for body in snakeBody:
        if snakeBody.index(body) == len(snakeBody) - 1:
            end = ']'
        else:
            end = ','
        print(
            f'Rect({body.left}, {body.top}, {blockSize}, {blockSize}, fill=\'green\', border=\'black\', borderWidth=1)',
            end=end)
    app.stop()


# Uses depth first search to path find to the end of the tail in the most amount of moves as possible
# Results in coiling itself
def dfs(grid, start, goal, order='lr'):
    visited = set()
    stack = [start]
    parentMap = {}
    rows, cols, = len(grid), len(grid[0])

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)

            x, y = node[0], node[1]

            if ((x > 0) and (x < rows - 1) and (y > 0)
                    and (y < cols - 1) and (grid[x][y]) == goal):
                return (x, y), parentMap

            # Favors going left to right than up and down
            if order == 'lr':
                if (x > 0) and (grid[x - 1][y] not in (1, 2, 3)
                                ) and ((x - 1, y) not in visited):
                    stack.append((x - 1, y))
                    parentMap[(x - 1, y)] = ((x, y), 'up')
                if (x < rows -
                    1) and (grid[x +
                                 1][y] not in (1, 2, 3)) and ((x +
                                                               1, y) not in visited):
                    stack.append((x + 1, y))
                    parentMap[(x + 1, y)] = ((x, y), 'down')
                if (y > 0) and (grid[x][y - 1] not in (1, 2, 3)
                                ) and ((x, y - 1) not in visited):
                    stack.append((x, y - 1))
                    parentMap[(x, y - 1)] = ((x, y), 'left')
                if (y < cols -
                    1) and (grid[x][y +
                                    1] not in (1, 2, 3)) and ((x, y +
                                                               1) not in visited):
                    stack.append((x, y + 1))
                    parentMap[(x, y + 1)] = ((x, y), 'right')
            # Favors going up and down than left to right
            elif order == 'ud':
                if (y > 0) and (grid[x][y - 1] not in (1, 2, 3)
                                ) and ((x, y - 1) not in visited):
                    stack.append((x, y - 1))
                    parentMap[(x, y - 1)] = ((x, y), 'left')
                if (y < cols -
                    1) and (grid[x][y +
                                    1] not in (1, 2, 3)) and ((x, y +
                                                               1) not in visited):
                    stack.append((x, y + 1))
                    parentMap[(x, y + 1)] = ((x, y), 'right')
                if (x > 0) and (grid[x - 1][y] not in (1, 2, 3)
                                ) and ((x - 1, y) not in visited):
                    stack.append((x - 1, y))
                    parentMap[(x - 1, y)] = ((x, y), 'up')
                if (x < rows -
                    1) and (grid[x +
                                 1][y] not in (1, 2, 3)) and ((x +
                                                               1, y) not in visited):
                    stack.append((x + 1, y))
                    parentMap[(x + 1, y)] = ((x, y), 'down')

    return None, None


# Uses breath first search to path find to the apple in the least amount
# of moves as possible
def bfs(grid, start, goal, order='lr'):
    visited = set()
    dq = deque([start])
    parentMap = {}
    rows, cols, = len(grid), len(grid[0])

    while dq:
        node = dq.pop()
        if node not in visited:
            visited.add(node)

            x, y = node[0], node[1]

            if ((x > 0) and (x < rows - 1) and (y > 0)
                    and (y < cols - 1) and (grid[x][y]) == goal):
                return (x, y), parentMap

            # Favors going left to right than up and down
            if order == 'lr':
                if (x > 0) and (grid[x - 1][y] not in (1, 2)
                                ) and ((x - 1, y) not in visited):
                    dq.appendleft((x - 1, y))
                    parentMap[(x - 1, y)] = ((x, y), 'up')
                if (x < rows -
                    1) and (grid[x +
                                 1][y] not in (1, 2)) and ((x +
                                                            1, y) not in visited):
                    dq.appendleft((x + 1, y))
                    parentMap[(x + 1, y)] = ((x, y), 'down')
                if (y > 0) and (grid[x][y - 1] not in (1, 2)
                                ) and ((x, y - 1) not in visited):
                    dq.appendleft((x, y - 1))
                    parentMap[(x, y - 1)] = ((x, y), 'left')
                if (y < cols -
                    1) and (grid[x][y +
                                    1] not in (1, 2)) and ((x, y +
                                                            1) not in visited):
                    dq.appendleft((x, y + 1))
                    parentMap[(x, y + 1)] = ((x, y), 'right')
            # Favors going up and down than left to right
            elif order == 'ud':
                if (y > 0) and (grid[x][y - 1] not in (1, 2)
                                ) and ((x, y - 1) not in visited):
                    dq.appendleft((x, y - 1))
                    parentMap[(x, y - 1)] = ((x, y), 'left')
                if (y < cols -
                    1) and (grid[x][y +
                                    1] not in (1, 2)) and ((x, y +
                                                            1) not in visited):
                    dq.appendleft((x, y + 1))
                    parentMap[(x, y + 1)] = ((x, y), 'right')
                if (x > 0) and (grid[x - 1][y] not in (1, 2)
                                ) and ((x - 1, y) not in visited):
                    dq.appendleft((x - 1, y))
                    parentMap[(x - 1, y)] = ((x, y), 'up')
                if (x < rows -
                    1) and (grid[x +
                                 1][y] not in (1, 2)) and ((x +
                                                            1, y) not in visited):
                    dq.appendleft((x + 1, y))
                    parentMap[(x + 1, y)] = ((x, y), 'down')

    return None, None


def findPath(goal, start, parentMap):
    curr = goal
    path = []
    while curr != start:
        curr, direction = parentMap[curr]
        path.append(direction)
    return path


# Determines if the snake will get stuck if it follows the path to the apple
def futurePath(path):
    # Makes a copy of the grid
    newGrid = grid.copy()
    for i in range(len(newGrid)):
        newGrid[i] = grid[i].copy()

    if len(path) < len(snakeBody):
        # Starting position is the snake's head position
        changeX = int(snakeHead.left / blockSize)
        changeY = int(snakeHead.top / blockSize)

        # Changes the path the snake will take into 2s on the grid (2 is
        # treated as a body)
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

                newGrid[changeY][changeX] = 2

        # Changes the end of the snake to empty spaces, so it is up to date
        for body in snakeBody:
            if snakeBody.index(body) < len(path) - 2:
                newGrid[int(body.top / blockSize)
                        ][int(body.left / blockSize)] = 0
            else:
                newGrid[int(body.top / blockSize)
                        ][int(body.left / blockSize)] = 5
                break

        # Uncomment to see the new grid
        # for g in newGrid:
        #    print(g)
        # print('\n')

        # Finds a path from the apple to the end of the tail
        # If no path is found, the snake will get stuck if it follows the apple
        # If a path is found, the snake is safe to get the apple
        fStart = int(pythonRound(apple.top / blockSize, 0)), int(pythonRound(apple.left / blockSize, 0))
        goal = 5
        xy, parentMap = dfs(newGrid, fStart, goal)

        if xy is not None:
            # Returns false if the snake will not get stuck
            return False
        else:
            # Returns true if the snake will get stuck
            return True


# Locates a path from the snake head to the furthest end of the snake tail
def findTailPath(path):
    start = int(snakeHead.top / blockSize), int(snakeHead.left / blockSize)

    # Saves the longest path for a worst-case scenario
    highPath = []

    # Finds the furthest tail-piece
    for body in snakeBody:
        # Sets a new goal as the tail-piece it finds
        grid[int(body.top / blockSize)][int(body.left / blockSize)] = 5
        xy, parentMap = dfs(grid, start, 5)

        # If a path is found
        if xy is not None:
            path = findPath(xy, start, parentMap)
            path.reverse()
            # Discards the last direction
            if path:
                path.pop(-1)

            # If a successful path is found
            if len(path) >= snakeBody.index(body) + 1:
                # Tries to find a longer path prioritizing up and down
                xy, parentMap = dfs(grid, start, 5, 'ud')

                if xy is not None:
                    newPath = findPath(xy, start, parentMap)
                    newPath.reverse()

                    if newPath:
                        newPath.pop(-1)

                    if len(newPath) > len(path):
                        path = newPath

                # Uncomment to see which option is chosen
                # print('Option', snakeBody.index(body), 'taken with', len(path), 'directions')
                break
            # If the path found will end up losing the game
            else:
                # Uncomment to see which option got rejected
                # print('Rejected option', snakeBody.index(body), 'with', len(path), 'directions')
                if len(path) > len(highPath):
                    highPath = path

        # Chooses the longest path if no successful path is found
        if snakeBody.index(body) == len(snakeBody) - 1:
            path = highPath
            # Uncomment to see the longest path
            # print('Best option chosen with', len(path), 'directions')
            break

        # Resets the grid
        grid[int(body.top / blockSize)][int(body.left / blockSize)] = 1

    return path


# Locates a path from the snake head to the apple
def findApplePath(path, goal):
    if not path:
        start = int(snakeHead.top / blockSize), int(snakeHead.left / blockSize)

        xy, parentMap = bfs(grid, start, goal)

        # If a path to the apple is found
        if xy is not None:
            path = findPath(xy, start, parentMap)
            path.reverse()

            # Determines if the snake will get stuck if it follows the planned
            # path
            isStuck = futurePath(path)

            # If the snake determines it will get stuck it path finds to the apple again, but this time prioritizing up and down
            if isStuck:
                xy, parentMap = bfs(grid, start, goal, 'ud')

                if xy is not None:
                    path = findPath(xy, start, parentMap)
                    path.reverse()
                    isStuck = futurePath(path)

                    # If the snake will still get stuck it path finds to the end of its tail
                    if isStuck:
                        path = findTailPath(path)
        # If a path to the apple is not found, the snake finds a path to its
        # tail
        else:
            path = findTailPath(path)

    return path


# Generates the apple
def genApple(apple, grid):
    global appleSeed
    global newAppleSeed

    if appleSeed:
        # Follows a set seed
        try:
            apple.left = appleSeed[len(snakeBody) - 1][0]
            apple.top = appleSeed[len(snakeBody) - 1][1]
        # When it runs through the set seed, the apples go back to being random
        except BaseException:
            appleSeed = []
            genApple(apple, grid)
    else:
        # Randomizes apple spawn
        apple.left = randrange(0, size) * blockSize + blockSize
        apple.top = randrange(0, size) * blockSize + blockSize

    # Updates the apple seed
    newApple = (apple.left, apple.top)
    newAppleSeed.append(newApple)

    # Regenerates apple if it is generated inside the snake head
    if snakeHead.hits(apple.centerX, apple.centerY):
        if appleSeed:
            appleSeed.pop(len(snakeBody) - 1)

        newAppleSeed.pop(-1)
        genApple(apple, grid)

    # Regenerates apple if it is generated inside the snake body
    for body in snakeBody:
        if body.hits(apple.centerX, apple.centerY):
            if appleSeed:
                appleSeed.pop(len(snakeBody) - 1)

            newAppleSeed.pop(-1)
            genApple(apple, grid)


def onKeyPress(key):
    global isPaused
    global isPlaying

    # Allows the player to play
    if key == 'P':
        if isPlaying:
            isPlaying = False
            print('Computer in control')
        else:
            isPlaying = True
            print('Player in control')
            print('Use WASD to move')

        isPaused = True
        print('Paused the game')

    # Player controls if the player is playing
    if isPlaying:
        if key == 'w' and snakeHead.direction != 'down':
            snakeHead.direction = 'up'
        if key == 's' and snakeHead.direction != 'up':
            snakeHead.direction = 'down'
        if key == 'a' and snakeHead.direction != 'right':
            snakeHead.direction = 'left'
        if key == 'd' and snakeHead.direction != 'left':
            snakeHead.direction = 'right'

    # Slows down the game
    if key == 'left':
        if app.stepsPerSecond == 1:
            print('Cannot lower speed past', app.stepsPerSecond)
        else:
            app.stepsPerSecond -= 1
            print('Lowered speed', app.stepsPerSecond)

    # Speeds up the game
    if key == 'right':
        app.stepsPerSecond += 1
        print('Increased speed', app.stepsPerSecond)

    # Pauses the game
    if key == 'space':
        if isPaused:
            isPaused = False
        else:
            isPaused = True
            print('Paused the game')

    if key == 'G':
        if gridBackground.visible:
            print('Grid hidden')
            gridBackground.visible = False
        else:
            print('Grid shown')
            gridBackground.visible = True

    # Prints information
    if key == 'I':
        # Prints the current grid
        print('Current grid')
        for g in grid:
            print(g)
        print('\n')

        # Prints the seed of the game, so the game can be replicated
        print('Copy and paste this code to save/replicate where the snake left off')
        print('appleSeed =', newAppleSeed)
        # Prints the snake's head
        print(
            f'snakeHead = Rect({snakeHead.left}, {snakeHead.top}, {blockSize}, {blockSize}, fill=\'blue\', border=\'black\', borderWidth=1)')
        # Prints the snake's body
        print('snakeBody = [', end='')
        for body in snakeBody:
            if snakeBody.index(body) == len(snakeBody) - 1:
                end = ']'
            else:
                end = ','
            print(
                f'Rect({body.left}, {body.top}, {blockSize}, {blockSize}, fill=\'green\', border=\'black\', borderWidth=1)',
                end=end)

    # Ends the game
    if key == 'E':
        print('Terminated game early')
        gameOver()


# This function runs X times every second; X = app.stepsPerSecond (the
# default is 10)
def onStep():
    global path
    global isPaused
    global isPlaying

    # Stops the game from continuing if it is paused
    if isPaused:
        return

    # Ends the game is the snake hits itself or the border
    if border.hits(snakeHead.centerX, snakeHead.centerY):
        gameOver()
        return
    for body in snakeBody:
        if body.hits(snakeHead.centerX, snakeHead.centerY):
            gameOver()
            return

    # Moves the snake body with the head
    snakeBody.append(
        Rect(
            snakeHead.left,
            snakeHead.top,
            blockSize,
            blockSize,
            fill='green',
            border='black',
            borderWidth=1))
    snakeBody[0].visible = False
    snakeBody.pop(0)

    # Stops path updating the grid and pathfinding if the player is in control
    if not isPlaying:
        # Updates the grid whenever the snake doesn't have a path to follow
        # The game would run significantly slower if the grid were to be
        # updated every single step
        if not path:
            for gridX in range(size + 2):
                if gridX != 0 and gridX != (
                        size + 2) - 1:              # Avoids updated the border
                    for gridY in range(size + 2):
                        if gridY != 0 and gridY != (
                                size + 2) - 1:      # Avoids updated the border
                            if apple.hits(
                                    blockSize * gridX + blockSize / 2,
                                    blockSize * gridY + blockSize / 2):
                                grid[gridY][gridX] = 9
                            elif border.hits(blockSize * gridX + blockSize / 2, blockSize * gridY + blockSize / 2):
                                grid[gridY][gridX] = 1
                            else:
                                grid[gridY][gridX] = 0

                            for body in snakeBody:
                                if body.hits(
                                        blockSize * gridX + blockSize / 2,
                                        blockSize * gridY + blockSize / 2):
                                    grid[gridY][gridX] = 1
                                    break

                            if snakeHead.hits(
                                    blockSize * gridX + blockSize / 2,
                                    blockSize * gridY + blockSize / 2):
                                grid[gridY][gridX] = 3

        # Determines the snake's next path to follow
        path = findApplePath(path, 9)
        try:
            snakeHead.direction = path[0]
            # Moves onto the next direction
            path.pop(0)
        except BaseException:
            pass

    # Moves the snake head
    if snakeHead.direction == 'right' and snakeHead.prevDirection != 'left':
        snakeHead.centerX += blockSize
    if snakeHead.direction == 'left' and snakeHead.prevDirection != 'right':
        snakeHead.centerX -= blockSize
    if snakeHead.direction == 'up' and snakeHead.prevDirection != 'down':
        snakeHead.centerY -= blockSize
    if snakeHead.direction == 'down' and snakeHead.prevDirection != 'up':
        snakeHead.centerY += blockSize

    snakeHead.prevDirection = snakeHead.direction

    if apple.hits(snakeHead.centerX, snakeHead.centerY):
        # Adds another snake body
        snakeBody.insert(0, Rect(snakeBody[-1].left,
                              snakeBody[-1].top,
                              blockSize,
                              blockSize,
                              fill='green',
                              border='black',
                              borderWidth=1))
        # Updates score, ends game if score is 324
        score.value = len(snakeBody)

        if score.value == pow(size, 2) - 1:
            gameOver()
            return

        # Generates the next apple
        genApple(apple, grid)


if __name__ == '__main__':
    cmu_graphics.run()