import sys
maze = [line.strip() for line in sys.stdin]
def count(beam):
    beams = [beam]
    e = set()
    while len(beams) > 0:
        b = beams.pop()
        b = (b[0] + b[2], b[1] + b[3], b[2], b[3])
        if b[0] < 0 or b[0] >= len(maze) or b[1] < 0 or b[1] >= len(maze[0]):
            continue
        if b in e:
            continue
        e.add(b)
        obj = maze[b[0]][b[1]]
        if obj == '/':
            beams.append((b[0], b[1], -b[3], -b[2]))
        elif obj == '\\':
            beams.append((b[0], b[1], b[3], b[2]))
        elif obj == '|' and b[2] == 0 or obj == '-' and b[3] == 0:
            beams.append((b[0], b[1], -b[3], -b[2]))
            beams.append((b[0], b[1], b[3], b[2]))
        else:
            beams.append(b)
    return len(set([(x[0], x[1]) for x in e]))

print('part1:', count((0, -1, 0, 1)))

m = 0
for i in range(len(maze)):
    m = max(m, count((i, -1, 0, 1)))
    m = max(m, count((i, len(maze[0]), 0, -1)))
for i in range(len(maze[0])):
    m = max(m, count((-1, i, 1, 0)))
    m = max(m, count((len(maze), i, 1, 0)))
print('part2:', m)
