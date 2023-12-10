import sys
import re

def parse(str):
    return [int(x) for x in re.split(r'\s+', str.strip())]

score = 0
wins = []
for _, line in enumerate(sys.stdin):
    win, have = line.strip().split(': ')[1].split(' | ')
    win = set(parse(win))
    have = parse(have)
    have_wins = sum(n in win for n in have)
    if have_wins > 0:
        score += 2 ** (have_wins - 1)
    wins.append(have_wins)

print('part1:',score)

cards = [1] * len(wins)
for i, n in enumerate(wins):
    for di in range(i + 1, i + 1 + wins[i]):
        cards[di] += cards[i]
print('part2:', sum(cards))
