package aoc2023;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
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

	public static int mod(int a, int m) {
		return (a % m + m) % m;
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
		int p1_target = 64;
		int p2_target = 26501365;
		List<Integer> poly = new ArrayList<Integer>();
		for (int i = 0;; i++) {
			for (Point p : front) {
				for (Point d : dirs) {
					Point n = new Point(p.r + d.r, p.c + d.c);
					String row = maze.get(mod(n.r, maze.size()));
					if (row.charAt(mod(n.c, row.length())) != '#') {
						step.add(n);
					}
				}
			}
			front = step;
			step = new HashSet<>();
			int steps = i + 1;
			if (steps == p1_target) {
				System.out.println("part1: " + front.size());
			}
			if (steps % maze.size() == p2_target % maze.size()) {
				poly.add(front.size());
				if (poly.size() == 3) {
					break;
				}
			}
		}
		int p1 = poly.get(0);
		int p2 = poly.get(1);
		int p3 = poly.get(2);
		long a = (p3 - (2 * p2) + p1) / 2;
		long b = p2 - p1 - a;
		long c = p1;
		long n = (p2_target - maze.size() / 2) / maze.size();
		System.out.println("part2: " + ((a * (n * n)) + (b * n) + c));
	}
}
