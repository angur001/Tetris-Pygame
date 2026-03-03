from re import S
import pygame
import time
from cell import Cell

from ui.theme import THEMES, DEFAULT_THEME_ID, THEME_SCORE_STEP, get_theme_by_id
from ui.layout import compute_layout
from ui.draw import (
    draw_background,
    draw_panel,
    draw_block,
    draw_grid_lines,
    draw_playfield_frame,
)


class Displays:
    CELL_SIZE = 20
    GRID_WIDTH_PX = 10 * CELL_SIZE  # 200px
    GRID_HEIGHT_PX = 20 * CELL_SIZE  # 400px

    SCREEN_W, SCREEN_H = 400, 500

    def __init__(self, theme_id: int | None = None):
        # If theme_id is provided (1–5), lock to that theme; otherwise cycle by score.
        self.theme_lock_id = theme_id if theme_id in THEMES else None
        self._current_theme_id = self.theme_lock_id or DEFAULT_THEME_ID
        self._last_bucket = None
        self._transition_frames = 0
        self._transition_max = 15

    def _pick_theme(self, score: int):
        if self.theme_lock_id is not None:
            self._current_theme_id = self.theme_lock_id
            return get_theme_by_id(self._current_theme_id)

        # Automatic cycling by score
        if THEME_SCORE_STEP <= 0:
            self._current_theme_id = DEFAULT_THEME_ID
            return get_theme_by_id(self._current_theme_id)

        bucket = score // THEME_SCORE_STEP
        if self._last_bucket is None:
            self._last_bucket = bucket
        elif bucket != self._last_bucket:
            self._last_bucket = bucket
            self._transition_frames = self._transition_max

        theme_ids = sorted(THEMES.keys())
        idx = bucket % len(theme_ids)
        self._current_theme_id = theme_ids[idx]
        return get_theme_by_id(self._current_theme_id)

    def drawFrame(self, screen, game):
        # Compute layout for current screen + grid
        layout = compute_layout(
            self.SCREEN_W,
            self.SCREEN_H,
            self.GRID_WIDTH_PX,
            self.GRID_HEIGHT_PX,
            self.CELL_SIZE,
        )
        grid_rect = layout.grid_rect
        next_rect = layout.next_panel_rect

        # Choose theme based on score (or locked ID)
        score = getattr(game, "score", 0)
        theme = self._pick_theme(score)

        # Background & playfield frame
        draw_background(screen, theme)
        draw_playfield_frame(screen, grid_rect, theme)

        # Draw faint grid lines
        draw_grid_lines(screen, grid_rect, game.WIDTH, game.HEIGHT, self.CELL_SIZE, theme)

        # Draw main game grid blocks
        theme_for_blocks = get_theme_by_id(self._current_theme_id)
        for i in range(game.HEIGHT):
            for j in range(game.WIDTH):
                cell = game.gameGrid[i][j]
                if cell == Cell.Empty:
                    continue
                color = theme_for_blocks.color_for_cell(cell)
                x = grid_rect.left + j * self.CELL_SIZE
                y = grid_rect.top + i * self.CELL_SIZE
                draw_block(screen, x, y, self.CELL_SIZE, color, theme_for_blocks)

        # Draw "next shape" preview on the right side, if available
        if hasattr(game, "nextShape") and game.nextShape is not None:
            preview_padding = 10
            preview_cell_size = self.CELL_SIZE

            # Panel with title
            title_font = pygame.font.Font(None, 24)
            draw_panel(screen, next_rect, theme, title="Next", font=title_font)

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

                base_x = next_rect.x + preview_padding + offset_x
                base_y = next_rect.y + preview_padding + offset_y

                for i in range(len(matrix)):
                    for j in range(len(matrix[0])):
                        cell = matrix[i][j]
                        if cell == Cell.Empty:
                            continue
                        cell_color = theme_for_blocks.color_for_cell(cell)
                        cell_x = base_x + (j - min_j) * preview_cell_size
                        cell_y = base_y + (i - min_i) * preview_cell_size
                        draw_block(
                            screen,
                            cell_x,
                            cell_y,
                            preview_cell_size,
                            cell_color,
                            theme_for_blocks,
                        )

        # HUD: score and level at the top (render-only)
        hud_font = pygame.font.Font(None, 30)
        if hasattr(game, "score"):
            score_text = hud_font.render(
                f"Score: {game.score}", True, theme.TEXT_PRIMARY
            )
            score_rect = score_text.get_rect(topleft=(12, 10))
            screen.blit(score_text, score_rect)

        if hasattr(game, "level"):
            level_text = hud_font.render(
                f"Level: {game.level}", True, theme.TEXT_PRIMARY
            )
            level_rect = level_text.get_rect(topright=(self.SCREEN_W - 12, 10))
            screen.blit(level_text, level_rect)

        # Simple flash overlay on theme change
        if self._transition_frames > 0:
            alpha = int(180 * (self._transition_frames / self._transition_max))
            overlay = pygame.Surface((self.SCREEN_W, self.SCREEN_H), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, alpha))
            screen.blit(overlay, (0, 0))
            self._transition_frames -= 1
   
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