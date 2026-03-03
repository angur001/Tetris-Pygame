from cell import Cell


class DarkRetroTheme:
    """Color palette for a dark retro / arcade look (render-only)."""

    NAME = "dark_retro"

    # Background gradient (top → bottom)
    BG_TOP = (10, 8, 30)
    BG_BOTTOM = (2, 4, 12)

    # Playfield & grid
    GRID_LINE = (32, 38, 70)
    PLAYFIELD_FRAME = (120, 210, 255)
    PLAYFIELD_FRAME_DARK = (40, 70, 120)

    # Panels
    PANEL_BG = (14, 16, 34)
    PANEL_BORDER = (90, 140, 210)
    PANEL_SHADOW = (0, 0, 0, 140)

    # Text
    TEXT_PRIMARY = (230, 235, 255)
    TEXT_ACCENT = (120, 200, 255)
    TEXT_MUTED = (150, 160, 200)
    TEXT_WARNING = (255, 120, 140)

    # Blocks (neon-tinted versions for dark background)
    BLOCK_COLORS = {
        Cell.Red: (255, 90, 90),
        Cell.Blue: (90, 150, 255),
        Cell.Green: (110, 220, 150),
        Cell.Yellow: (245, 210, 110),
        Cell.Purple: (210, 130, 255),
    }

    EMPTY_COLOR = (8, 10, 24)

    # Style
    VIGNETTE_ALPHA = 120
    VIGNETTE_MARGIN_FACTOR = 1 / 6
    PANEL_RADIUS = 12
    PANEL_SHADOW_OFFSET = (3, 3)
    PANEL_BORDER_WIDTH = 2
    BLOCK_RADIUS = 5
    BLOCK_BORDER_WIDTH = 2
    BLOCK_BORDER_DARKEN = 60
    BLOCK_HIGHLIGHT_BRIGHTEN = 50
    BLOCK_HIGHLIGHT_HEIGHT_RATIO = 0.33
    GRID_LINE_WIDTH = 1
    FRAME_OUTER_WIDTH = 4
    FRAME_INNER_WIDTH = 2
    FRAME_RADIUS = 10

    @staticmethod
    def color_for_cell(cell: Cell):
        if cell == Cell.Empty:
            return None
        return DarkRetroTheme.BLOCK_COLORS.get(cell, DarkRetroTheme.TEXT_PRIMARY)


class DarkJapaneseCedarTheme:
    """Dark wood + warm lantern accents (render-only)."""

    NAME = "dark_japanese_cedar"

    BG_TOP = (12, 8, 6)
    BG_BOTTOM = (4, 3, 3)

    GRID_LINE = (40, 26, 20)
    PLAYFIELD_FRAME = (180, 130, 70)
    PLAYFIELD_FRAME_DARK = (80, 50, 30)

    PANEL_BG = (24, 16, 12)
    PANEL_BORDER = (160, 110, 60)
    PANEL_SHADOW = (0, 0, 0, 160)

    TEXT_PRIMARY = (240, 220, 190)
    TEXT_ACCENT = (230, 170, 90)
    TEXT_MUTED = (170, 140, 110)
    TEXT_WARNING = (220, 110, 80)

    BLOCK_COLORS = {
        Cell.Red: (210, 80, 70),
        Cell.Blue: (80, 140, 210),
        Cell.Green: (120, 180, 120),
        Cell.Yellow: (220, 180, 90),
        Cell.Purple: (180, 120, 210),
    }

    EMPTY_COLOR = (18, 12, 10)

    # Style: heavier vignette, squarer blocks, stronger frame
    VIGNETTE_ALPHA = 160
    VIGNETTE_MARGIN_FACTOR = 0.2
    PANEL_RADIUS = 8
    PANEL_SHADOW_OFFSET = (4, 4)
    PANEL_BORDER_WIDTH = 2
    BLOCK_RADIUS = 3
    BLOCK_BORDER_WIDTH = 2
    BLOCK_BORDER_DARKEN = 70
    BLOCK_HIGHLIGHT_BRIGHTEN = 40
    BLOCK_HIGHLIGHT_HEIGHT_RATIO = 0.3
    GRID_LINE_WIDTH = 1
    FRAME_OUTER_WIDTH = 5
    FRAME_INNER_WIDTH = 2
    FRAME_RADIUS = 8

    @staticmethod
    def color_for_cell(cell: Cell):
        if cell == Cell.Empty:
            return None
        return DarkJapaneseCedarTheme.BLOCK_COLORS.get(cell, DarkJapaneseCedarTheme.TEXT_PRIMARY)


