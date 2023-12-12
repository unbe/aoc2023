import sys
import re
import functools

recs = []
for line in sys.stdin:
    rec, grp = line.strip().split(' ')
    grp = list(map(int, grp.split(',')))
    recs.append((tuple(rec), tuple(grp)))

@functools.cache
def solve(rec, grp):
    cnt = 0
    if len(grp) == 0:
        cnt = +('#' not in rec)
    if len(grp) > 0 and len(rec) > 0:
        g = grp[0]
        for i in range(len(rec)-g+1):
            fits = sum(x != '.' for x in rec[i:i+g]) == g
            if fits and (i+g == len(rec) or rec[i+g] != '#'):
                cnt += solve(rec[i+g+1:], grp[1:])
            if rec[i] == '#':
                break
    return cnt

total = 0
for r in recs:
    s = solve(*r)
    total += s
print("part1:", total)

def unfold(t, s):
    t = ((list(t)) + s) * 5
    if len(s) > 0:
        t = t[:-len(s)]
    return tuple(t)

recs2 = []
for r in recs:
    recs2.append((unfold(r[0], ['?']), unfold(r[1], [])))
    
total = 0
for r in recs2:
    s = solve(*r)
    total += s
print("part2:", total)
