import sys
import re

image = []
for _, line in enumerate(sys.stdin):
    image.append(list(line.strip()))

def linedup(image):
    idx = 0
    while idx < len(image):
        line = image[idx]
        if all(p=='.' for p in line):
            image.insert(idx, line.copy());
            idx += 1
        idx += 1
    return image

def transpose(image):
    return list(map(list, zip(*image)))

image = transpose(linedup(transpose(linedup(image))))
galaxies = [(y, x) for y, line in enumerate(image) for x, ch in enumerate(line) if ch == '#']
dist = 0
for idx, a in enumerate(galaxies):
    for b in galaxies[idx:]:
        if a == b:
            continue
        dist += abs(a[0]-b[0]) + abs(a[1] - b[1])

print(dist)


