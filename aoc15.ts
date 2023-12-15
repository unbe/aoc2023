let fs = require("fs");
let steps : string[] = fs.readFileSync(0).toString().trim().split(',');


const hash = function(s: string) : number {
  let sum = 0;
  for(let i = 0; i < s.length; i++) {
    sum += s.charCodeAt(i);
    sum = (sum * 17) % 256;
  }
  console.log(s, sum);
  return sum;
}

let total = 0;
steps.forEach((step) => { total += hash(step); });
console.log(total);
