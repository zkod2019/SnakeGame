import pygame
import time
import random

# https://www.edureka.co/blog/snake-game-with-pygame/
# https://www.analyticsvidhya.com/blog/2021/06/gesture-controlled-video-game/
pygame.init()
display_width = 600
display_height  = 600
display = pygame.display.set_mode((display_width, display_height))

pygame.display.update()
pygame.display.set_caption('Snake Game')

color = (255,0,0)
white = (0,0,0)

snake_block=10
clock = pygame.time.Clock()
snake_speed=10

def gameLoop():
    game_over=False
    x1 = display_width/2
    y1 = display_height/2

    x2 = 0
    y2 = 0

    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_over=True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x2 = -snake_block
                    y2 = 0
                elif event.key == pygame.K_RIGHT:
                    x2 = snake_block
                    y2 = 0 
                elif event.key == pygame.K_UP:
                    x2 = 0
                    y2 = -snake_block
                elif event.key == pygame.K_DOWN:
                    x2 = 0
                    y2 = snake_block
        if x1 > display_width or y1 >= display_height or x1<0 or y1<0:
            game_over=True
        x1 += x2
        y1 += y2
        display.fill(white)
        pygame.draw.rect(display, (255,0,0), [x1, y1, snake_block, snake_block])
        pygame.draw.rect(display, (0,0,255), [foodx, foody, snake_block, snake_block])
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            print("Yummy!!")
    
        clock.tick(snake_speed)
        #pygame.draw.rect(display, color, pygame.Rect(200, 150, 30, 30)) #first two num r position and second two num are size of square
        #pygame.display.flip()
 

    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()
gameLoop()
