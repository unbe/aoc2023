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

def solve(mir, target_diff):
    summ = 0
    for i in range(len(mir) - 1):
        sz = min(i + 1, len(mir) - i - 1)
        sl1 = mir[i+1-sz : i+1]
        sl2 = mir[i+sz : i :-1]
        diff = sum(c1 != c2 for (s1,s2) in zip(sl1, sl2) for(c1, c2) in zip(s1,s2))
        if diff == target_diff:
            summ += (i + 1)
    return summ

def solveall(mirs, target_diff):
    total = 0
    for mir in mirs:
        cols = list(map(''.join, zip(*mir))) # transpose
        total += 100*solve(mir, target_diff) + solve(cols, target_diff)
    return total

print('part1:', solveall(mirs, 0))
print('part2:', solveall(mirs, 1))
