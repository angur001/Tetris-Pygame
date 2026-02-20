from re import S
import pygame
import time
from cell import Cell

class Displays:
    CELL_SIZE = 20
    GRID_WIDTH_PX = 10 * CELL_SIZE  # 200px
    GRID_HEIGHT_PX = 20 * CELL_SIZE # 400px

    SCREEN_W, SCREEN_H = 400, 500

    X_OFFSET = (SCREEN_W - GRID_WIDTH_PX) // 2
    Y_OFFSET = (SCREEN_H - GRID_HEIGHT_PX) // 2
    
    def drawFrame(self, screen, game):
        for i in range(game.HEIGHT):
            for j in range(game.WIDTH):
                # calculate position of the cell
                rect_x = self.X_OFFSET + (j * self.CELL_SIZE)
                rect_y = self.Y_OFFSET + (i * self.CELL_SIZE)
                
                color = Cell.getColorValue(game.gameGrid[i][j])
                pygame.draw.rect(screen, color, (rect_x, rect_y, self.CELL_SIZE, self.CELL_SIZE))
                
                # outline trick
                pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, self.CELL_SIZE, self.CELL_SIZE), 1)

   
    def DisplayGameOver(self, screen , score = 0):
            # Create a semi-transparent overlay
            overlay = pygame.Surface((self.SCREEN_W, self.SCREEN_H))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # Display game over text
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.SCREEN_W // 2, self.SCREEN_H // 2 - 50))
            screen.blit(game_over_text, text_rect)
            
            # Display score
            score_font = pygame.font.Font(None, 36)
            score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.SCREEN_W // 2, self.SCREEN_H // 2 + 20))
            screen.blit(score_text, score_rect)