# sed didn't fit the second part that well, but what was started in sed has to be finished in sed :)
cat input.txt | sed -E 's/one/o1e/g; s/two/t2o/g; s/three/t3e/g; s/four/f4r/g; s/five/f5e/g; s/six/s6x/g; s/seven/s7n/g; s/eight/e8t/g; s/nine/n9e/g; s/[^0-9]//g; s/^(.)$/\1\1/; s/^(.).*(.)$/\1\2/g' | paste -sd+ - | bc -l 
