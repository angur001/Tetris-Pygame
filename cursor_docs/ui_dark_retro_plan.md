## Dark Retro Tetris UI Plan (UI-Only, Logic Frozen)

### 1. Goals & Constraints
- **Goals**
  - Dark, retro-arcade vibe: deep background, neon accents, CRT-ish feel.
  - Cleaner, more modern layout while staying true to classic Tetris.
  - Strong readability for board, next piece, score, and level.
- **Hard constraints**
  - **No gameplay logic changes**: movement, gravity, rotations, collision, scoring, RNG, input, timings all remain identical.
  - All changes are **rendering-only**: colors, shapes, fonts, layout, visual effects.
  - Primary work happens in `displays.py` and new `ui/` modules.

---

### 2. File & Module Structure
- **Existing**
  - `displays.py` – main render entry point.
- **New UI modules** (render-only)
  - `ui/theme.py`
    - Define dark-retro color palette(s): background, panel, grid, block colors, text colors, outline/shadow colors.
    - Optional: allow switching between themes (e.g., DARK_RETRO, NEON, PASTEL) via constants.
  - `ui/layout.py`
    - Screen/layout constants: margins, paddings, panel sizes, block size reference (uses `Displays.CELL_SIZE`).
    - Computed positions: board rect, next-piece panel rect, HUD text anchors.
  - `ui/draw.py`
    - `draw_background(surface, theme)`
    - `draw_playfield(surface, game, layout, theme)`
    - `draw_block(surface, x, y, size, color, theme)` (rounded, beveled, shadow).
    - `draw_panel(surface, rect, theme, title=None)`
    - `draw_text(surface, text, font, color, pos, align)`
  - `ui/effects.py` (optional; purely visual)
    - Hooks for line-clear flash, subtle glow, or particles, driven by info passed from game (no extra logic decisions).

`displays.py` will be refactored to call these helpers; it will not change gameplay state or behavior.

---

### 3. Visual Theme – Dark Retro
- **Background**
  - Very dark bluish/purplish base (`#050714` / `#080b1e` style).
  - Vertical or radial gradient from deep purple at top to near-black at bottom.
  - Optional subtle noise or vignette overlay for CRT/arcade feel (alpha-only, precomputed surface).
- **Grid & Panels**
  - Playfield framed with a bright neon outline (e.g., cyan or magenta) plus a subtle outer glow.
  - Interior grid lines: faint, low alpha lines to hint at cells without overpowering blocks.
  - Panels (Next piece, Score, Level, Lines):
    - Dark panel background slightly lighter than global background.
    - Rounded corners with a 1–2 px lighter border and a subtle drop shadow.
- **Blocks**
  - Keep distinct colors per tetromino but shift to neon-tinted palette on dark background.
  - For each block:
    - Rounded rect (`border_radius`) with:
      - Thin, darker border.
      - Slight top-left highlight strip (lighter version of color).
      - Subtle inner gradient or faux bevel (lighter top, darker bottom).
    - Optional stack shadow: faint darker strip at bottom of the board to suggest weight.
- **Typography**
  - Prefer a pixel/retro font (if available under `assets/fonts`), else pygame default.
  - Color scheme:
    - Titles/headings: bright neon (e.g., cyan or magenta).
    - Values (score, level): high-contrast light color (off-white).
  - Consistent hierarchy:
    - Game title (if drawn) > section headers (Next, Score, Level) > values.

---

### 4. Layout Plan
- **Playfield**
  - Slightly left-of-center to make room for a right-hand info column.
  - Use `ui/layout.py` to compute:
    - `PLAYFIELD_RECT` from `Displays.CELL_SIZE`, `GameState.WIDTH`, `GameState.HEIGHT`.
    - Keep the existing logical grid dimensions; only shift pixel positions.
- **Right Column Panels**
  - From top to bottom on the right side:
    - "Next" panel (next piece preview).
    - Score panel.
    - Level + lines panel (or combined HUD panel).
  - Consistent width, padding, and spacing between panels.
- **Bottom / Misc HUD**
  - Optional small text hints for controls at bottom or top-left, in muted color.
  - Ensure they do not overlap the board or interfere with gameplay.

---

### 5. Rendering Refactor Steps
1. **Introduce theme & layout modules**
   - Create `ui/theme.py` with dark-retro palette constants.
   - Create `ui/layout.py` with computed rects for board and panels.
2. **Add drawing helpers**
   - Implement `draw_background`, `draw_panel`, `draw_block`, `draw_text` in `ui/draw.py`.
3. **Wire into `displays.py`**
   - Replace raw `pygame.draw.rect` calls for:
     - Board cells → `draw_block`.
     - Next piece panel background and border → `draw_panel` + `draw_block` for cells.
   - Add background drawing at frame start using `draw_background`.
   - Move all direct color literals into `ui/theme.py`.
4. **Align layout using layout constants**
   - Use `ui/layout.py` to compute:
     - Board origin (top-left).
     - Panel rects for Next/Score/Level/Lines.
   - Ensure no changes to how many cells are drawn or where gameplay thinks they are; only pixel placement of visuals changes.

---

### 6. Retro “Juice” (Safe Visual Effects)
- **Line-clear flash (optional)**
  - When the environment reports non-zero `lines_cleared` (already available via info in RL; for manual mode may need a passive flag passed in from existing logic without changing decisions):
    - Draw a brief white/bright overlay with low alpha fading out over a few frames.
    - Implement state in `ui/effects.py` managed only by renderer.
- **Piece lock glow (optional)**
  - Short-lived glow around the stack when a piece locks (triggered by a non-invasive flag tied to update events, not logic).
- **Background pulse (very subtle)**
  - Slight variation of gradient offset or brightness based on time, not gameplay.

All of the above must **not** change timings, decisions, or physics—only visuals.

---

### 7. Implementation Order
1. **Phase 1 – Theme & Background**
   - Implement `ui/theme.py` and `ui/layout.py`.
   - Add gradient background and vignette.
   - Verify game still behaves identically (only looks different).
2. **Phase 2 – Blocks & Grid**
   - Swap to new `draw_block` with rounded, beveled neon blocks.
   - Add faint grid lines and stronger outer frame.
3. **Phase 3 – Panels & HUD**
   - Implement right-side panels with rounded rectangles and shadows.
   - Style "Next", "Score", "Level", "Lines" text with retro colors and consistent fonts.
4. **Phase 4 – Optional Effects**
   - Add line-clear flash and subtle glow/particles in `ui/effects.py`.
   - Carefully test to ensure no gameplay behavior change.

---

### 8. Verification Checklist
- Same key inputs result in the same piece movements, timings, and outcomes.
- Scores, levels, and line counts match pre-UI-change behavior.
- Random sequences of pieces are unchanged.
- No added input behaviors or gameplay-affecting state.
- Visual changes:
  - Dark background with retro gradient and vignette.
  - Neon-styled blocks with rounded corners and highlights.
  - Clean right-side HUD panels for next piece and stats.
  - Consistent typography and spacing.

