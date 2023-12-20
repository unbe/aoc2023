#include <unordered_map>
#include <iostream>
#include <string>
#include <vector>

#include <absl/strings/numbers.h>
#include <absl/strings/str_split.h>

#include <limits.h>

int main() {
	std::vector<std::tuple<char, int, std::string>> plan;
    for (std::string line; std::getline(std::cin, line);) {
    	std::vector<std::string> line_parts = absl::StrSplit(line, " ");
		int len;
		assert(absl::SimpleAtoi(line_parts[1], &len));
		auto instr = std::make_tuple(line_parts[0].at(0), len, line_parts[2]);
		plan.push_back(instr);
    }

	std::unordered_map<char, std::pair<int, int>> dirs = {
			{'R', {0, 1}},
			{'L', {0, -1}},
			{'U', {-1, 0}},
			{'D', {1, 0}},
	};

	auto pos = std::make_pair(0, 0);
	auto min = std::make_pair(INT_MAX, INT_MAX);
	auto max = std::make_pair(INT_MIN, INT_MIN);
	std::set<std::pair<int, int>> dug;
	std::set<std::pair<int, int>> fill;
	for (const auto& instr : plan) {
		char dir;
		int len;
		std::string tail;
		std::tie(dir, len, tail) = instr;
		auto mov = dirs[dir];
		for (int i = 0; i<len; i++) {
			pos.first += mov.first;
			pos.second += mov.second;
			dug.insert(pos);
			min.first = std::min(min.first, pos.first);
			min.second = std::min(min.second, pos.second);
			max.first = std::max(max.first, pos.first);
			max.second = std::max(max.second, pos.second);
		}
	}
	for (int i = min.first; i <= max.first; i++) {
		bool inside = false;
		bool edge = false;
		bool e_above, e_below;
		for (int j = min.second; j <= max.second; j++) {
			auto point = std::make_pair(i, j);
			bool d = dug.count(point) > 0;
			if (d) {
				auto above = dug.count(std::make_pair(i-1, j)) > 0;
				auto below = dug.count(std::make_pair(i+1, j)) > 0;
				if (!edge) {
					if (above && below) {
						inside = !inside;
						continue;
					}
					assert(above || below);
					edge = true;
					e_above = above;
					e_below = below;
				} else {
					if (above || below) {
						edge = false;
					}
					if (above && !e_above || below && !e_below) {
						inside = !inside;
					}
				}
			} else {
				if (inside) {
					fill.insert(point);
				}
			}
		}
	}
	for (int i = min.first; i <= max.first; i++) {
		for (int j = min.second; j <= max.second; j++) {
			auto point = std::make_pair(i, j);
			if (dug.count(point) > 0) {
				std::cout << "#";
			} else if (fill.count(point) > 0) {
				std::cout << "*";
			} else {
				std::cout << ".";
			}
		}
		std::cout << std::endl;
	}
	std::cout << int(dug.size() + fill.size()) << std::endl;
    return 0;
}
