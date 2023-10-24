from grid import Grid


def pathfind_greedy_first(grid: Grid) -> list[tuple[int, int]] | None:
    start_pos = grid.start_pos()
    end_pos = grid.end_pos()

    def _greedy_recursive(grid, currentCell, path):
        path = path.copy()
        #print("greedy_recursive", currentCell, path)
        path += [currentCell]

        neighbors = grid.neighbors(currentCell)
        #print("     neighbors:",neighbors)
        if end_pos in neighbors:  # win condition
            return path + [end_pos]

        neighbors.sort(key=lambda p: abs(p[0] - end_pos[0]) + abs(p[1] - end_pos[1]))
        #print("     neighbors_sorted:",neighbors)

        for neighbor in neighbors:
            if neighbor not in path:  # Don't get stuck in between two cells
                potential_path = _greedy_recursive(grid, neighbor, path)
                if potential_path is not None:
                    return potential_path
        
        #print("     Stuck")
        return None  # Stuck

    return _greedy_recursive(grid, start_pos, [])
