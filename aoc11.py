import sys
import re

image = []
for _, line in enumerate(sys.stdin):
    image.append(list(line.strip()))

def get_empty(image):
    r = []
    for idx, line in enumerate(image):
        if all(p=='.' for p in line):
            r.append(idx)
    return r

fat_lines = get_empty(image)
fat_cols = get_empty(list(map(list, zip(*image))))
galaxies = [(y, x) for y, line in enumerate(image) for x, ch in enumerate(line) if ch == '#']

def solve(fat_coeff):
    fat_coeff -= 1
    dist = 0
    for idx, a in enumerate(galaxies):
        for b in galaxies[idx + 1:]:
            dist += abs(a[0]-b[0]) + abs(a[1] - b[1])
            s0 = (min(a[0], b[0]), max(a[0], b[0]))
            s1 = (min(a[1], b[1]), max(a[1], b[1]))
            dist += sum((fat_coeff for x in fat_lines if x > s0[0] and x < s0[1]))
            dist += sum((fat_coeff for x in fat_cols if x > s1[0] and x < s1[1]))
    return dist

print("part1:", solve(2))
print("part2:", solve(1000000))


