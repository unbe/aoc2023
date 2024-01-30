import sys
import operator

import networkx as nx
from networkx.algorithms.connectivity import minimum_edge_cut

E = []
for line in sys.stdin:
  a, b = line.strip().split(': ')
  b = b.split(' ')
  E.extend(zip([a]*len(b), b))

G=nx.Graph()
G.add_edges_from(E)
mec = nx.minimum_edge_cut(G)
G.remove_edges_from(mec)
cc = list(nx.connected_components(G))
print('part1:', len(cc[0])*len(cc[1]))

# There is no part2 in day25
