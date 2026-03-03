import pygame

_BACKGROUND_CACHE = {}


def _create_background(size, theme):
    """Precompute a vertical gradient background surface for a given theme."""
    width, height = size
    surf = pygame.Surface((width, height))

    top = theme.BG_TOP
    bottom = theme.BG_BOTTOM

    for y in range(height):
        t = y / max(height - 1, 1)
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (width, y))

    # Simple vignette overlay (soft darkening at edges), strength per theme
    vignette = pygame.Surface((width, height), pygame.SRCALPHA)
    edge_alpha = getattr(theme, "VIGNETTE_ALPHA", 120)
    inner_alpha = 0
    margin_factor = getattr(theme, "VIGNETTE_MARGIN_FACTOR", 1 / 6)
    margin = int(min(width, height) * margin_factor)

    for y in range(height):
        for x in range(width):
            dx = min(x, width - 1 - x)
            dy = min(y, height - 1 - y)
            d = min(dx, dy)
            if d >= margin:
                alpha = inner_alpha
            else:
                t = (margin - d) / margin
                alpha = int(inner_alpha + t * (edge_alpha - inner_alpha))
            if alpha > 0:
                vignette.set_at((x, y), (0, 0, 0, alpha))

    surf.blit(vignette, (0, 0))
    return surf


def draw_background(screen: pygame.Surface, theme):
    """Draw cached gradient background for the current theme."""
    size = screen.get_size()
    key = (size, getattr(theme, "NAME", "default"))
    if key not in _BACKGROUND_CACHE:
        _BACKGROUND_CACHE[key] = _create_background(size, theme)
    screen.blit(_BACKGROUND_CACHE[key], (0, 0))


def draw_panel(screen: pygame.Surface, rect: pygame.Rect, theme, title: str | None = None, font=None):
    """Draw a rounded panel with subtle shadow and optional title, themed."""
    radius = getattr(theme, "PANEL_RADIUS", 12)
    shadow_offset = getattr(theme, "PANEL_SHADOW_OFFSET", (3, 3))
    # Shadow
    shadow_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(
        shadow_surf,
        theme.PANEL_SHADOW,
        shadow_surf.get_rect(),
        border_radius=radius,
    )
    screen.blit(shadow_surf, (rect.x + shadow_offset[0], rect.y + shadow_offset[1]))

    # Panel background
    pygame.draw.rect(
        screen,
        theme.PANEL_BG,
        rect,
        border_radius=radius,
    )
    # Border
    pygame.draw.rect(
        screen,
        theme.PANEL_BORDER,
        rect,
        width=getattr(theme, "PANEL_BORDER_WIDTH", 2),
        border_radius=radius,
    )

    # Title text, if any
    if title and font is not None:
        label_surf = font.render(title, True, theme.TEXT_ACCENT)
        label_rect = label_surf.get_rect(midbottom=(rect.centerx, rect.top - 4))
        screen.blit(label_surf, label_rect)


def draw_block(screen: pygame.Surface, x: int, y: int, size: int, color, theme):
    """Draw a single Tetris block with a themed shading style."""
    if color is None:
        return

    base_rect = pygame.Rect(x, y, size, size)

    radius = getattr(theme, "BLOCK_RADIUS", 5)
    border_w = getattr(theme, "BLOCK_BORDER_WIDTH", 2)
    darken = getattr(theme, "BLOCK_BORDER_DARKEN", 60)
    brighten = getattr(theme, "BLOCK_HIGHLIGHT_BRIGHTEN", 50)
    highlight_ratio = getattr(theme, "BLOCK_HIGHLIGHT_HEIGHT_RATIO", 0.33)

    # Optional glow (e.g., for neon theme)
    if getattr(theme, "BLOCK_USE_GLOW", False):
        glow_rect = base_rect.inflate(6, 6)
        glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        glow_color = (*color, getattr(theme, "BLOCK_GLOW_ALPHA", 70))
        pygame.draw.rect(
            glow_surf,
            glow_color,
            glow_surf.get_rect(),
            border_radius=radius + 3,
        )
        screen.blit(glow_surf, glow_rect.topleft)

    # Outer base
    pygame.draw.rect(
        screen,
        color,
        base_rect,
        border_radius=radius,
    )

    # Darker border
    border_color = tuple(max(c - darken, 0) for c in color)
    pygame.draw.rect(
        screen,
        border_color,
        base_rect,
        width=border_w,
        border_radius=radius,
    )

    # Top highlight strip
    highlight_color = tuple(min(c + brighten, 255) for c in color)
    h_height = max(2, int(size * highlight_ratio))
    highlight_rect = pygame.Rect(x + 2, y + 2, size - 4, h_height)
    pygame.draw.rect(
        screen,
        highlight_color,
        highlight_rect,
        border_radius=max(radius - 1, 0),
    )


def draw_grid_lines(screen: pygame.Surface, grid_rect: pygame.Rect, cols: int, rows: int, cell_size: int, theme):
    """Faint grid lines within the playfield."""
    width = getattr(theme, "GRID_LINE_WIDTH", 1)
    # Vertical lines
    for c in range(cols + 1):
        x = grid_rect.left + c * cell_size
        pygame.draw.line(
            screen,
            theme.GRID_LINE,
            (x, grid_rect.top),
            (x, grid_rect.bottom),
            width,
        )
    # Horizontal lines
    for r in range(rows + 1):
        y = grid_rect.top + r * cell_size
        pygame.draw.line(
            screen,
            theme.GRID_LINE,
            (grid_rect.left, y),
            (grid_rect.right, y),
            width,
        )


def draw_playfield_frame(screen: pygame.Surface, grid_rect: pygame.Rect, theme):
    """Stronger outer frame around the playfield."""
    frame_rect = grid_rect.inflate(8, 8)
    outer_w = getattr(theme, "FRAME_OUTER_WIDTH", 4)
    inner_w = getattr(theme, "FRAME_INNER_WIDTH", 2)
    radius = getattr(theme, "FRAME_RADIUS", 10)
    pygame.draw.rect(
        screen,
        theme.PLAYFIELD_FRAME_DARK,
        frame_rect,
        width=outer_w,
        border_radius=radius,
    )
    pygame.draw.rect(
        screen,
        theme.PLAYFIELD_FRAME,
        frame_rect,
        width=inner_w,
        border_radius=radius,
    )


