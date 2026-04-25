EMPTY = 0
WALL = 9


class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY] * cols for _ in range(rows)]

    def load(self, grid_data):
        for r, row in enumerate(grid_data):
            for c, val in enumerate(row):
                self.grid[r][c] = val

    def get(self, row, col):
        return self.grid[row][col]

    def set(self, row, col, value):
        self.grid[row][col] = value

    def is_wall(self, row, col):
        return self.grid[row][col] == WALL

    def is_empty(self, row, col):
        return self.grid[row][col] == EMPTY

    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
