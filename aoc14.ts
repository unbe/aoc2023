let fs = require("fs");
let map = fs.readFileSync(0).toString().split('\n').slice(0, -1).map((x: string) => [...x]);
console.log(map);

let count = 0;
map[0].forEach(
  (_ : string[], j : number) => {
    let stack = map.length;
    map.forEach(
      (row : string, i : number) => {
        if(row[j] == 'O') {
          count += stack--;
        } else if(row[j] == '#') {
          stack = map.length - i - 1;
        }
      }
    )
  }
)  

console.log('part1:', count);
