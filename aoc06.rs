use std::io::{self, BufRead};

fn parse1(str: &str) -> Vec<u64> {
    return str.split(':').skip(1).next().unwrap().split_ascii_whitespace().map(|x| x.parse::<u64>().unwrap()).collect();
}
fn parse2(str: &str) -> Vec<u64> {
    vec![str.split(':').skip(1).next().unwrap().chars().filter(|c| !c.is_whitespace()).collect::<String>().parse::<u64>().unwrap()]
}

fn solve(times: Vec<u64>, dists: Vec<u64>) -> u64 {
    let mut total = 1u64;
    for (i, time) in times.iter().enumerate() {
        let dist = dists[i];
        let d_s = f64::sqrt((time*time - 4*dist) as f64);
        let ftime = f64::from(*time as f64);
        let p1 = (ftime - d_s) / 2.0;
        let p2 = (ftime + d_s) / 2.0;
        let f1 = p1.ceil() as u64;
        let f2 = p2.floor() as u64;
        let mut vars = f2 - f1 + 1;
        if p1.fract() == 0.0 {
            vars-=1;
        }
        if p2.fract() == 0.0 {
            vars-=1;
        }
        total *= vars;
    }
    total
}

fn main() {
    let stdin = io::stdin();
    let mut iterator = stdin.lock().lines();
    let times = iterator.next().unwrap().unwrap();
    let dists = iterator.next().unwrap().unwrap();
    let part1 = solve(parse1(&times), parse1(&dists));
    let part2 = solve(parse2(&times), parse2(&dists));
    println!("part1: {}", part1);
    println!("part2: {}", part2);
}

