use std::io::{self, BufRead};
use std::collections::HashMap;
use std::collections::HashSet;

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    let mut maze = vec!();
    let mut w = 0;
    for line in lines {
        maze.extend(line.unwrap().chars());
        if w == 0 {
            w = maze.len() as i32;
        }
    }
    let s_pos = maze.iter().position(|&r| r == 'S').unwrap() as i32;
    let dirs = HashMap::from([
        ('N', -w),
        ('S', w),
        ('W', -1),
        ('E', 1)
    ]);
    // pipe char --> index shifts for entry/exit
    let pipe_dirs = [
        ('|', ('N', 'S')),  // | is a vertical pipe connecting north and south.
        ('-', ('E', 'W')),  // - is a horizontal pipe connecting east and west.
        ('L', ('N', 'E')),  // L is a 90-degree bend connecting north and east.
        ('J', ('N', 'W')),  // J is a 90-degree bend connecting north and west.
        ('7', ('S', 'W')),  // 7 is a 90-degree bend connecting south and west.
        ('F', ('S', 'E'))   // F is a 90-degree bend connecting south and east.
    ].iter().map(|d| (d.0, (dirs[&d.1.0], dirs[&d.1.1]))).collect::<HashMap<_,_>>();
    
    let mut start = vec!();
    // Find the first two pipes
    for (_, dir) in dirs.iter() {
        let pos = s_pos + dir;
        if pos / w != s_pos / w && pos % w != s_pos % w || pos >= maze.len() as i32 || pos < 0 {
            continue;
        }
        let pipe = maze[pos as usize];
        if pipe == '.' {
            continue;
        }
        let pd = pipe_dirs[&pipe];
        if pos + pd.0 == s_pos || pos + pd.1 == s_pos {
            start.push(pos);
        }
    }
    assert!(start.len() == 2);

    let mut pos = s_pos;
    let mut next : i32 = start[0];
    let mut count = 0;
    let mut big_loop = HashSet::new();
    big_loop.insert(start[1]);
    big_loop.insert(s_pos);
    while next != start[1] {
        big_loop.insert(next);
        count += 1;
        let pipe = maze[next as usize];
        assert!(pipe!='.');
        let pd = pipe_dirs[&pipe];
        if next + pd.0 == pos {
            pos = next;
            next = next + pd.1;
        } else {
            pos = next;
            next = next + pd.0;
        }
    }

    println!("part1: {}", count / 2 + 1);

    // Guess the 'S' pipe.
    let s_dirs = (start[0] - s_pos, start[1] - s_pos);
    let s_pipe = pipe_dirs.iter().filter(|(_k, &v)| s_dirs == v || s_dirs == (v.1, v.0)).map(|(k, _v)| k).collect::<Vec<_>>()[0];

    let mut inside_count = 0;
    let mut outside = true;
    let mut edge = false;
    let mut edge_from_top = false;
    for (i, pipe) in maze.iter().enumerate() {
        let idx = i as i32;
        if idx % w == 0 {
            outside = true;
        }
        if big_loop.contains(&idx) {
            let mut p = *pipe;
            if p == 'S' {
                p = *s_pipe;
            }
            match p {
                '|' => outside = !outside,
                '-' => assert!(edge),
                'L' => {
                    assert!(!edge);
                    edge = true;
                    edge_from_top = true;
                }
                'J' => {
                    assert!(edge);
                    edge = false;
                    if !edge_from_top {
                        outside = !outside;
                    }
                }
                '7' => {
                    assert!(edge);
                    edge = false;
                    if edge_from_top {
                        outside = !outside;
                    }
                }
                'F' => {
                    assert!(!edge);
                    edge = true;
                    edge_from_top = false;
                }
                '.' => {},
                _ => panic!("what?")
            }
        } else {
            if !edge && !outside {
                inside_count += 1
            }
        }
    }

    println!("part2: {}", inside_count);
}

