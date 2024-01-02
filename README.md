## Advent of Code 2023

Notable things this year:

* I tried Rust a bit more and really like it! Feels as powerful as Python, maybe a bit more verbose, but much less struggle than with Go.
* I went quite deep with part 2 of day 8, which wasn't actually necessary since the input was aligned in a way permitting a simpler solution. I noticed it mid-way, but finished the full solution anyway.
* My solution for day 10 is a single and quite simple linear pass for each part, while others seem to have deployed various search algos. Curious. At the same time, part2 was solvable even easier with the Shoelace formula + Pick's theorem, which I wasn't aware of.
* I did a bunch of premature optimization for day 12 and it ended up buggy. Rewrote with a simple solution, which ended up fast enough.
* Mountains > coding. I'm a few days behind ;)
* I made a somewhat complex solution for day 18, again not knowing the Shoelace formula. TIL.
* For day 20, I created a solution tailored for my input. I was slightly annoyed by not finding a generic solution, but I'm half-sure there isn't one.
* Day 20 story tripped me on day 21, I started looking for a generic solution and all I found was computationally too expensive. Looks like there isn't one, again. This is the first day I used some help to come up with the solution, only to find that there is no generic one -- spent too much time failing to find it.
* Day 23 is NP-hard again for the generic case. The input can be folded into a much smaller graph though. I think further optimizations might be possible, but not sure I'll get to it.
