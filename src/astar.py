import math

from grid import Grid


# Manhattan distance between two squares ignoring obstacles
def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def pathfind_astar(grid: Grid) -> tuple[list[tuple[int, int]] | None, int]:
    start_pos = grid.start_pos()
    end_pos = grid.end_pos()
    # queue for squares to visit
    explore_queue: list[tuple[int, int]] = [start_pos]
    grid_count = grid.grid_count()
    # g-score is cheapest score from square to goal
    g_score = [[math.inf] * grid_count for _ in range(grid_count)]
    g_score[start_pos[0]][start_pos[1]] = 0
    # f-score is how cheap if path
    #   from start to end goes through square
    f_score = [[math.inf] * grid_count for _ in range(grid_count)]
    f_score[start_pos[0]][start_pos[1]] = heuristic(start_pos, end_pos)
    # keep track what square another square came from
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    visit_count = 0
    # while the queue is not empty
    while len(explore_queue) != 0:
        visit_count += 1
        explore_queue.sort(key=lambda s: f_score[s[0]][s[1]])
        # current is node with lowest f-score in explore_queue
        current = explore_queue[0]
        # if goal is reached
        if current == end_pos:
            # return path in reverse order
            path = [current]
            while current in came_from.keys():
                current = came_from[current]
                path.insert(0, current)
            return path, visit_count
        explore_queue.remove(current)
        # set scores for neighboring squares
        neighbors = grid.neighbors(current)
        for neighbor in neighbors:
            tentative_g_score = g_score[current[0]][current[1]] + 1
            if tentative_g_score < g_score[neighbor[0]][neighbor[1]]:
                came_from[neighbor] = current
                g_score[neighbor[0]][neighbor[1]] = tentative_g_score
                f_score[neighbor[0]][neighbor[1]] = \
                    tentative_g_score + heuristic(neighbor, end_pos)
                # add neighbors to queue
                if neighbor not in explore_queue:
                    explore_queue.append(neighbor)
    return None, visit_count
