from grid import Grid


# Manhattan distance between two squares ignoring obstacles
def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def pathfind_greedy_first(grid: Grid) -> tuple[list[tuple[int, int]] | None, int]:
    start_pos = grid.start_pos()
    end_pos = grid.end_pos()
    # keep track what square another square came from
    came_from = {start_pos: None}
    # queue of squares to visit
    queue: list[tuple[int, int]] = [start_pos]
    visit_count = 0
    # while the queue is not empty
    while len(queue) != 0:
        visit_count += 1
        queue.sort(key=lambda s: heuristic(s, end_pos))
        # remove square with the 
        #   lowest heuristic from queue
        current = queue[0]
        queue.pop(0)
        # loop through all neighbors
        for neighbor in grid.neighbors(current):
            if neighbor not in came_from:
                # end is found
                if neighbor == end_pos:
                    # return reverse of path
                    path = [neighbor, current]
                    while current := came_from[current]:
                        path.append(current)
                    path.reverse()
                    return path, visit_count
                else:
                    # add neighbors to queue
                    came_from[neighbor] = current
                    queue.append(neighbor)
    return None, visit_count
