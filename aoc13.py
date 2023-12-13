import sys
import re
import functools

mir = []
mirs = [mir]
for line in sys.stdin:
    line = line.strip()
    if line == "":
        mir = []
        mirs.append(mir)
        continue
    mir.append(line)

def solve(mir):
    summ = 0
    for i in range(len(mir) - 1):
        sz = min(i + 1, len(mir) - i - 1)
        if all(mir[i - j] == mir[i + j + 1] for j in range(sz)):
            summ += (i + 1)
    return summ

total = 0
for mir in mirs:
    cols = list(map(''.join, zip(*mir)))
    total += 100*solve(mir) + solve(cols)
print('part1:', total)