class NeonGridTheme:
    """High-contrast neon-on-black, very arcadey (render-only)."""

    NAME = "neon_grid"

    BG_TOP = (0, 0, 0)
    BG_BOTTOM = (0, 0, 0)

    GRID_LINE = (40, 80, 120)
    PLAYFIELD_FRAME = (0, 255, 200)
    PLAYFIELD_FRAME_DARK = (0, 120, 100)

    PANEL_BG = (5, 5, 20)
    PANEL_BORDER = (0, 200, 255)
    PANEL_SHADOW = (0, 0, 0, 180)

    TEXT_PRIMARY = (230, 255, 255)
    TEXT_ACCENT = (0, 255, 200)
    TEXT_MUTED = (140, 190, 190)
    TEXT_WARNING = (255, 120, 160)

    BLOCK_COLORS = {
        Cell.Red: (255, 60, 110),
        Cell.Blue: (60, 190, 255),
        Cell.Green: (60, 255, 180),
        Cell.Yellow: (255, 240, 120),
        Cell.Purple: (200, 120, 255),
    }

    EMPTY_COLOR = (5, 5, 15)

    # Style: strong vignette, glow blocks, sharp frame
    VIGNETTE_ALPHA = 200
    VIGNETTE_MARGIN_FACTOR = 0.25
    PANEL_RADIUS = 10
    PANEL_SHADOW_OFFSET = (3, 3)
    PANEL_BORDER_WIDTH = 2
    BLOCK_RADIUS = 4
    BLOCK_BORDER_WIDTH = 2
    BLOCK_BORDER_DARKEN = 40
    BLOCK_HIGHLIGHT_BRIGHTEN = 80
    BLOCK_HIGHLIGHT_HEIGHT_RATIO = 0.28
    BLOCK_USE_GLOW = True
    BLOCK_GLOW_ALPHA = 80
    GRID_LINE_WIDTH = 1
    FRAME_OUTER_WIDTH = 4
    FRAME_INNER_WIDTH = 2
    FRAME_RADIUS = 12

    @staticmethod
    def color_for_cell(cell: Cell):
        if cell == Cell.Empty:
            return None
        return NeonGridTheme.BLOCK_COLORS.get(cell, NeonGridTheme.TEXT_PRIMARY)


class MidnightOceanTheme:
    """Deep blue ocean night with cool tones (render-only)."""

    NAME = "midnight_ocean"

    BG_TOP = (4, 12, 30)
    BG_BOTTOM = (1, 5, 18)

    GRID_LINE = (20, 40, 70)
    PLAYFIELD_FRAME = (90, 150, 220)
    PLAYFIELD_FRAME_DARK = (20, 50, 90)

    PANEL_BG = (6, 16, 34)
    PANEL_BORDER = (100, 160, 220)
    PANEL_SHADOW = (0, 0, 0, 150)

    TEXT_PRIMARY = (220, 235, 255)
    TEXT_ACCENT = (120, 190, 250)
    TEXT_MUTED = (150, 170, 200)
    TEXT_WARNING = (230, 130, 130)

    BLOCK_COLORS = {
        Cell.Red: (230, 110, 110),
        Cell.Blue: (110, 180, 255),
        Cell.Green: (120, 220, 190),
        Cell.Yellow: (240, 215, 140),
        Cell.Purple: (200, 150, 255),
    }

    EMPTY_COLOR = (5, 10, 22)

    # Style: medium vignette, smooth rounded blocks, calm frame
    VIGNETTE_ALPHA = 110
    VIGNETTE_MARGIN_FACTOR = 0.22
    PANEL_RADIUS = 12
    PANEL_SHADOW_OFFSET = (3, 3)
    PANEL_BORDER_WIDTH = 2
    BLOCK_RADIUS = 6
    BLOCK_BORDER_WIDTH = 2
    BLOCK_BORDER_DARKEN = 50
    BLOCK_HIGHLIGHT_BRIGHTEN = 55
    BLOCK_HIGHLIGHT_HEIGHT_RATIO = 0.35
    GRID_LINE_WIDTH = 1
    FRAME_OUTER_WIDTH = 4
    FRAME_INNER_WIDTH = 2
    FRAME_RADIUS = 11

    @staticmethod
    def color_for_cell(cell: Cell):
        if cell == Cell.Empty:
            return None
        return MidnightOceanTheme.BLOCK_COLORS.get(cell, MidnightOceanTheme.TEXT_PRIMARY)



# Theme registry --------------------------------------------------------------

THEMES = {
    1: DarkRetroTheme,
    2: DarkJapaneseCedarTheme,
    3: NeonGridTheme,
    4: MidnightOceanTheme,
}

DEFAULT_THEME_ID = 1
THEME_SCORE_STEP = 200  # points per automatic theme change (modifiable)


def get_theme_by_id(theme_id: int):
    return THEMES.get(theme_id, DarkRetroTheme)