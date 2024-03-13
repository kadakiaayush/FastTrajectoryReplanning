from grid import Grid
from searchAlgos import forwardA, backwardA
from statistics import mean
from collections import deque
import time


#BFS-search to verify path exists
def checkPath(grid):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  #right, left, down, up
    start, end = (0, 0), (grid.size-1, grid.size-1)

    queue, visited = deque(), set()

    queue.append(start)
    visited.add(start)

    while queue:
        curr = queue.popleft()

        #Agent reached the target
        if curr == end:
            return True  #Path found

        x, y = curr

        #Check all four directions
        for dirX, dirY in directions:
            new_x, new_y = x + dirX, y + dirY

            #Check if not blocked
            if 0 <= new_x < grid.size and 0 <= new_y < grid.size:
                if grid.grid[new_x][new_y] == 0 and (
                    new_x, new_y) not in visited:
                    queue.append((new_x, new_y))
                    visited.add((new_x, new_y))

    return False  #No path found


gridWorlds = []
timesForwardASmall, timesForwardALarge, timesBack = [], [], []
totalCellsASmall, totalCellsALarge, totalCellsBack = 0, 0, 0

#Generate 50 gridworlds
for i in range(50):
    while True:
        grid = Grid(101)
        grid.initGrid(0.3)

        #Check that path exists and grid is valid:
        if checkPath(grid):
            gridWorlds.append(grid)
            break

fileForwardASmall = open("outForwardASmall.txt", "w")
fileForwardALarge = open("outForwardALarge.txt", "w")
fileBackward = open("outBackward.txt", "w")

for i in range(len(gridWorlds)):
    grid = gridWorlds[i]

    #Forward A with tie break for smaller g-values
    start = time.time()
    pathForwardASmall, cellsForwardASmall = forwardA(gridWorlds[i], True)
    timesForwardASmall.append(time.time() - start)
    totalCellsASmall += cellsForwardASmall

    #Forward A with tie break for larger g-values
    start = time.time()
    pathForwardALarge, cellsForwardALarge = forwardA(gridWorlds[i], False)
    timesForwardALarge.append(time.time() - start)
    totalCellsALarge += cellsForwardALarge

    #Backward A with tie break for larger g-values
    start = time.time()
    pathBackward, cellsBackward = backwardA(gridWorlds[i])
    timesBack.append(time.time() - start)
    totalCellsBack += cellsBackward

    #Write the ouput grid to the file
    fileForwardASmall.write("Output Grid #" + str((i+1)) + ":\n")
    for r in range(grid.size):
        for c in range(grid.size):
            if (r, c) in pathForwardASmall:
                fileForwardASmall.write("  ")
            else:
                fileForwardASmall.write(str(grid.grid[r][c]) + " ")
        fileForwardASmall.write("\n")
    fileForwardASmall.write("\n")

    #Write the ouput grid to the file
    fileForwardALarge.write("Output Grid #" + str((i+1)) + ":\n")
    for r in range(grid.size):
        for c in range(grid.size):
            if (r, c) in pathForwardALarge:
                fileForwardALarge.write("  ")
            else:
                fileForwardALarge.write(str(grid.grid[r][c]) + " ")
        fileForwardALarge.write("\n")
    fileForwardALarge.write("\n")

    #Write the ouput grid to the file
    fileBackward.write("Output Grid #" + str((i+1)) + ":\n")
    for r in range(grid.size):
        for c in range(grid.size):
            if (r, c) in pathBackward:
                fileBackward.write("  ")
            else:
                fileBackward.write(str(grid.grid[r][c]) + " ")
        fileBackward.write("\n")
    fileBackward.write("\n")

fileForwardASmall.close()
fileForwardALarge.close()
fileBackward.close()

print("Average time for forwardASmall: ", round(mean(timesForwardASmall), 7),
      "s, with", (totalCellsASmall/50), "average cells.")
print("Average time for forwardALarge: ", round(mean(timesForwardALarge), 7),
      "s, with", (totalCellsALarge/50), "average cells.")
print("Average time for backwardA:     ", round(mean(timesBack), 7),
      "s, with", (totalCellsBack/50), "average cells.")

