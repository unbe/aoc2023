package aoc2023;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

public class aoc22 {
	record XY(int x, int y) {
	}

	static class Brick {
		int x0, x1;
		int y0, y1;
		int z0, z1;
		Set<Brick> pillars = new HashSet<>();
		Set<Brick> piles = new HashSet<>();

		public Brick(String def) {
			int[] coords = Arrays.stream(def.split("~|,")).mapToInt(Integer::parseInt).toArray();
			x0 = Math.min(coords[0], coords[3]);
			x1 = Math.max(coords[0], coords[3]);
			y0 = Math.min(coords[1], coords[4]);
			y1 = Math.max(coords[1], coords[4]);
			z0 = Math.min(coords[2], coords[5]);
			z1 = Math.max(coords[2], coords[5]);
		}
	}

	public static void main(String[] args) throws IOException {
		Map<XY, Brick> tops = new HashMap<>();
		List<Brick> bricks = Files.lines(Paths.get(args[0])).map(Brick::new).collect(Collectors.toList());
		bricks.sort((b1, b2) -> (b1.z0 - b2.z0));
		for (Brick b : bricks) {
			int land = 0;
			for (int x = b.x0; x <= b.x1; x++) {
				for (int y = b.y0; y <= b.y1; y++) {
					XY key = new XY(x, y);
					Brick below = tops.get(key);
					if (below != null && below.z1 >= land) {
						if (below.z1 > land) {
							land = below.z1;
							b.pillars.clear();
						}
						b.pillars.add(below);
					}
				}
			}
			land += 1;
			assert (land < b.z0);
			b.z1 -= (b.z0 - land);
			b.z0 = land;
			for (Brick bp : b.pillars) {
				bp.piles.add(b);
			}
			for (int x = b.x0; x <= b.x1; x++) {
				for (int y = b.y0; y <= b.y1; y++) {
					tops.put(new XY(x, y), b);
				}
			}
		}
		int removable = 0;
		for (Brick b : bricks) {
			boolean critical = b.piles.stream().anyMatch(bs -> (bs.pillars.size() == 1));
			if (!critical)
				removable++;
		}
		System.out.println("part1: " + removable);

		int chainTotal = 0;
		for (Brick b : bricks) {
			Set<Brick> gone = new HashSet<>();
			gone.add(b);
			Set<Brick> couldfall = new HashSet<>(b.piles);
			while (true) {
				boolean step = false;
				for (Brick cf : new HashSet<>(couldfall)) {
					if (gone.containsAll(cf.pillars)) {
						gone.add(cf);
						couldfall.remove(cf);
						couldfall.addAll(cf.piles);
						step = true;
					}
				}
				if (!step) {
					break;
				}
			}
			chainTotal += gone.size() - 1;
		}
		System.out.println("part2: " + chainTotal);
	}
}
