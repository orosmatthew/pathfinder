import math

from grid import Grid


def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def pathfind_astar(grid: Grid) -> list[tuple[int, int]] | None:
    start_pos = grid.start_pos()
    end_pos = grid.end_pos()

    explore_queue: list[tuple[int, int]] = [start_pos]

    g_score = [[math.inf] * grid.grid_count() for _ in range(grid.grid_count())]
    g_score[start_pos[0]][start_pos[1]] = 0

    f_score = [[math.inf] * grid.grid_count() for _ in range(grid.grid_count())]
    f_score[start_pos[0]][start_pos[1]] = heuristic(start_pos, end_pos)

    came_from: dict[tuple[int, int], tuple[int, int]] = {}

    while not len(explore_queue) == 0:
        # current is node with lowest f-score in explore_queue
        current = explore_queue[0]
        for node in explore_queue:
            if f_score[node[0]][node[1]] < f_score[current[0]][current[1]]:
                current = node

        if current == end_pos:
            path = [current]
            while current in came_from.keys():
                current = came_from[current]
                path.insert(0, current)
            return path

        explore_queue.remove(current)
        neighbors = grid.neighbors(current)
        for neighbor in neighbors:
            tentative_g_score = g_score[current[0]][current[1]]
            if tentative_g_score < g_score[neighbor[0]][neighbor[1]]:
                came_from[neighbor] = current
                g_score[neighbor[0]][neighbor[1]] = tentative_g_score
                f_score[neighbor[0]][neighbor[1]] = tentative_g_score + heuristic(neighbor, end_pos)
                if neighbor not in explore_queue:
                    explore_queue.append(neighbor)

    return None
