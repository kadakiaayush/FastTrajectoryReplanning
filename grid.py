import random

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[0] * size for i in range(size)]

    def initGrid(self, chanceBlocked):
        for r in range(self.size):
            for c in range(self.size):
                if random.random() < chanceBlocked:
                    self.grid[r][c] = 1

        #Top left, bottom right must be unblocked
        self.grid[0][0], self.grid[self.size-1][self.size-1] = 0, 0
