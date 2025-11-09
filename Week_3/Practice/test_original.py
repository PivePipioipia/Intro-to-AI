from romania import getHeuristics, createGraph, GBFS, Astar

def calc_cost(path, graph):
    total = 0
    for i in range(len(path) - 1):
        for n, c in graph[path[i]]:
            if n == path[i + 1]:
                total += int(c)
                break
    return total

if __name__ == "__main__":
    heuristics = getHeuristics()
    graph = createGraph()

    startCity = "Arad"
    goalCity = "Hirsova"

    gbfs_path = GBFS(startCity, heuristics, graph, goalCity)
    astar_path = Astar(startCity, heuristics, graph, goalCity)

    print("===== KẾT QUẢ CHƯƠNG TRÌNH BAN ĐẦU =====")
    print("GBFS  → ", gbfs_path)
    print("Chi phí GBFS =", calc_cost(gbfs_path, graph))
    print()
    print("A*    → ", astar_path)
    print("Chi phí A* =", calc_cost(astar_path, graph))
