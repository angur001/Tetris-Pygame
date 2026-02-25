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
        # Shift the main grid slightly to the left to leave more space on the right
        grid_x_offset = self.X_OFFSET - 40
        grid_y_offset = self.Y_OFFSET

        # Draw main game grid
        for i in range(game.HEIGHT):
            for j in range(game.WIDTH):
                rect_x = grid_x_offset + (j * self.CELL_SIZE)
                rect_y = grid_y_offset + (i * self.CELL_SIZE)

                color = Cell.getColorValue(game.gameGrid[i][j])
                pygame.draw.rect(screen, color, (rect_x, rect_y, self.CELL_SIZE, self.CELL_SIZE))
                pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, self.CELL_SIZE, self.CELL_SIZE), 1)

        # Draw "next shape" preview on the right side, if available
        if hasattr(game, "nextShape") and game.nextShape is not None:
            preview_padding = 10
            preview_cell_size = self.CELL_SIZE

            # Position the preview box to the right of the grid
            preview_x = grid_x_offset + self.GRID_WIDTH_PX + 40
            preview_y = grid_y_offset + 40
            preview_w = preview_cell_size * 4 + preview_padding * 2
            preview_h = preview_cell_size * 4 + preview_padding * 2

            # Background rectangle for the preview
            pygame.draw.rect(screen, (30, 30, 30), (preview_x, preview_y, preview_w, preview_h))
            pygame.draw.rect(screen, (255, 255, 255), (preview_x, preview_y, preview_w, preview_h), 2)

            # Label above the preview box (black text so it stands out against the white grid)
            font = pygame.font.Font(None, 24)
            label_surface = font.render("Next Shape", True, (0, 0, 0))
            label_rect = label_surface.get_rect(midbottom=(preview_x + preview_w // 2, preview_y - 5))
            screen.blit(label_surface, label_rect)

            # Draw the next shape inside the preview box using its 4x4 matrix,
            # centered within the preview area based on its bounding box.
            matrix = game.nextShape.matrix

            # Compute bounding box of non-empty cells
            min_i, max_i = len(matrix), -1
            min_j, max_j = len(matrix[0]), -1
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] != Cell.Empty:
                        if i < min_i:
                            min_i = i
                        if i > max_i:
                            max_i = i
                        if j < min_j:
                            min_j = j
                        if j > max_j:
                            max_j = j

            if max_i >= 0 and max_j >= 0:
                inner_w = 4 * preview_cell_size
                inner_h = 4 * preview_cell_size
                shape_w = (max_j - min_j + 1) * preview_cell_size
                shape_h = (max_i - min_i + 1) * preview_cell_size

                offset_x = (inner_w - shape_w) // 2
                offset_y = (inner_h - shape_h) // 2

                base_x = preview_x + preview_padding + offset_x
                base_y = preview_y + preview_padding + offset_y

                for i in range(len(matrix)):
                    for j in range(len(matrix[0])):
                        if matrix[i][j] == Cell.Empty:
                            continue
                        cell_color = Cell.getColorValue(matrix[i][j])
                        cell_x = base_x + (j - min_j) * preview_cell_size
                        cell_y = base_y + (i - min_i) * preview_cell_size
                        pygame.draw.rect(screen, cell_color, (cell_x, cell_y, preview_cell_size, preview_cell_size))
                        pygame.draw.rect(screen, (0, 0, 0), (cell_x, cell_y, preview_cell_size, preview_cell_size), 1)


        hud_font = pygame.font.Font(None, 36)
        if hasattr(game, "score"):
            score_text = hud_font.render(f"Score: {game.score}", True, (0, 0, 0))
            score_rect = score_text.get_rect(topleft=(10, 10))
            screen.blit(score_text, score_rect)

        if hasattr(game, "level"):
            level_text = hud_font.render(f"Level: {game.level}", True, (0, 0, 0))
            level_rect = level_text.get_rect(topright=(self.SCREEN_W - 20, 10))
            screen.blit(level_text, level_rect)
   
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