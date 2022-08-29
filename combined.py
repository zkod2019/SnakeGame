from cvzone.HandTrackingModule import HandDetector

import cv2
import copy
import math
import pygame
import random
import threading

pygame.init()

tile_width = 20
size = tile_width * tile_width
screen = pygame.display.set_mode([size, size])

colors = {
    "bg": (0, 0, 0),
    "snake": (255, 0, 0),
    "apple": (0, 255, 0),
}

grid = [[colors["bg"] for i in range(tile_width)] for j in range(tile_width)]

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x \
            and self.y == other.y

    def __hash__(self):
        return hash(('x', self.x, 'y', self.y))

class Snake:
    def __init__(self, direction='left'):
        self.body = [Point(5, 0), Point(6, 0), Point(7, 0)]
        self.direction = direction
        self.grow = False

    def draw(self, grid):
        for point in self.body:
            grid[point.x][point.y] = colors["snake"]

    def set_direction(self, direction):
        if self.direction == "right" and direction == "left":
            self.direction = "right"
        elif self.direction == "left" and direction == "right":
            self.direction = "left"
        elif self.direction == "up" and direction == "down":
            self.direction = "up"
        elif self.direction == "down" and direction == "up":
            self.direction = "down"
        else:
            self.direction = direction

    def move(self, grid):
        # Deepcopy is required because of the Point object
        new_body = copy.deepcopy(self.body)

        # Duplicate the previous snakes head
        new_head = new_body[0]

        # Then move it to the next position
        if self.direction == "right":
            new_head.x += 1
        elif self.direction == "left":
            new_head.x -= 1
        elif self.direction == "up":
            new_head.y -= 1
        elif self.direction == "down":
            new_head.y += 1

        new_head.x = (new_head.x + tile_width) % tile_width
        new_head.y = (new_head.y + tile_width) % tile_width

        # If snake is not growing remove the last piece
        if not self.grow:
            toClear = self.body.pop()
            grid[toClear.y][toClear.x] = colors["bg"]

        # Add back the new head
        self.body.insert(0, new_head)
        self.grow = False  # Reset the growing

clock = pygame.time.Clock()
running = True

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

def hand_detection():
    global snake
    while True:
        # Get image frame
        success, img = cap.read()
        # Find the hand and its landmarks
        hands, img = detector.findHands(img)  # with draw
        # hands = detector.findHands(img, draw=False)  # without draw

        if hands:
            hand = hands[0]
            if hand["type"] == "Right":
                thumbBase = hand["lmList"][1]
                thumbTip = hand["lmList"][4]
                angle = math.atan2(thumbTip[1] - thumbBase[1], thumbTip[0] - thumbBase[0]) * 180 / math.pi

                newDirection = None
                # bottom left quadrant
                if angle > 20 and angle < 60:
                    newDirection = "down"
                elif angle < -10 and angle > -40:
                    newDirection = "left"
                elif angle < -40 and angle > -80:
                    newDirection = "up"
                elif angle < -100 and angle > -150:
                    newDirection = "right"
                
                if newDirection != None and newDirection != snake.direction:
                    snake.set_direction(newDirection)
                    print(f"Direction changed to: {snake.direction}")

        # Display
        cv2.imshow("Preview", img)
        cv2.waitKey(1)

hand_detection_thread = threading.Thread(target=hand_detection)
hand_detection_thread.start()

snake = Snake()
apple = Point(5, 5)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.set_direction("left")
            elif event.key == pygame.K_RIGHT:
                snake.set_direction("right")
            elif event.key == pygame.K_UP:
                snake.set_direction("up")
            elif event.key == pygame.K_DOWN:
                snake.set_direction("down")
 
    screen.fill(colors["bg"])
    
    grid = [[colors["bg"] for i in range(tile_width)] for j in range(tile_width)]
    grid[apple.x][apple.y] = colors["apple"]
    snake.draw(grid)

    if len(set(snake.body)) != len(snake.body):
        grid = [[colors["bg"] for i in range(tile_width)] for j in range(tile_width)]
        snake = Snake()
        apple = Point(5, 5)
        continue
    elif snake.body[0] == apple:
        while True:
            apple.x = random.randint(0, tile_width-1)
            apple.y = random.randint(0, tile_width-1)

            if not (apple in snake.body):
                break
        snake.grow = True

    snake.move(grid)
    
    for i, row in enumerate(grid):
        for j, px in enumerate(row):
            pygame.draw.rect(screen, px, pygame.Rect(i * tile_width, j * tile_width, tile_width, tile_width))

    pygame.display.flip()
    clock.tick(8)

pygame.quit()
