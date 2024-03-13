import heapq

def manhattanD(cell, end):
    #sum of the absolute difference of the x coordinates and the absolute
    #difference of the y coordinates of the cell and the cell in the end
    return abs(end[0] - cell[0]) + abs(end[1] - cell[1])


def forwardA(grid, favorSmallG):
    start = (0, 0)
    end = (grid.size-1, grid.size-1)
    openList = [] #cells to be expanded
    closedList = set() #list of already expanded cells
    gVals = {} #cost from start to end
    fVals = {} #total cost
    parent = {} #preveous cells

    #Turn the open list into binary heap, push the start cell to it
    heapq.heappush(openList, (manhattanD(start, end), start))

    gVals[start] = 0
    fVals[start] = manhattanD(start, end)

    while openList:
        #Pop the highest priority cell from the heap
        current = heapq.heappop(openList)[1]

        #If reached the end, return the final path and the total number of
        #the cells that were expanded and explored for evaluation; the path is
        #reconstructed by following the chain of parent cells and reversing it
        if current == end:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)

            return path[::-1], len(closedList) #+ len(openList)

        closedList.add(current)

        #Get the neighbor cells: bottom, top, right, left
        neighbors = [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                     (current[0], current[1] + 1), (current[0], current[1] - 1)]

        for neighbor in neighbors:
            #Make sure the neighbor cell isn't blocked or outside grid
            if neighbor[0] < 0 or neighbor[0] >= grid.size:
                continue
            if neighbor[1] < 0 or neighbor[1] >= grid.size:
                continue
            if grid.grid[neighbor[0]][neighbor[1]] == 1:
                continue
            #Skip the already evaluated cells
            if neighbor in closedList:
                continue

            #Add a cost of 1 step from the parent cell to current g-value
            #and calculate f-value by adding the manhattan distance
            new_g = gVals[current] + 1
            new_f = new_g + manhattanD(neighbor, end)

            #Based on the tie-breaking strategy, push the neighbor to the heap
            #and update g- and f-values if better path;
            #f-value is compared first, then g-value is compared afterwards;
            #in a tie a new g-value is compared to the previous of neighbor
            if favorSmallG:
                if neighbor not in gVals or new_f < fVals[neighbor] or (
                    new_f == fVals[neighbor] and new_g < gVals[neighbor]):
                    if neighbor not in gVals:
                        parent[neighbor] = current
                        gVals[neighbor] = new_g
                        fVals[neighbor] = new_g + manhattanD(neighbor, start)

                        #Push the new favorite neighbor cell to the heap
                        heapq.heappush(openList, (fVals[neighbor], neighbor))
                    else:
                        parent[neighbor] = current
                        gVals[neighbor] = new_g
                        fVals[neighbor] = new_g + manhattanD(neighbor, start)
            else:
                #if neighbor not in gVals or new_g > gVals[neighbor]:
                if neighbor not in gVals or new_f < fVals[neighbor] or (
                    new_f == fVals[neighbor] and new_g > gVals[neighbor]):
                    if neighbor not in gVals:
                        parent[neighbor] = current
                        gVals[neighbor] = new_g
                        fVals[neighbor] = new_g + manhattanD(neighbor, end)

                        #Push the new favorite neighbor cell to the heap
                        heapq.heappush(openList, (fVals[neighbor], neighbor))
                    else:
                        parent[neighbor] = current
                        gVals[neighbor] = new_g
                        fVals[neighbor] = new_g + manhattanD(neighbor, end)

    return None, len(closedList) #+ len(openList)


def backwardA(grid):
    start = (0, 0)
    end = (grid.size-1, grid.size-1)
    openList = [] #cells to be expanded
    closedList = set() #list of already expanded cells
    gVals = {} #cost from start to end
    fVals = {} #total cost
    parent = {} #preveous cells

    #Turn the open list into binary heap, push the end goal cell to it
    heapq.heappush(openList, (manhattanD(start, end), end))

    gVals[end] = 0
    fVals[end] = manhattanD(start, end)

    while openList:
        #Pop the highest priority cell from the heap
        current = heapq.heappop(openList)[1]

        #If reached the start, return the final path and the total number of
        #the cells that were expanded and explored for evaluation; the path is
        #reconstructed by following the chain of parent cells
        if current == start:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(end)
            #return path[::-1], len(closedList) + len(openList)
            return path, len(closedList) #+ len(openList)

        closedList.add(current)

        #Get the neighbor cells: bottom, top, right, left
        neighbors = [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                     (current[0], current[1] + 1), (current[0], current[1] - 1)]

        for neighbor in neighbors:
            #Make sure the neighbor cell isn't blocked or outside grid
            if neighbor[0] < 0 or neighbor[0] >= grid.size:
                continue
            if neighbor[1] < 0 or neighbor[1] >= grid.size:
                continue
            if grid.grid[neighbor[0]][neighbor[1]] == 1:
                continue
            #Skip the already evaluated cells
            if neighbor in closedList:
                continue

            #Add a cost of 1 step from the parent cell to current g-value
            #and calculate f-value by adding the manhattan distance
            new_g = gVals[current] + 1
            new_f = new_g + manhattanD(neighbor, end)


            #Update g- and f-values if better path
            if neighbor not in gVals or new_f < fVals[neighbor] or (
                new_f == fVals[neighbor] and new_g < gVals[neighbor]):
                parent[neighbor] = current
                gVals[neighbor] = new_g
                fVals[neighbor] = new_g + manhattanD(neighbor, start)

                #Push the new favorite neighbor cell to the heap
                heapq.heappush(openList, (fVals[neighbor], neighbor))

    return None, len(closedList) #+ len(openList)
