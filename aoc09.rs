use std::io::{self, BufRead};
use std::iter::zip;

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    let mut tail_sum = 0;
    let mut head_sum = 0;
    for m_line in lines {
        let line = m_line.unwrap();
        let mut v = line.split(" ").map(|a| a.parse::<i32>().unwrap()).collect::<Vec<_>>();
        let mut tails = vec![];
        let mut heads = vec![];
        while v.iter().filter(|x| **x != 0).count() > 0 {
            heads.push(v[0]);
            tails.push(v[v.len()-1]);
            v = zip(&v, &v[1..]).map(|z| z.1 - z.0).collect::<Vec<_>>();
        }
        tail_sum += tails.iter().sum::<i32>();
        head_sum += heads.iter().zip([1,-1].iter().cycle()).map(|(&v, &s)| v*s).sum::<i32>();
    }
    println!("part1: {}", tail_sum);
    println!("part2: {}", head_sum);
}

