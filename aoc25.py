import sys
import operator

import networkx as nx
from networkx.algorithms.connectivity import minimum_edge_cut

G=nx.Graph()
for line in sys.stdin:
  a, b = line.strip().split(': ')
  b = b.split(' ')
  G.add_edges_from(zip([a]*len(b), b))

mec = nx.minimum_edge_cut(G)
G.remove_edges_from(mec)
cc = list(nx.connected_components(G))
print('part1:', len(cc[0])*len(cc[1]))

# There is no part2 in day25
