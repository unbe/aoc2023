## Advent of Code 2023

These are my solutions for https://adventofcode.com/2023 and some notes. They are mostly written in [*sports programming style*](https://en.wikipedia.org/wiki/Competitive_programming#Benefits_and_criticism), which definitely makes it harder to read than my production code style.

Index:

 * Shell: [Day1](aoc01.sh)
 * Golang: [Day2](aoc02.go) [Day3](aoc03.go)
 * Python: [Day4](aoc04.py) [Day5](aoc05.py) [Day11](aoc11.py) [Day12](aoc12.py) [Day13](aoc13.py) [Day16](aoc16.py) [Day17](aoc17.py)
 * Rust: [Day6](aoc06.rs) [Day7](aoc07.rs) [part2](aoc07b.rs) [Day8](aoc08.rs) [part2](aoc08b.rs) [Day9](aoc09.rs) [Day10](aoc10.rs)
 * Typescript: [Day14](aoc14.ts) [Day15](aoc15.ts) (for JavaScript look here)
 * C++: [Day18](aoc18.cc) [Day19](aoc19.cc) [Day20](aoc20.cc)
 * Java: [Day21](aoc21.java) [Day22](aoc22.java) [Day23](aoc23.java)

Notable things this year:

* I tried Rust a bit more and really like it! Feels as powerful as Python, maybe a bit more verbose, but much less struggle than with Go.
* I went quite deep with part 2 of day 8, which wasn't actually necessary since the input was aligned in a way permitting a simpler solution. I noticed it mid-way, but finished the full solution anyway.
* My solution for day 10 is a single and quite simple linear pass for each part, while others seem to have deployed various search algos. Curious. At the same time, part2 was solvable even easier with the Shoelace formula + Pick's theorem, which I wasn't aware of.
* I did a bunch of premature optimization for day 12 and it ended up buggy. Rewrote with a simple solution, which ended up fast enough.
* Mountains > coding. I'm a few days behind ;)
* I tried TypeScript, which looks similar to ClosureCompiler types I'm fimilar from my time at Google. The type inferences looks weaker than in Rust though and was occasionally getting in the way.
* I made a somewhat complex solution for day 18, again not knowing the Shoelace formula. TIL.
* For day 20, I created a solution tailored for my input. I was slightly annoyed by not finding a generic solution, but I'm half-sure there isn't one.
* Day 20 story tripped me on day 21, I started looking for a generic solution and all I found was computationally too expensive. Looks like there isn't one, again. This is the first day I used some help to come up with the solution, only to find that there is no generic one -- spent too much time failing to find it.
* Day 23 is NP-hard again for the generic case. The input can be folded into a much smaller graph though. I think further optimizations might be possible, but not sure I'll get to it.
