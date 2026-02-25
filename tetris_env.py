import numpy as np
from cell import Cell
from shape import Shape
from gameState import GameState

SHAPE_NAMES = list(Shape.SHAPES.keys())
NUM_FEATURES = 4
FEATURE_NORMS = np.array([4.0, 200.0, 50.0, 40.0], dtype=np.float32)


class TetrisEnv:
    NUM_ROTATIONS = 4
    NUM_COLUMNS = GameState.WIDTH
    NUM_ACTIONS = NUM_ROTATIONS * NUM_COLUMNS  # 40

    def __init__(self):
        self.game = None
        self.reset()

    def reset(self):
        self.game = GameState()
        self.game.removeShadow()
        return self.get_afterstates()

    # ------------------------------------------------------------------
    # Lightweight placement simulation (no GameState.clone needed)
    # ------------------------------------------------------------------

    def _occupied_cells(self, raw):
        return [(i, j) for i in range(4) for j in range(4) if raw[i][j] != 0]

    def _simulate_placement(self, rotation, grid_col):
        """Simulate placing the current piece; return (lines_cleared, grid_copy)."""
        grid = [row[:] for row in self.game.gameGrid]
        shape = self.game.currentShape
        raw = Shape.SHAPES[shape.name][rotation]
        occupied = self._occupied_cells(raw)
        min_j = min(j for _, j in occupied)
        min_i = min(i for i, _ in occupied)

        x = grid_col - min_j
        y = -min_i

        while True:
            can_drop = True
            for ci, cj in occupied:
                ny, gx = y + ci + 1, x + cj
                if ny >= self.game.HEIGHT:
                    can_drop = False
                    break
                if ny >= 0 and grid[ny][gx] != Cell.Empty:
                    can_drop = False
                    break
            if not can_drop:
                break
            y += 1

        color = shape.color
        for ci, cj in occupied:
            gy, gx = y + ci, x + cj
            if 0 <= gy < self.game.HEIGHT:
                grid[gy][gx] = color

        lines_cleared = 0
        write = self.game.HEIGHT - 1
        for i in range(self.game.HEIGHT - 1, -1, -1):
            if all(grid[i][j] != Cell.Empty for j in range(self.game.WIDTH)):
                lines_cleared += 1
                continue
            if write != i:
                grid[write] = grid[i][:]
            write -= 1
        for i in range(write, -1, -1):
            grid[i] = [Cell.Empty] * self.game.WIDTH

        return lines_cleared, grid

    def _compute_features(self, grid, lines_cleared):
        heights = [0] * self.game.WIDTH
        for j in range(self.game.WIDTH):
            for i in range(self.game.HEIGHT):
                if grid[i][j] != Cell.Empty:
                    heights[j] = self.game.HEIGHT - i
                    break

        aggregate_height = sum(heights)

        holes = 0
        for j in range(self.game.WIDTH):
            found = False
            for i in range(self.game.HEIGHT):
                if grid[i][j] != Cell.Empty:
                    found = True
                elif found:
                    holes += 1

        bumpiness = sum(
            abs(heights[j] - heights[j + 1]) for j in range(self.game.WIDTH - 1)
        )

        raw_feats = np.array(
            [lines_cleared, aggregate_height, holes, bumpiness], dtype=np.float32
        )
        return raw_feats / FEATURE_NORMS

    # ------------------------------------------------------------------
    # Valid actions & afterstate generation
    # ------------------------------------------------------------------

    def get_valid_actions(self):
        mask = np.zeros(self.NUM_ACTIONS, dtype=bool)
        shape = self.game.currentShape
        if shape is None:
            return mask

        for rotation in range(self.NUM_ROTATIONS):
            raw = Shape.SHAPES[shape.name][rotation]
            occupied = self._occupied_cells(raw)
            if not occupied:
                continue

            min_j = min(j for _, j in occupied)
            max_j = max(j for _, j in occupied)
            min_i = min(i for i, _ in occupied)
            max_col = self.game.WIDTH - (max_j - min_j + 1)

            for grid_col in range(max_col + 1):
                x = grid_col - min_j
                y = -min_i
                overlap = False
                for ci, cj in occupied:
                    gy, gx = y + ci, x + cj
                    if 0 <= gy < self.game.HEIGHT and 0 <= gx < self.game.WIDTH:
                        if self.game.gameGrid[gy][gx] != Cell.Empty:
                            overlap = True
                            break
                if not overlap:
                    mask[rotation * self.NUM_COLUMNS + grid_col] = True
        return mask

    def get_afterstates(self):
        """Return [(action_idx, feature_vector), ...] for every valid placement."""
        mask = self.get_valid_actions()
        afterstates = []
        for action in np.where(mask)[0]:
            rotation = action // self.NUM_COLUMNS
            grid_col = action % self.NUM_COLUMNS
            lines, grid = self._simulate_placement(rotation, grid_col)
            afterstates.append((int(action), self._compute_features(grid, lines)))
        return afterstates

    # ------------------------------------------------------------------
    # Step
    # ------------------------------------------------------------------

    def step(self, action):
        rotation = action // self.NUM_COLUMNS
        grid_col = action % self.NUM_COLUMNS

        shape = self.game.currentShape
        raw = Shape.SHAPES[shape.name][rotation]
        occupied = self._occupied_cells(raw)
        min_j = min(j for _, j in occupied)
        min_i = min(i for i, _ in occupied)

        shape.matrix = shape.mapRawMatrixToColor(raw)
        shape.rotation_index = rotation
        shape.x = grid_col - min_j
        shape.y = -min_i

        while self._can_move_down():
            shape.y += 1

        self.game.updateGameGrid()

        old_lines = self.game.totalLinesCleared
        self.game.checkForLines()
        lines_cleared = self.game.totalLinesCleared - old_lines

        reward = lines_cleared ** 2  # 0, 1, 4, 9, 16

        self.game.currentShape = self.game.nextShape
        self.game.nextShape = Shape.generateRandomShape(
            self.game.WIDTH // 2 - 1, -4
        )

        afterstates = self.get_afterstates()
        done = len(afterstates) == 0
        if done:
            reward -= 2.0

        info = {
            "score": self.game.score,
            "lines": self.game.totalLinesCleared,
            "lines_cleared": lines_cleared,
        }
        return afterstates, reward, done, info

    def _can_move_down(self):
        shape = self.game.currentShape
        for j in range(4):
            for i in range(3, -1, -1):
                if shape.matrix[i][j] != Cell.Empty:
                    ny = shape.y + i + 1
                    gx = shape.x + j
                    if ny >= self.game.HEIGHT:
                        return False
                    if ny >= 0 and self.game.gameGrid[ny][gx] != Cell.Empty:
                        return False
                    break
        return True
