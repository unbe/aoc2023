import sys
import re
import functools
import numpy as np

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

# Part2:
#
# px0 + dx0 * t0 = pxr + dxr * t0 —> t0 = (pxr - px0) / (dx0 - dxr)
# py0 + dy0 * t0 = pyr + dyr * t0 —> t0 = (pyr - py0) / (dy0 - dyr)
# pz0 + dz0 * t0 = pzr + dzr * t0 —> t0 = (pzr - pz0) / (dz0 - dzr)
# -->
# (pxr - px0) / (dx0 - dxr) = (pyr - py0) / (dy0 - dyr)
# (pyr - py0) / (dy0 - dyr) = (pzr - pz0) / (dz0 - dzr)
# -->
# (pxr - px0) * (dy0 - dyr) = (pyr - py0) * (dx0 - dxr)
# (pyr - py0) * (dz0 - dzr) = (pzr - pz0) * (dy0 - dyr)
# -->
# pxr*dy0 + px0*dyr - px0*dy0 - pxr*dyr = pyr*dx0 + py0 * dxr - py0 * dx0 - pyr * dxr
# pyr*dz0 + py0*dzr - py0*dx0 - pyr*dzr = pzr*dy0 + pz0 * dyr - pz0 * dy0 - pzr * dyr
# -
# pxr*dy1 + px1*dyr - px1*dy1 - pxr*dyr = pyr*dx1 + py1 * dxr - py1 * dx1 - pyr * dxr
# pyr*dz1 + py1*dzr - py1*dx1 - pyr*dzr = pzr*dy1 + pz1 * dyr - pz1 * dy1 - pzr * dyr
# -->
# pxr*dy1 + px1*dyr - px1*dy1 - pxr*dyr - (pxr*dy0 + px0*dyr - px0*dy0 - pxr*dyr) = pyr*dx1 + py1 * dxr - py1 * dx1 - pyr * dxr - (pyr*dx0 + py0 * dxr - py0 * dx0 - pyr * dxr)
# pxr*dy1 + dyr*px1 - px1*dy1 - pxr*dy0 - px0*dyr + px0*dy0 = pyr*dx1 + py1 * dxr - py1 * dx1 - pyr*dx0 - py0 * dxr + py0 * dx0
# pxr*(dy1 - dy0) + pyr*(dx0 - dx1) + dxr*(py0 - py1) + dyr*(px1 - px0)  = py0 * dx0 + px1*dy1 - px0*dy0  - py1*dx1 
# pyr*(dz1 - dz0) + pzr*(dy0 - dy1) + dyr*(pz0 - pz1) + dzr*(py1 - py0)  = pz0 * dy0 + py1*dz1 - py0*dz0  - pz1*dy1 
# -->
# pxr*          pyr*          pzr*          dxr*          dyr*          dzr*
# (dy1 - dy0) + (dx0 - dx1) + 0           + (py0 - py1) + (px1 - px0) + 0            = py0 * dx0 + px1*dy1 - px0*dy0  - py1*dx1 
# 0           + (dz1 - dz0) + (dy0 - dy1) + 0           + (pz0 - pz1) + (py1 - py0)  = pz0 * dy0 + py1*dz1 - py0*dz0  - pz1*dy1 
# (dy2 - dy0) + (dx0 - dx2) + 0           + (py0 - py2) + (px2 - px0) + 0            = py0 * dx0 + px2*dy2 - px0*dy0  - py2*dx2 
# 0           + (dz2 - dz0) + (dy0 - dy2) + 0           + (pz0 - pz2) + (py2 - py0)  = pz0 * dy0 + py2*dz2 - py0*dz0  - pz2*dy2 
# (dy3 - dy0) + (dx0 - dx3) + 0           + (py0 - py3) + (px3 - px0) + 0            = py0 * dx0 + px3*dy3 - px0*dy0  - py3*dx3 
# 0           + (dz3 - dz0) + (dy0 - dy3) + 0           + (pz0 - pz3) + (py3 - py0)  = pz0 * dy0 + py3*dz3 - py0*dz0  - pz3*dy3 

px0, py0, pz0 = lines[0][0]
dx0, dy0, dz0 = lines[0][1]

px1, py1, pz1 = lines[1][0]
dx1, dy1, dz1 = lines[1][1]

px2, py2, pz2 = lines[2][0]
dx2, dy2, dz2 = lines[2][1]

a = np.array([
  (dy1 - dy0) , (dx0 - dx1) , 0           , (py0 - py1) , (px1 - px0) , 0,
  0           , (dz1 - dz0) , (dy0 - dy1) , 0           , (pz0 - pz1) , (py1 - py0),
  (dy2 - dy0) , (dx0 - dx2) , 0           , (py0 - py2) , (px2 - px0) , 0,
  0           , (dz2 - dz0) , (dy0 - dy2) , 0           , (pz0 - pz2) , (py2 - py0),
  (dy3 - dy0) , (dx0 - dx3) , 0           , (py0 - py3) , (px3 - px0) , 0,
  0           , (dz3 - dz0) , (dy0 - dy3) , 0           , (pz0 - pz3) , (py3 - py0)
])

b = np.array([
  py0 * dx0 + px1*dy1 - px0*dy0  - py1*dx1,
  pz0 * dy0 + py1*dz1 - py0*dz0  - pz1*dy1,
  py0 * dx0 + px2*dy2 - px0*dy0  - py2*dx2,
  pz0 * dy0 + py2*dz2 - py0*dz0  - pz2*dy2,
  py0 * dx0 + px3*dy3 - px0*dy0  - py3*dx3,
  pz0 * dy0 + py3*dz3 - py0*dz0  - pz3*dy3]
)

r = np.linalg.solve(a, b)
