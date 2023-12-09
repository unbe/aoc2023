use std::io::{self, BufRead};
use std::collections::HashMap;

fn gcd(mut a: i64, mut b: i64) -> i64 {
    while b != 0 {
        let remainder = a % b;
        a = b;
        b = remainder;
    }
    a
}

fn lcm(a: i64, b: i64) -> i64 {
    (a * b) / gcd(a, b)
}

fn mod_inverse(mut a: i64, mut m: i64) -> i64 {
    if m == 1 {
        return 0;
    }
    let m0 = m;
    let mut y = 0;
    let mut x = 1;

    while a > 1 {
        let q = a / m;
        let mut t = m;

        m = a % m;
        a = t;
        t = y;

        y = x - q * y;
        x = t;
    }

    if x < 0 {
        x += m0;
    }
    x
}

fn mod_div(mut a: i64, b: i64, m: i64) -> i64 {
    a = a % m;
    let inv = mod_inverse(b, m);
    let mut r = (inv * a) % m;
    if r < 0 {
        r += m
    }
    r
}

// Merge two cyclic ghosts into equivalent single cyclic ghost.
// fN: first z-point of the ghost N
// pN: period of the ghost B
fn merge_ghosts(f1: i64, p1: i64, f2: i64, p2: i64) -> (i64, i64) {
    let g = gcd(p1, p2);
    let k2 = mod_div((f1 - f2) / g, p2 / g, p1 / g);
    let k1 = (k2 * p2 + f2 - f1) / p1;
    assert!(k1*p1+f1 == k2*p2+f2);
    (k1*p1+f1, lcm(p1, p2))
}

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
    let mut ghosts = map.keys().filter(|k| k.ends_with('A')).map(|p| (p, Vec::<&str>::new(), 0, "", 0)).collect::<Vec<_>>();
    let mut count = 0;
    for dir in route.chars().cycle() {
        count += 1;
        let idx = dirs.find(dir).unwrap();
        for ghost in &mut ghosts {
            let next = &map[ghost.0][idx];
            ghost.0 = next;
            if next.ends_with("Z") {
                if ghost.4 == 0 && next == ghost.3 {
                    ghost.4 = count
                }
                if ghost.2 == 0 {
                    ghost.2 = count;
                    ghost.3 = next;
                } 
            }
        }
        if ghosts.iter().filter(|g| g.0.ends_with("Z")).count() == ghosts.len() {
            // Happens ever?
            break;
        }
        if ghosts.iter().filter(|g| g.2 > 0 && g.4 > 0).count() == ghosts.len() {
            let cycles = ghosts.iter().map(|g| (g.2, g.4 - g.2)).collect::<Vec<_>>();
            let merged = cycles.iter().fold((1, 1), |acc, nxt| merge_ghosts(acc.0, acc.1, nxt.0, nxt.1));
            // This simpler way also works for the input, as there are no misaligned cycles.
            // The real code should also work for misaligned cycles.
            // count = cycles.iter().fold(1, |acc, nxt| lcm(acc, nxt.0));
            count = merged.1;
            break;
        }
    }
    println!("{}", count);
}
