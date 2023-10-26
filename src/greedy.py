from grid import Grid


def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Implemented based on Wikipedia
# https://en.wikipedia.org/wiki/Best-first_search
def pathfind_greedy_first3(grid: Grid) -> list[tuple[int, int]] | None:
    start_pos = grid.start_pos()
    end_pos = grid.end_pos()
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {start_pos: None}
    queue: list[tuple[int, int]] = [start_pos]
    while len(queue) != 0:
        queue.sort(key=lambda s: heuristic(s, end_pos))
        current_node = queue[0]
        queue.remove(current_node)
        for neighbor in grid.neighbors(current_node):
            if neighbor not in came_from.keys():
                if neighbor == end_pos:
                    path = [end_pos]
                    while current_node in came_from.keys():
                        current_node = came_from[current_node]
                        path.insert(0, current_node)
                    path.pop(0)  # remove start position which is None
                    return path
                else:
                    came_from[neighbor] = current_node
                    queue.append(neighbor)
    return None


# Implemented based on article from Red Blob
# https://www.redblobgames.com/pathfinding/a-star/introduction.html
def pathfind_greedy_first2(grid: Grid) -> list[tuple[int, int]] | None:
    start_pos = grid.start_pos()
    end_pos = grid.end_pos()

    queue: list[tuple[int, int]] = [start_pos]
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {start_pos: None}

    while not len(queue) == 0:
        current = queue[0]
        queue.pop(0)
        if current == end_pos:
            path = [end_pos]
            while current in came_from.keys():
                current = came_from[current]
                path.insert(0, current)
            path.pop(0)  # remove start position which is None
            return path
        for neighbor in grid.neighbors(current):
            if neighbor not in came_from.keys():
                queue.append(neighbor)
                queue.sort(key=lambda square: heuristic(end_pos, square))
                came_from[neighbor] = current
    return None


def pathfind_greedy_first(grid: Grid) -> list[tuple[int, int]] | None:
    start_pos = grid.start_pos()
    end_pos = grid.end_pos()

    def _greedy_recursive(grid, currentCell, path):
        path = path.copy()
        # print("greedy_recursive", currentCell, path)
        path += [currentCell]

        neighbors = grid.neighbors(currentCell)
        # print("     neighbors:",neighbors)
        if end_pos in neighbors:  # win condition
            return path + [end_pos]

        neighbors.sort(key=lambda p: abs(p[0] - end_pos[0]) + abs(p[1] - end_pos[1]))
        # print("     neighbors_sorted:",neighbors)

        for neighbor in neighbors:
            if neighbor not in path:  # Don't get stuck in between two cells
                potential_path = _greedy_recursive(grid, neighbor, path)
                if potential_path is not None:
                    return potential_path

        # print("     Stuck")
        return None  # Stuck

    return _greedy_recursive(grid, start_pos, [])
