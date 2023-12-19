import sys
import heapq

maze = [[int(x) for x in line.strip()] for line in sys.stdin]

def moves(u, d_min, d_max):
    x, y, cnt, d = u 
    for dmove in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if dmove == (-d[0], -d[1]):
            continue
        if dmove == d:
            if cnt == d_max:
                continue
            else:
                ncnt = cnt + 1
        else:
            if cnt < d_min and d != (0, 0):
                continue
            ncnt = 1
        nx = x + dmove[0]
        ny = y + dmove[1]
        if nx < 0 or ny < 0 or nx >= len(maze) or ny >= len(maze[0]):
            continue
        yield ((nx, ny, ncnt, dmove), maze[nx][ny])

def solve(d_min, d_max):
    s = (0, 0, -1, (0, 0))
    dist = {}
    dist[s] = 0
    pq = [(0, s)]
    prev = {}

    while len(pq) > 0:
        _, u = heapq.heappop(pq)
        for v, l in moves(u, d_min, d_max):
            if v not in dist or dist[u] + l < dist[v]:
                dist[v] = dist[u] + l
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    stop = (len(maze)-1, len(maze[0])-1)
    end, best_v = sorted([(k, v) for k, v in dist.items() if (k[0], k[1]) == stop and k[2] >= d_min and k[2] <= d_max], key=lambda u: u[1])[0]
    return (best_v, end, prev)   # extra values for debugging

print('part1:', solve(0, 3)[0])
print('part2:', solve(4, 10)[0])


"""
path = {}
path[(r[0], r[1])] = '*'
sm = maze[r[0]][r[1]]
while r in prev:
    r = prev[r]
    path[(r[0], r[1])] = '*'
    sm += maze[r[0]][r[1]]
    # print(r, dist[r], maze[r[0]][r[1]], sm)

for x, r in enumerate(maze):
    for y, n in enumerate(r):
        if (x, y) in path:
            print('\033[1m', end='')
        print(maze[x][y], end='')
        if (x, y) in path:
            print('\033[0m', end='')
    print('')
"""
