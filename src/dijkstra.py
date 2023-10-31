# //Dijkstra’s algorithm for single-source the shortest paths
# //Input: A weighted connected graph G = 〈V , E〉 with non-negative weights
# // and its vertex s
# //Output: The length d v of the shortest path from s to v
# // and its penultimate vertex p v for every vertex v in V
# Initialize(Q) //initialize priority queue to empty
# for every vertex v in V
# d v ← ∞; p v ← null
# Insert(Q, v, d v ) //initialize vertex priority in the priority queue
# ds ← 0; Decrease(Q, s, d s ) //update priority of s with d s
# VT ← ∅
# for i ← 0 to |V | − 1 do
# u∗ ← DeleteMin(Q) //delete the minimum priority element
# V T ← V T ∪ {u∗ }
# for every vertex u in V − V T that is adjacent to u∗ do
# if du∗ + w(u∗, u) < du
# du ← d u∗ + w(u∗, u); p u ← u∗
# Decrease(Q, u, d u )

# For a given source, find the shortest path to all other vertices
# v = nearest vertex,
# u = adjacent/fringe vertices,
# d = length of shortest path to v,
# s = source vertex
# G = graph of nodes
# Each vertex is labeled with d, and its parent.
# Next nearest vertex n is found by looking for
# the fringe vertex with the smallest d.
# Once n is found: 1) add n to the path/tree.
# 2) update the u's of vertices connected to n (that are farther away from s).
# Assume V is all the vertices, and E is all their weighted edges
import math
from grid import Grid


def pathfind_dijkstra(grid: Grid) -> list[tuple[int, int]] | None:
    start_pos = grid.start_pos()
    end_pos = grid.end_pos()
    explore_queue: list[tuple[int, int]] = [start_pos]
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    grid_count = grid.grid_count()
    weight = [[math.inf] * grid_count for _ in range(grid_count)]
    weight[start_pos[0]][start_pos[1]] = 0

    while not len(explore_queue) == 0:
        current = explore_queue[0]
        for node in explore_queue:  # Explore
            weight_node = weight[node[0]][node[1]]
            weight_current = weight[current[0]][current[1]]
            if weight_node < weight_current:
                current = node

        if current == end_pos:  # Determine path
            path = [current]
            while current in came_from.keys():
                current = came_from[current]
                path.insert(0, current)
            return path

        explore_queue.remove(current)
        neighbors = grid.neighbors(current)
        for neighbor in neighbors:
            temp_weight = weight[current[0]][current[1]] + 1
            if temp_weight < weight[neighbor[0]][neighbor[1]]:
                came_from[neighbor] = current
                weight[neighbor[0]][neighbor[1]] = temp_weight
                weight[neighbor[0]][neighbor[1]] = temp_weight
                if neighbor not in explore_queue:
                    explore_queue.append(neighbor)

    return None

#     #For 1 - initialize a queue of vertices
#     #For 2 - delete minimum ......
#     #For 3 - if there is a lower weight path, then take it?...
