# --- Chương trình tìm đường đi từ Arad đến Hirsova bằng GBFS và A* ---

import queue
import matplotlib.pyplot as plt


def getHeuristics(filename="heuristics.txt"):
    heuristics = {}
    with open(filename) as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2:
                heuristics[parts[0]] = int(parts[1])
    return heuristics


def getCity(filename="cities.txt"):
    city = {}
    citiesCode = {}
    with open(filename) as f:
        j = 1
        for line in f:
            parts = line.split()
            if len(parts) == 3:
                city[parts[0]] = [int(parts[1]), int(parts[2])]
                citiesCode[j] = parts[0]
                j += 1
    return city, citiesCode


def createGraph(filename="citiesGraph.txt"):
    graph = {}
    with open(filename) as f:
        for line in f:
            parts = line.split()
            if len(parts) == 3:
                a, b, cost = parts[0], parts[1], int(parts[2])
                graph.setdefault(a, []).append((b, cost))
                graph.setdefault(b, []).append((a, cost))
    return graph


def GBFS(startNode, heuristics, graph, goalNode="Bucharest"):
    open_list = queue.PriorityQueue()
    open_list.put((heuristics[startNode], startNode))
    closed = set()
    parent = {}
    total_cost = 0

    while not open_list.empty():
        _, current = open_list.get()

        if current in closed:
            continue
        closed.add(current)

        if current == goalNode:
            break

        for neighbor, cost in graph[current]:
            if neighbor not in closed:
                open_list.put((heuristics[neighbor], neighbor))
                parent[neighbor] = current

    # reconstruct path
    path = [goalNode]
    while path[-1] != startNode:
        path.append(parent[path[-1]])
    path.reverse()

    # compute total path cost
    for i in range(len(path) - 1):
        for nb, c in graph[path[i]]:
            if nb == path[i + 1]:
                total_cost += c

    return path, total_cost


def Astar(startNode, heuristics, graph, goalNode="Bucharest"):
    open_list = queue.PriorityQueue()
    open_list.put((heuristics[startNode], startNode))
    g_cost = {startNode: 0}
    parent = {}
    closed = set()

    while not open_list.empty():
        _, current = open_list.get()

        if current in closed:
            continue
        closed.add(current)

        if current == goalNode:
            break

        for neighbor, cost in graph[current]:
            tentative_g = g_cost[current] + cost
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                f_val = tentative_g + heuristics[neighbor]
                open_list.put((f_val, neighbor))
                parent[neighbor] = current

    # reconstruct path
    path = [goalNode]
    while path[-1] != startNode:
        path.append(parent[path[-1]])
    path.reverse()

    total_cost = g_cost[goalNode]
    return path, total_cost



def drawMap(city, gbfs, astar, graph):
    # vẽ toàn bộ các cạnh xám
    for name, coord in city.items():
        plt.plot(coord[0], coord[1], "ro")
        plt.annotate(name, (coord[0] + 5, coord[1]))
        for neighbor, _ in graph[name]:
            n_coord = city[neighbor]
            plt.plot([coord[0], n_coord[0]], [coord[1], n_coord[1]], "gray")

    def draw_path(path, color, label):
        for i in range(len(path) - 1):
            if path[i] in city and path[i + 1] in city:
                c1, c2 = city[path[i]], city[path[i + 1]]
                plt.plot([c1[0], c2[0]], [c1[1], c2[1]], color=color, linewidth=2)
        plt.plot([], [], color=color, label=label)

    draw_path(gbfs, "green", "GBFS")
    draw_path(astar, "blue", "A*")

    plt.legend(loc="lower left")
    plt.title("Kết quả tìm đường GBFS và A* trên bản đồ Romania")
    plt.show()



if __name__ == "__main__":
    heuristics = getHeuristics()
    graph = createGraph()
    city, citiesCode = getCity()

    print("\n===== DANH SÁCH THÀNH PHỐ =====")
    for i, j in citiesCode.items():
        print(f"{i:>2} : {j}")
    print("Nhập 0 để thoát.\n")

    while True:
        try:
            inputCode1 = int(input("Nhập đỉnh bắt đầu: "))
            inputCode2 = int(input("Nhập đỉnh kết thúc: "))
            if inputCode1 == 0 or inputCode2 == 0:
                break

            startCity = citiesCode[inputCode1]
            endCity = citiesCode[inputCode2]

            gbfs_path, gbfs_cost = GBFS(startCity, heuristics, graph, endCity)
            astar_path, astar_cost = Astar(startCity, heuristics, graph, endCity)

            print("\n===== KẾT QUẢ SAU KHI SỬA CHƯƠNG TRÌNH =====")
            print(f"GBFS → {gbfs_path}")
            print(f"Chi phí GBFS = {gbfs_cost}")
            print()
            print(f"A*   → {astar_path}")
            print(f"Chi phí A* = {astar_cost}")
            print("=" * 60)

            drawMap(city, gbfs_path, astar_path, graph)

        except KeyError:
            print("Mã thành phố không hợp lệ. Vui lòng nhập lại!\n")
        except Exception as e:
            print(f"Lỗi: {e}")
