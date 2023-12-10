use std::io::{self, BufRead};
use std::collections::HashMap;

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    let labels = "AKQJT98765432";
    let mut hands : Vec<_> = vec![];
    for m_line in lines {
        let line = m_line.unwrap();
        let mut parts = line.split(' ');
        let hand = parts.next().unwrap();
        let bid = parts.next().unwrap().parse::<u32>().unwrap();
        let mut hand_counts: HashMap<char,i32> = HashMap::new();
        for ch in hand.chars().collect::<Vec<char>>() {
            *hand_counts.entry(ch).or_insert(0) += 1;
        }
        let mut hand_sorted: Vec<_> = hand_counts.iter().collect();
        hand_sorted.sort_by(|a, b| b.1.cmp(a.1));
        let rank;
        if *hand_sorted[0].1 == 5 {
            rank = 7
        } else if *hand_sorted[0].1 == 4 {
            rank = 6
        } else if *hand_sorted[0].1 == 3 && *hand_sorted[1].1 == 2 {
            rank = 5
        } else if *hand_sorted[0].1 == 3 {
            rank = 4
        } else if *hand_sorted[0].1 == 2 && *hand_sorted[1].1 == 2 {
            rank = 3
        } else if *hand_sorted[0].1 == 2 {
            rank = 2
        } else {
            rank = 1
        }
        let label_ranks: Vec<_> = hand.chars().map(|c| labels.len() - labels.find(c).unwrap()).collect();
        hands.push((rank, label_ranks.clone(), hand.to_string(), bid));
    }
    hands.sort_by(|a, b| a.cmp(b));
    let mut win = 0;
    for (i, hand) in hands.iter().enumerate() {
        win += hand.3 * (i as u32 + 1)
    }
    println!("part1: {}", win);
}

