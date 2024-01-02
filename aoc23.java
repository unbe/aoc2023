package aoc2023;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

public class aoc23 {
	record XY(int x, int y) {
	}

	record XYd(int x, int y, char d) {
	}

	record Edge(XY from, XY to, int w) {
	}

	record QueueEntry(XY pos, Set<XY> tail, int len) {
	}

	private static void addEdge(Edge e, Map<XY, Set<Edge>> edgesFrom, Map<XY, Set<Edge>> edgesTo) {
		edgesFrom.computeIfAbsent(e.from(), t -> (new HashSet<Edge>())).add(e);
		edgesTo.computeIfAbsent(e.to(), t -> (new HashSet<Edge>())).add(e);
	}

	private static void rmEdge(Edge e, Map<XY, Set<Edge>> edgesFrom, Map<XY, Set<Edge>> edgesTo) {
		edgesFrom.get(e.from()).remove(e);
		edgesTo.get(e.to()).remove(e);
	}

	private static void foldPipes(HashMap<XY, Set<Edge>> edgesFrom, HashMap<XY, Set<Edge>> edgesTo) {
		Set<XY> nodes = new HashSet<XY>(edgesFrom.keySet());
		for (var node : nodes) {
			Set<Edge> outgoing = edgesFrom.get(node);
			if (outgoing == null || outgoing.size() != 2) {
				continue;
			}
			Set<Edge> incoming = edgesTo.get(node);
			if (incoming == null || incoming.size() != 2) {
				continue;
			}
			Set<XY> points = new HashSet<>();
			points.addAll(outgoing.stream().map(t -> t.to()).toList());
			points.addAll(incoming.stream().map(t -> t.from()).toList());
			assert (points.size() == 2);
			int w = outgoing.stream().mapToInt(t -> t.w()).sum();

			List.copyOf(outgoing).forEach(e -> {
				rmEdge(e, edgesFrom, edgesTo);
			});
			List.copyOf(incoming).forEach(e -> {
				rmEdge(e, edgesFrom, edgesTo);
			});
			assert (edgesFrom.get(node).size() == 0);
			assert (edgesTo.get(node).size() == 0);
			edgesFrom.remove(node);
			edgesTo.remove(node);

			XY[] pts = points.toArray(new XY[2]);
			Edge e = new Edge(pts[0], pts[1], w);
			addEdge(e, edgesFrom, edgesTo);
			e = new Edge(pts[1], pts[0], w);
			addEdge(e, edgesFrom, edgesTo);
		}
	}

	private static int solve(List<String> maze, boolean canClimb) {
		XY mazeSize = new XY(maze.get(0).length(), maze.size());
		XY start = new XY(maze.get(0).indexOf('.'), 0);
		XY end = new XY(maze.get(mazeSize.y - 1).indexOf('.'), mazeSize.y-1);
		HashMap<XY, Set<Edge>> edgesFrom = new HashMap<>();
		HashMap<XY, Set<Edge>> edgesTo = new HashMap<>();
		XYd[] moves = new XYd[] { new XYd(-1, 0, '<'), new XYd(1, 0, '>'), new XYd(0, -1, '^'), new XYd(0, 1, 'v') };
		for (int y = 0; y < mazeSize.y; y++) {
			String row = maze.get(y);
			for (int x = 0; x < mazeSize.x; x++) {
				char at = row.charAt(x);
				if (at == '#') {
					continue;
				}
				XY pos = new XY(x, y);
				for (XYd move : moves) {
					XY npos = new XY(pos.x + move.x, pos.y + move.y);
					if (npos.x < 0 || npos.x >= mazeSize.x || npos.y < 0 || npos.y >= mazeSize.y) {
						continue;
					}
					char nat = maze.get(npos.y).charAt(npos.x);
					if (!canClimb && at != '.' && at != move.d) {
						continue;
					}
					if (nat == '#') {
						continue;
					}
					Edge e = new Edge(pos, npos, 1);
					addEdge(e, edgesFrom, edgesTo);
				}

			}
		}

		foldPipes(edgesFrom, edgesTo);

		Set<XY> path = new HashSet<XY>();
		int pathlen = 0;
		XY pos = start;
		int max = 0;
		List<QueueEntry> queue = new LinkedList<>();
		while (true) {
			if (pos.equals(end)) {
				max = Math.max(max, pathlen);
			}
			path.add(pos);
			Set<Edge> edges = edgesFrom.get(pos);
			Set<XY> ipath = path;
			List<Edge> goodEdges = edges.stream().filter(e -> !ipath.contains(e.to())).toList();
			if (goodEdges.size() > 0) {
				for (int i = 1; i < goodEdges.size(); i++) {
					Edge edge = goodEdges.get(i);
					queue.add(new QueueEntry(edge.to(), new HashSet<XY>(path), pathlen + edge.w()));
				}
				Edge edge = goodEdges.get(0);
				pos = edge.to();
				pathlen += edge.w();
			} else {
				if (queue.size() == 0) {
					return max;
				}
				QueueEntry qmove = queue.remove(0);
				pos = qmove.pos();
				path = qmove.tail();
				pathlen = qmove.len();
			}
		}
	}

	public static void main(String[] args) throws IOException {
		List<String> maze = Files.lines(Paths.get(args[0])).collect(Collectors.toList());
		System.out.println("part1: " + solve(maze, false));
		System.out.println("part2: " + solve(maze, true));
	}
}
