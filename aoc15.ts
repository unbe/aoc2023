let fs = require("fs");
let steps : string[] = fs.readFileSync(0).toString().trim().split(',');

const hash = function(s: string) : number {
  let sum = 0;
  for(let i = 0; i < s.length; i++) {
    sum += s.charCodeAt(i);
    sum = (sum * 17) % 256;
  }
  return sum;
}

let total = 0;
steps.forEach((step) => { total += hash(step); });
console.log('part1:', total);

let boxes : [string, number][][] = new Array(256).fill(null).map(() => []);

steps.forEach((step) => {
  let match = step.match(/(.*)([=-])(\d+)?/);
  let label = match![1];
  let op = match![2];
  let boxid = hash(label);
  let box = boxes[boxid];
  if(op == '-') {
    boxes[boxid] = box.filter((lens) => lens[0] != label);
  }
  if(op == '=') {
    let foclen : number = +match![3];
    let existing : [string, number] | undefined;
    box.forEach((lens) => {
      if(lens[0] == label) {
        existing = lens;
      }
    });
    if (existing != undefined) {
      existing[1] = foclen;
    } else {
      box.push([label, foclen]);
    }
  }
});

total = 0;
boxes.forEach((box, boxid) => {
  box.forEach((lens, lensid) => {
    total += (1 + boxid) * (1 + lensid) * lens[1];
  });
});
console.log('part2:', total);
