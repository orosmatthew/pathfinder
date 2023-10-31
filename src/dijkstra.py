import math
from grid import Grid


def pathfind_dijkstra(grid: Grid) -> list[tuple[int, int]] | None:
    start_pos = grid.start_pos()
    end_pos = grid.end_pos()
    # queue of squares to traverse
    explore_queue: list[tuple[int, int]] = [start_pos]
    # keep track what square another square came from
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    grid_count = grid.grid_count()
    weight = [[math.inf] * grid_count for _ in range(grid_count)]
    weight[start_pos[0]][start_pos[1]] = 0
    # loop until queue is empty
    while len(explore_queue) != 0:
        # sort queue according to lowest weight
        explore_queue.sort(key=lambda s: weight[s[0]][s[1]])
        # remove square with lowest weight from queue
        current = explore_queue[0]
        explore_queue.pop(0)
        # end is reached
        if current == end_pos:
            # return reverse of path
            path = [current]
            while current in came_from.keys():
                current = came_from[current]
                path.insert(0, current)
            return path
        # loop through all neighbors of current square
        neighbors = grid.neighbors(current)
        for neighbor in neighbors:
            temp_weight = weight[current[0]][current[1]] + 1
            if temp_weight < weight[neighbor[0]][neighbor[1]]:
                came_from[neighbor] = current
                weight[neighbor[0]][neighbor[1]] = temp_weight
                # add neighbors to queue
                if neighbor not in explore_queue:
                    explore_queue.append(neighbor)
    return None
