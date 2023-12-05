import sys

seeds = [int(x) for x in sys.stdin.readline().strip().split(': ')[1].split(' ')]

maps = []
for _, line in enumerate(sys.stdin):
    line = line.strip()
    if line == "":
        continue
    if line.endswith('map:'):
        thismap = []
        maps.append(thismap)
        continue
    dst, src, cnt = [int(x) for x in line.split(' ')]
    thismap.append((dst, src, cnt))

minloc = 100**20
for s in seeds:
    for m in maps:
        for rule in m:
            if s >= rule[1] and s < rule[1] + rule[2]:
                s = rule[0] + s - rule[1]
                break
    minloc = min(minloc, s)

print('part1: ', minloc)

to_map=zip(seeds[::2], seeds[1::2])
mapped = []
for m in maps:
    for map_rule in m:
        md, ms, mc = map_rule
        me = ms + mc - 1
        next_rule = []
        for rng in to_map:
            rs, rc = rng
            re = rs + rc - 1
            if rs < ms:
                if re < ms:
                    next_rule.append((rs, rc))
                    continue
                next_rule.append((rs, ms - rs))
                rs = ms
            if re > me:
                if rs > me:
                    next_rule.append((rs, rc))
                    continue
                next_rule.append((me + 1, re - me))
                re = me
            mapped.append((md + rs - ms, re - rs + 1))
        to_map = next_rule
    to_map += mapped
    mapped = []

print('part2: ', min([x[0] for x in to_map]))
