let fs = require("fs");
let rock_map : string[][] = fs.readFileSync(0).toString().split('\n').slice(0, -1).map((x: string) => [...x]);

let rotate = function(m: string[][]): string[][] {
  return m[0].map((_, i) => m.map(r => r[i]).reverse())
}
let count = function(m: string[][]) : number {
  let count = 0;
  m.forEach((row : string[], i : number) => { 
    row.forEach( (ch : string, j : number) => {
      if(ch == 'O') {
        count += m.length - i
      }
    });
  });  
  return count;
}

let move = function(m: string[][]) {
  m[0].forEach((_ : string, j : number) => {
    let stack = 0;
    m.forEach((row : string[], i : number) => {
      if(row[j] == 'O') {
        if (i != stack) {
          m[stack][j] = row[j];
          row[j] = '.'; 
        }
        stack++;
      } else if(row[j] == '#') {
        stack = i + 1;
      }
    });
  });  
}

move(rock_map);
let cnt = count(rock_map);
console.log('part1:', cnt);

let cycle = function(map: string[][]) : [number, string[][]] {
  let mm = map;
  for (let i = 0; i < 4; i++) {
    move(mm);
    mm = rotate(mm);
  }
  return [count(mm), mm]
}

let seen = new Map();
let cycles = 1000000000;
for (let i = 0; i < cycles; i++) {
  const key = JSON.stringify(rock_map);
  if (seen.has(key)) {
    let jump = i - seen.get(key);
    let remaining = cycles - i;
    const reps = Math.floor(remaining / jump);
    i += jump * reps;
  } else {
    seen.set(key, i);
  }
  [cnt, rock_map]  = cycle(rock_map);
}
console.log('part2:', cnt);
