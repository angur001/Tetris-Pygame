# Skill: Make a Pygame Tetris Prettier (Zero Logic Changes)

## Mission
Upgrade the game's **visual appeal and feel** (UI polish) while changing **ABSOLUTELY NOTHING** about gameplay logic, rules, scoring, timing, piece behavior, collisions, RNG, rotations, line clears, or input semantics.

You are allowed to:
- Add rendering helpers
- Add UI layout constants
- Add assets that are *not custom sprites* (fonts, gradients, simple shapes, procedural effects)
- Add sound polish (optional) without touching logic
- Add toggles/config for visuals only
- Refactor drawing code for cleanliness/performance (still zero behavior change)

You are NOT allowed to:
- Modify piece movement/rotation code
- Modify collision checks
- Modify gravity/timing/deltas
- Modify score/level/line-clear rules
- Modify the game loop logic in any way that affects what happens, only how it’s drawn
- Change the board representation or piece definitions
- Change randomization behavior
- Introduce new gameplay features (ghost piece, hold, previews count change) unless it already exists
- Change keybinds behavior (you may add UI hints showing existing binds)

If uncertain, assume it's gameplay logic and **do not touch it**.

---

## Aesthetic Targets (What "prettier" means)
### 1) Clean layout & spacing
- Center the playfield with generous padding.
- Make side panels aligned (Next piece, Score, Level, Lines).
- Add consistent margins, rounded panels, and a background.

### 2) Modern color palette
- Replace raw RGB primaries with a cohesive palette.
- Provide 2–3 themes (Dark, Neon, Pastel) via config constants.

### 3) Better blocks (no sprites)
- Draw blocks with:
  - subtle bevel/inner highlight
  - thin border
  - soft shadow under stack
- Use `pygame.draw.rect(..., border_radius=...)` for round corners.

### 4) Background polish
- Simple animated gradient or static gradient
- Subtle noise/scanlines overlay (procedural)
- Vignette overlay (procedural)

### 5) UI typography
- Use `pygame.font.Font` with a nice free font file in `/assets/fonts` (optional).
- Use hierarchy: title > section headers > values.
- Consistent text color and anti-aliasing.

### 6) Feedback & juice (still no logic changes)
- Line clear: quick screen shake / flash overlay (purely visual)
- Piece lock: tiny “thunk” effect (visual glow)
- Soft particle sparks for clears (procedural circles)
- Smooth drop trail (render-only)

### 7) Performance-safe
- Cache surfaces:
  - background gradient surface
  - panel surfaces
  - pre-rendered text for values that don't change every frame
- Avoid per-frame heavy loops beyond board draw.

---

## Useful Pygame Techniques
### Rounded rects
- `pygame.draw.rect(surface, color, rect, border_radius=12)`
- For borders: draw twice (outer darker, inner main).

### Shadows
- Draw same rect offset by (3,3) with alpha surface.
- Use an `SRCALPHA` surface for translucency.

### Alpha overlays
- `overlay = pygame.Surface(size, pygame.SRCALPHA)`
- Fill with `(0,0,0, alpha)` and blit.

### Gradients
- Precompute once into a surface.
- Vertical gradient: draw horizontal lines with interpolated color.

### Glow
- Fake glow by drawing the same rect several times expanded by 1–3px with lower alpha.

### Text rendering
- Always antialias: `font.render(text, True, color)`
- Cache rendered surfaces for repeated strings.

---

## Deliverables Checklist
✅ A `render/` or `ui/` module that contains:
- theme constants
- layout constants
- helpers: draw_panel, draw_block, draw_text, draw_background

✅ Zero edits to gameplay functions except:
- replacing direct draw calls with helper draw calls
- passing state to renderer instead of re-computing logic

✅ Before/after screenshots (optional but helpful)

---

## Self-test (Must pass)
- Same inputs produce same outcomes.
- Scoring and timing identical.
- RNG identical.
- The only difference is how it looks/sounds.

If anything about gameplay *feels* different, revert.