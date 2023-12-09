use std::io::{self, BufRead};
use std::collections::HashMap;

fn main() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();
    let route = lines.next().unwrap().unwrap();
    lines.next();
    let mut map: HashMap<String, Vec<String>> = HashMap::new();

    for m_line in lines {
        let line = m_line.unwrap();
        let Some((src, dest)) = line.split_once(" = ") else { panic!(); };
        map.insert(src.to_string(), dest[1..dest.len()-1].split(", ").map(String::from).collect::<Vec<_>>());
    }
    let dirs = "LR";
    let mut next = "AAA";
    let mut count = 0;
    for dir in route.chars().cycle() {
        let idx = dirs.find(dir).unwrap();
        next = &map[next][idx];
        count += 1;
        if next == "ZZZ" {
            break
        }
    }
    println!("part1: {}", count);
}
