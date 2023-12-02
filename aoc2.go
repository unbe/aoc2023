package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func parseReq(reqString string) map[string]int {
	req := make(map[string]int)
	reqItems := strings.Split(reqString, ", ")
	for _, itemString := range reqItems {
		parts := strings.Split(itemString, " ")
		cnt, _ := strconv.Atoi(parts[0])
		req[parts[1]] = cnt
	}
	return req
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	gameId := 1
	gameSum := 0
	powerSum := 0
	for scanner.Scan() {
		line := scanner.Text()
		gameLine := strings.Split(line, ": ")[1]
		gameOk := true
		maxReqs := make(map[string]int)
		for _, reqString := range strings.Split(gameLine, "; ") {
			req := parseReq(reqString)
			if req["red"] > 12 || req["green"] > 13 || req["blue"] > 14 {
				gameOk = false
			}
			for color, count := range req {
				maxReqs[color] = max(maxReqs[color], count)
			}
		}
		if gameOk {
			gameSum += gameId
		}
		power := 1
		for _, count := range maxReqs {
			power *= count
		}
		powerSum += power
		gameId += 1
	}
	fmt.Printf("part one: %d\n", gameSum)
	fmt.Printf("part two: %d\n", powerSum)
}
