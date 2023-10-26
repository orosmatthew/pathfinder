from queue import PriorityQueue

from grid import Grid


def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def pathfind_greedy_first(grid: Grid) -> list[tuple[int, int]] | None:
    start_pos = grid.start_pos()
    end_pos = grid.end_pos()

    visited = {start_pos: None}
    queue = PriorityQueue()

    queue.put((heuristic(start_pos, end_pos), start_pos))

    while not queue.empty():
        current_node = queue.get()[1]
        for neighbor in grid.neighbors(current_node):
            if neighbor not in visited:
                if neighbor == end_pos:
                    path = [neighbor, current_node]
                    while current_node := visited[current_node]:
                        path.append(current_node)
                    path.reverse()
                    return path
                else:
                    visited[neighbor] = current_node
                    queue.put((heuristic(neighbor, end_pos), neighbor))
    return None
