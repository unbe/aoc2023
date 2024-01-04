import sys
import re
import functools

lines = []
for line in sys.stdin:
    pos, d = ([int(i) for i in x.split(', ')] for x in line.split(" @ "))
    lines.append((pos, d))

def intrs(a, b):
  pa, da = a
  pb, db = b
  x1, y1, z1 = pa
  x2, y2, z2 = map(sum, zip(pa, da))
  x3, y3, z3 = pb
  x4, y4, z4 = map(sum, zip(pb, db))

  d = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
  if d == 0:
    return None
  t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / d
  u = ((x1 - x3)*(y1 - y2) - (y1 - y3)*(x1 - x2)) / d

  px, py = (x1 + t*(x2 - x1), y1 + t*(y2 - y1))

  return ((px, py), t, u)

pmin = 200000000000000
pmax = 400000000000000

cnt = 0
for i in range(len(lines)):
  for j in range(i + 1, len(lines)):
    ix = intrs(lines[i], lines[j])
    if ix is None or ix[1] < 0 or ix[2] < 0:
      continue
    p = ix[0]
    if p[0] < pmin or p[0] > pmax or p[1] < pmin or p[1] > pmax:
      continue
    cnt += 1

print("part1:", cnt)
