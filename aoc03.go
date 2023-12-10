package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	parts := make([]int, 0)
	parts = append(parts, -1)
	partmap := make([][]int, 0)
	syms := make([][]int, 0)
	numsRe := regexp.MustCompile(`\d+`)
	symsRe := regexp.MustCompile(`[^\d.]`)
	lineId := 0
	for scanner.Scan() {
		line := scanner.Text()
		mapLine := make([]int, 0)
		for _, match := range numsRe.FindAllStringIndex(line, -1) {
			pn, err := strconv.Atoi(line[match[0]:match[1]])
			if err != nil {
				log.Fatal(err)
			}
			mapEntry := make([]int, match[1]-match[0])
			for i := range mapEntry {
				mapEntry[i] = len(parts)
			}
			mapFiller := make([]int, match[0]-len(mapLine))

			parts = append(parts, pn)
			mapLine = append(mapLine, mapFiller...)
			mapLine = append(mapLine, mapEntry...)
		}

		mapFiller := make([]int, len(line)-len(mapLine))
		mapLine = append(mapLine, mapFiller...)
		partmap = append(partmap, mapLine)

		for _, match := range symsRe.FindAllStringIndex(line, -1) {
			syms = append(syms, []int{lineId, match[0], int(line[match[0]])})
		}

		lineId += 1
	}
	totalGearPower := 0
	sumPartNumbers := 0
	for _, sym := range syms {
		nextTo := make(map[int]int)
		for _, shift0 := range []int{-1, 0, 1} {
			for _, shift1 := range []int{-1, 0, 1} {
				if shift0 == 0 && shift1 == 0 {
					continue
				}
				i0 := sym[0] + shift0
				i1 := sym[1] + shift1
				if i0 < 0 || i1 < 0 || i0 >= len(partmap) || i1 >= len(partmap[i0]) {
					continue
				}
				pi := partmap[i0][i1]
				if pi > 0 {
					nextTo[pi] = parts[pi]
				}
			}
		}
		gearPower := 0
		if len(nextTo) == 2 && sym[2] == '*' {
			gearPower = 1
		}
		for _, v := range nextTo {
			gearPower *= v
			sumPartNumbers += v
		}
		totalGearPower += gearPower
	}
	fmt.Printf("part1: %d\n", sumPartNumbers)
	fmt.Printf("part2: %d\n", totalGearPower)
}
