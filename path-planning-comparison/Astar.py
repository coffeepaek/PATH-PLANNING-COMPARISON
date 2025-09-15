INF = 0xFFFF
n, m = map(int, input().split())   # n: 정점 개수 / m: 간선 개수

# 가중치 인접 행렬
W = [[0 if i == j else INF for i in range(n)] for j in range(n)]
for _ in range(m):
    u, v, w = map(int, input().split())
    W[u][v] = w

# 노드 좌표n줄 입력 "x y"
coords = [tuple(map(float,input().split())) for _ in range(n)]

s,t = map(int,input().split())
        
def astar_run(coords, start, goal, n, W):
    parent = [start for _ in range(n)]              # 직전 노드 저장
    g = [0 if i == start else INF for i in range(n)]  # 실제 비용
    h = heuristic(goal, coords)
    f = [h[start] if i == start else INF for i in range(n)]  # f = g + h

    for _ in range(n - 1):
        u = pick_lowest_f(f)                        # f값이 최소인 노드 선택
        if u == goal:
            return parent, f

        for v in range(n):
            if g[v] > g[u] + W[u][v]:
                g[v] = g[u] + W[u][v]
                f[v] = g[v] + h[v]
                parent[v] = u
        f[u] = -1  # 방문 처리
    return parent,f


def restore_path(start, target, parent):
    # 재귀적으로 경로 복원
    if parent[target] == start:
        return [start, target]
    else:
        return restore_path(start, parent[target], parent) + [target]


def pick_lowest_f(f):
    # f값이 가장 작은 노드 반환
    minimum, u = INF, -1
    for v in range(len(f)):
        if 0 <= f[v] < minimum:
            minimum = f[v]
            u = v
    return u

import math
def heuristic(target, coords):
    gx, gy = coords[target]
    h = [math.hypot(x-gx, y-gy) for (x,y) in coords]
    return h

 # --- 추가: 경로 시각화 (matplotlib) ---
def visualize_path(W, path, INF=0xFFFF):
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

    parent,f = astar_run(coords, s, t, n, W)
    path = restore_path(s, t, parent)
    dist_total = 0

    if f[t] == INF:
        print("Unreachable")              # 도달 불가
    
    for a,b in zip(path,path[1:]):
            dist_total += W[a][b]

    print(*path)     # 최단 경로
    print(dist_total)
    visualize_path(W, path)