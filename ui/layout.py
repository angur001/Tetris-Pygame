from dataclasses import dataclass

import pygame


@dataclass
class Layout:
    """Precomputed rectangles for main UI regions (render-only)."""

    grid_rect: pygame.Rect
    next_panel_rect: pygame.Rect


def compute_layout(
    screen_w: int,
    screen_h: int,
    grid_w_px: int,
    grid_h_px: int,
    cell_size: int,
) -> Layout:
    """
    Compute positions for the playfield and the "next piece" panel.

    This reproduces the existing layout:
    - Playfield slightly left of center.
    - Next-piece panel to the right of the grid.
    """
    # Base center offsets, then nudge grid a bit left to make side-panel room.
    x_offset_center = (screen_w - grid_w_px) // 2
    grid_x = x_offset_center - 40
    grid_y = (screen_h - grid_h_px) // 2

    grid_rect = pygame.Rect(grid_x, grid_y, grid_w_px, grid_h_px)

    # Next-piece panel sizing matches previous logic: 4x4 cells plus padding.
    preview_padding = 10
    preview_w = cell_size * 4 + preview_padding * 2
    preview_h = cell_size * 4 + preview_padding * 2

    preview_x = grid_x + grid_w_px + 40
    preview_y = grid_y + 40
    next_panel_rect = pygame.Rect(preview_x, preview_y, preview_w, preview_h)

    return Layout(grid_rect=grid_rect, next_panel_rect=next_panel_rect)

