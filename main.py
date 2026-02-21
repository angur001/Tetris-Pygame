import pygame
from gameState import GameState
from displays import Displays

pygame.init()
displays = Displays()
game = GameState()
screen = pygame.display.set_mode((Displays.SCREEN_W, Displays.SCREEN_H))
pygame.display.set_caption("Tetris")
## genera documentation
## game state will be a 2d array of 10x20
## game state will also include score and some variable that will be used to control the game speed
## each cell can be empty or have a block of a certain color
## we can represent a cell with an enum: Empty, Red, Blue, Green, Yellow, Purple
## shapes will be represented as 4*4 matrice
## each cell  in the shape matrix will be represented same as cells in the game state
## shape object will also include coordinates of the shape in the game grid
## shapes will be harcoded same for all rotations for shape for simplicity
## arrow keys will be used to move the shape left and right and also to rotate the shape
## when a shaped reaches the bottom of the game grid, it is added to the game state and a new shape is generated


SHAPE_FALL_EVENT = pygame.USEREVENT + 1 ## custom id that's supposed to be unique
pygame.time.set_timer(SHAPE_FALL_EVENT, game.getGameSpeed())
SOFT_DROP_SPEED = 25
last_soft_drop_time = pygame.time.get_ticks()

running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SHAPE_FALL_EVENT:
            game.step()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.tryMoveLeft()
            if event.key == pygame.K_RIGHT:
                game.tryMoveRight()
            if event.key == pygame.K_UP:
                game.tryRotate()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        if current_time - last_soft_drop_time > SOFT_DROP_SPEED:
            game.step()
            last_soft_drop_time = current_time


    screen.fill((255, 255, 255))
    displays.drawFrame(screen, game)
    if game.gameOver():
        displays.DisplayGameOver(screen, game.score)
    pygame.display.flip()
pygame.quit()