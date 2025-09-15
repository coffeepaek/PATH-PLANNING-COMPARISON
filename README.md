# PATH-PLANNING-COMPARISON
Dijkstra vs A* (Python) — path planning on weighted graphs with Euclidean heuristic
# Dijkstra vs A* (Python, adjacency matrix)

이 프로젝트는 **자율주행(모바일 로봇)에서의 경로 계획(Path Planning)** 방법으로 널리 쓰이는  
**Dijkstra**와 **Astar**를 같은 입력 형식으로 구현·비교합니다.

- **Dijkstra**: 휴리스틱 없이 실제 비용 `g`만으로 최단경로를 보장합니다. 출발 지점으로부터 도착 지점까지 모든 노드를 방문하며 가중치를 최신화하여 최단 경로를 탐색합니다.

- **A\***: 좌표 기반 **유클리드 휴리스틱** `h`를 이용해 `f = g + h`를 최소화하는 노드를 우선 탐색합니다. 모든 노드를 방문하는 방식이 아닌 `f = g + h`를 최소화하는 노드만을 방문하여 최단 경로를 탐색합니다.
  - 좌표(`coords`)는 **평가용(heuristic)** 으로만 사용되며, 간선 가중치 `W`(도로 비용/속도/제약)은 **그대로** 실제 비용으로 유지됩니다.  
  - `h`가 **admissible/consistent**(실제 비용을 넘지 않고 삼각부등식 만족)할 때 A\*는 최적해를 보장하며, 일반적으로 Dijkstra보다 **확장 노드 수가 적어** 빠릅니다.


  ## 폴더 구조
```
PATH-PLANNING-COMPARISON/
├─ assets/
│  ├─ Astar_result.jpg
│  └─ Dijkstra_result.jpg
├─ examples/
│  ├─ Astar_ex
│  ├─ Astar_unreachable_ex.txt
│  └─ dijkstra_ex.txt
├─ Astar.py
├─ Dijkstra.py
├─ License
├─ Readme.md
└─ requirements.txt
```

## 설치
```bash
pip install -r requirements.txt
```

## 실행
**Dijkstra**
    
-  n m
- 간선 u v w X m줄
- s t


*예시 파일 실행 코드*
```bash
python Dijkstra.py < examples/dijkstra_01.txt
```
*직접 입력 실행*
```bash
python Dijkstra.py

5 7
0 1 10
0 3 5
1 2 1
3 1 3
3 2 9
3 4 2
4 2 6
0 2
```

**A\* 실행 (좌표 기반 휴리스틱)**
-  n m
- 간선 u v w X m줄
- 좌표 x y X n줄
- s t

*예시 파일 실행 코드*
```bash
python AStar.py < examples/astar_01.txt
```
*직접 입력 실행*
```bash
python AStar.py

5 7
0 1 10
0 3 5
1 2 1
3 1 3
3 2 9
3 4 2
4 2 6
0 0
2 0
3 0
0 1
1 1
0 2
```

### Dijkstra
![Dijkstra shortest path](assets/Dijkstra_result.jpg)

### A*
![A* shortest path](assets/Astar_result.jpg)


## 주의사항 (Warnings)
- **인덱스/방향성**: 노드는 **0-based**입니다. 그래프는 **방향 그래프**로 처리되므로 무방향이라면 `u v w`와 `v u w`를 **둘 다** 입력하세요.
- **음수 가중치 미지원**: 두 알고리즘 모두 **음수 간선**을 가정하지 않습니다.
- **INF 상수**: `INF = 0xFFFF (65535)`는 “간선 없음” 표기용입니다.  
  - 총 경로비용이 `INF`를 넘지 않도록 가중치를 선택하세요.  
  - 큰 가중치가 필요하면 `INF = 10**15`처럼 **더 큰 값**으로 바꾸는 것을 권장합니다.
- **좌표와 스케일**: A\*의 좌표 `coords`는 **휴리스틱 계산용**입니다. `coords[i]`는 **노드 i와 순서가 정확히 일치**해야 합니다.  
  - 가중치 단위(시간/비용)와 좌표 거리 단위가 크게 다르면 `h`가 **과대평가**될 수 있습니다. 필요 시 `h = α·distance (0<α≤1)`로 스케일을 낮추세요.
- **최적성 조건**: A\*가 **최적해 보장**을 유지하려면 휴리스틱이 **admissible/consistent**여야 합니다. (유클리드 거리는 보통 안전)
- **도달 불가 처리**: 경로가 없으면 `"Unreachable"`을 출력합니다. 이때는 거리 합산/시각화를 건너뛰세요.
- **성능**: 현 구현은 우선순위 큐 대신 **선형 스캔**을 사용하므로 복잡도는 대략 `O(V^2 + E)`입니다. 큰 그래프에선 `heapq`로 개선하세요.
- **시각화**: `matplotlib`가 필요합니다. 표시가 어려운 환경(서버/WSL)에서는 백엔드 설정이나 파일 저장(예: `plt.savefig`)을 사용하세요.




## 자율주행 관점 비교 (요약)
- **문제 맥락**  
  - 전역 경로 계획(Global Planning)에 초점을 둔 **그래프 기반** 비교입니다.  
  - 실제 도로망/차선/교차로/통행료 등 **현실 비용**은 인접행렬 `W`에,  
    “목표까지 얼마나 가까운가”에 대한 **기하학적 단서**는 A\*의 **휴리스틱**에 담습니다.

- **Dijkstra**  
  - **장점**: 휴리스틱 없이도 **최단경로 보장**, 구현 단순/기준선(baseline)으로 좋음.  
  - **단점**: 목표 방향성이 없어 **탐색 범위가 넓어질 수 있음**(대규모 지도에서 느림).  
  - **권장 사용처**: 노드 수가 작거나, 휴리스틱을 정의하기 어려운 그래프(예: 특수 비용 규칙).

- **A\***  
  - **장점**: `f = g + h`로 **목표 지향 탐색** → 보통 더 빠름(확장 노드 수 감소).  
  - **조건**: `h`가 **admissible/consistent**일 때 **최적성 보장**.  
  - **권장 사용처**: 좌표가 있거나, 물리 공간(도로/지도)에서 목표까지의 “직선/격자” 단서가 있는 경우.

- **확장/실전 팁**  
  - **휴리스틱 강화**: 격자면 **Octile/맨해튼**(이동 제약에 따라 선택), 일반 그래프면 **랜드마크(ALT)**로 보강.  
  - **알고리즘 변형**: **Weighted A\***(속도↑, 최적성 근사), **D\* / D\* Lite**(지도 갱신/재계획), **Hybrid A\***(차량 동역학/조향 각도 반영).  
  - **후처리**: 스플라인/폴리라인 **경로 스무딩** 후 **Pure Pursuit/MPC** 등 추종(controller) 적용.  
  - **안전 여유**: 장애물 팽창(inflation)·비용 레이어(차선 유지, 속도 제한, 커브 페널티 등)로 **안전/쾌적성** 반영.

## License
MIT © 2025 coffeepaek






