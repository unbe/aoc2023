package aoc2023;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class aoc21 {
	static class Point {
		public int r;
		public int c;

		public Point(int r, int c) {
			this.r = r;
			this.c = c;
		}

		@Override
		public String toString() {
			return "(" + r + ", " + c + ")";
		}

		@Override
		public int hashCode() {
			return Objects.hash(c, r);
		}

		@Override
		public boolean equals(Object obj) {
			if (this == obj)
				return true;
			if (obj == null)
				return false;
			if (getClass() != obj.getClass())
				return false;
			Point other = (Point) obj;
			return c == other.c && r == other.r;
		}
	}

	public static void main(String[] args) {
		Stream<String> lines = new BufferedReader(new InputStreamReader(System.in)).lines();
		List<String> maze = lines.collect(Collectors.toList());
		int sr, sc = 0;
		for (sr = 0; sr < maze.size(); sr++) {
			sc = maze.get(sr).indexOf('S');
			if (sc >= 0) {
				break;
			}
		}
		Point[] dirs = new Point[] { new Point(-1, 0), new Point(1, 0), new Point(0, -1), new Point(0, 1) };
		Set<Point> front = new HashSet<>();
		front.add(new Point(sr, sc));
		Set<Point> step = new HashSet<>();
		for (int i = 0; i < 64; i++) {
			for (Point p : front) {
				for (Point d : dirs) {
					Point n = new Point(p.r + d.r, p.c + d.c);
					if (n.r >= 0 && n.r < maze.size()) {
						String row = maze.get(n.r);
						if (n.c >= 0 && n.c < row.length()) {
							if (row.charAt(n.c) != '#') {
								step.add(n);
							}
						}
					}
				}
			}
			front = step;
			step = new HashSet<>();
		}
		System.out.println("part1: " + front.size());
	}
}
