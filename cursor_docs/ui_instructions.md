# Instructions: Beautify the Pygame Tetris (UI-only, Logic Frozen)

## Critical Rule
You must change ABSOLUTELY NOTHING in gameplay logic.

Do NOT modify:
- movement
- rotations
- collision detection
- gravity/timing
- scoring rules
- level progression
- RNG / bag logic
- input semantics
- board dimensions
- spawn positions

If gameplay behavior changes in any way, you failed.

---

# Where To Look First

Most drawing logic lives in:

    displays.py

This is your primary target file.

Start there.
Refactor rendering from there.
Improve visuals from there.

You are allowed to inspect the whole repository to understand how state flows,
but gameplay modules must remain untouched.

If you need to separate concerns:
- Extract rendering helpers into `ui/` modules.
- Keep gameplay modules intact.
- Only adjust calls that relate to drawing.

---

# Step 0 — Identify Logic vs Rendering

In the project:

### Likely Gameplay Files (DO NOT TOUCH)
- board logic
- piece definitions
- rotation system
- collision checks
- scoring
- main game loop timing
- input handling

### Primary Rendering File
- `displays.py`

This file likely:
- draws the grid
- draws pieces
- draws UI elements
- renders text
- manages layout positions

You may:
- Refactor inside displays.py
- Move draw functions into new modules
- Replace hardcoded colors/layout with theme constants

You may NOT:
- Change data passed into drawing functions
- Add new state that influences gameplay

---

# Step 1 — Restructure Rendering Cleanly

Create a small UI system:

- ui/theme.py
    - color palettes
    - font sizes
    - spacing constants

- ui/layout.py
    - panel dimensions
    - margins
    - block size
    - screen padding

- ui/draw.py
    - draw_block()
    - draw_panel()
    - draw_text()
    - draw_background()

- ui/effects.py (optional)
    - flash overlay
    - particles (visual-only)
    - glow helpers

Refactor displays.py to call these helpers instead of raw pygame.draw calls.

Gameplay code must still pass:
- board state
- active piece state
- score/level info

No new gameplay logic allowed inside UI code.

---

# Step 2 — Visual Improvements To Implement

## 2.1 Background

- Precompute a vertical or radial gradient surface.
- Add subtle vignette overlay.
- Optional: slight animated gradient shift using time (render-only).

Do NOT affect timing.

---

## 2.2 Panels

Replace flat rectangles with:
- rounded rectangles (border_radius)
- subtle drop shadow
- slightly darker outer frame
- consistent margins

All purely cosmetic.

---

## 2.3 Blocks

Upgrade block rendering:

For each block:
- rounded rectangle
- thin darker border
- subtle top-left highlight strip
- faint shadow behind stack

Still drawn at exact same grid coordinates.

No coordinate changes.
No size changes affecting collision.

---

## 2.4 Grid

- Add faint grid lines with low alpha.
- Stronger outer frame around playfield.

---

## 2.5 Typography

- Load font with fallback:
    try assets/fonts/Inter-Regular.ttf
    else pygame default font

Use hierarchy:
- Title: large
- Section headers: medium
- Values: bold/bright

Cache rendered text surfaces when possible.

---

# Step 3 — Optional Visual Juice (Safe Only)

You may add:

### Line Clear Flash
If gameplay reports lines cleared:
- draw temporary white overlay that fades out
- do NOT modify clear timing

### Subtle Particles
Spawn small fading circles when lines clear.
Particles must not affect gameplay state.

### Piece Lock Glow
Short glow effect when a piece locks.

All must be render-only state.

---

# Step 4 — Asset Policy

Prefer:
- No sprites
- Procedural shapes
- Gradients
- Fonts only

If adding fonts:
- Use open-license font
- Place in assets/fonts
- Document license in assets/README.md

Avoid sprite sheets unless absolutely necessary.

---

# Step 5 — Hard Safety Checks

Before finishing:

- Same inputs must produce identical outcomes.
- Score must match previous version exactly.
- Level timing must be identical.
- RNG must behave identically.
- No added gameplay features.

If something feels even slightly different:
Revert.

---

# Step 6 — Deliverables

Provide:

1) Summary of visual changes
2) List of files modified
3) Confirmation that gameplay files were untouched
4) Optional screenshots

---

# Definition of Success

The game must feel:

- Identical in gameplay
- Cleaner
- More modern
- More polished
- More readable
- More visually satisfying

Same Tetris.
Better skin.
Nothing else.