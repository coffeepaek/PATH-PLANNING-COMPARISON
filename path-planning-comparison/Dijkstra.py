INF = 0xFFFF
n, m = map(int, input().split())

# 가중치 인접 행렬 초기화
W = [[0 if i == j else INF for i in range(n)] for j in range(n)]

for _ in range(m):
    u, v, w = map(int, input().split())
    W[u][v] = w

# 출발 노드와 도착 노드 입력
s, t = map(int, input().split())


def dijkstra_run(start, n, W):
    parent = [start for _ in range(n)]           # 각 노드로 오기 직전 노드 저장
    dist = [W[start][i] for i in range(n)]       # 시작점에서 각 노드까지 거리

    for _ in range(n - 1):
        u = pick_nearest(start, dist)            # 가장 가까운 정점 선택

        for v in range(n):
            if dist[v] > dist[u] + W[u][v]:
                dist[v] = dist[u] + W[u][v]
                parent[v] = u
        dist[u] = -1  # 방문 처리
    return parent,dist


def restore_path(start, target, parent):
    # 경로를 재귀적으로 복원
    if parent[target] == start:
        return [start, target]
    else:
        return restore_path(start, parent[target], parent) + [target]


def pick_nearest(start, dist):
    minimum, u = INF, start
    for v in range(len(dist)):
        if v == start:
            continue
        if 0 <= dist[v] < minimum:
            minimum = dist[v]
            u = v
    return u

    # --- 추가: 경로 시각화 (matplotlib) ---
def visualize_path(W, path, INF=0xFFFF):
    import math
    import matplotlib.pyplot as plt

    n = len(W)

    # 노드 배치: 단순 원형 레이아웃
    pos = [(math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n)) for i in range(n)]

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    # 간선(전체 그래프)
    for i in range(n):
        for j in range(n):
            if i != j and W[i][j] != INF:
                x1, y1 = pos[i]
                x2, y2 = pos[j]
                ax.annotate(
                    "", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", lw=1)  # 방향 그래프 기준
                )
                # 가중치 라벨
                ax.text((x1+x2)/2, (y1+y2)/2, str(W[i][j]), fontsize=9, ha="center", va="center")

    # 노드
    xs = [p[0] for p in pos]
    ys = [p[1] for p in pos]
    ax.scatter(xs, ys, s=300)
    for i, (x, y) in enumerate(pos):
        ax.text(x, y, str(i), fontsize=10, ha="center", va="center", weight="bold")

    # 최단경로 강조
    if path and len(path) > 1:
        for a, b in zip(path, path[1:]):
            x1, y1 = pos[a]
            x2, y2 = pos[b]
            ax.plot([x1, x2], [y1, y2], lw=4)  # 굵게만 표시(최단경로)

    plt.title("Shortest Path")
    plt.show()



if __name__ == "__main__":
    parent,dist = dijkstra_run(s, n, W)
    dist_total = 0

    if dist[t] == INF:
        print("Unreachable")              # 도달 불가
    
    else:
        path = restore_path(s, t, parent) # 최단 경로 복원
        for a,b in zip(path,path[1:]):
            dist_total += W[a][b]
        
        print(*path)                      # 경로 출력
        print(dist_total)                 # 최단거리 출력10
        visualize_path(W, path)

        

