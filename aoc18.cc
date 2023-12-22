#include <unordered_map>
#include <iostream>
#include <string>
#include <vector>

#include <absl/strings/numbers.h>
#include <absl/strings/str_split.h>

#include <limits.h>

using point64_t = std::pair<int64_t, int64_t>;
using segment = std::pair<point64_t, point64_t>;
using plan_t = std::vector<std::tuple<std::pair<int64_t, int64_t>, int64_t, std::string>>;

int64_t solve(const plan_t& plan) {
    auto pos = std::make_pair(0, 0);
    std::vector<segment> dug;
    int64_t dug_sum = 0;
    for (const auto& instr : plan) {
        std::pair<int64_t, int64_t> dir;
        int64_t len;
        std::string tail;
        std::tie(dir, len, tail) = instr;
        auto oldpos = pos;
        pos.first += dir.first * len;
        pos.second += dir.second * len;
        dug_sum += len;
        dug.push_back(std::make_pair(oldpos, pos));
    }

     std::vector<segment> verticals;
    std::copy_if(std::begin(dug), std::end(dug), std::back_inserter(verticals),
               [](const segment& s) { return s.first.second == s.second.second; });
    std::sort(std::begin(verticals), std::end(verticals),
               [](segment a, segment b) { return a.first.second < b.first.second; });

    std::set<int64_t> attention_rows;
    for (const auto s : dug) {
        if (s.first.first == s.second.first) {
            attention_rows.insert(s.first.first);
            attention_rows.insert(s.first.first + 1);
        }
    }

    int64_t inside_sum = 0;
    int64_t rep_i = 0;
    int64_t rep_d = 0;
    for (auto i : attention_rows) {
        bool inside = false;
        bool edge = false;
        bool e_below;
        int64_t inside_since;
        inside_sum += rep_d * (i - rep_i);
        rep_d = 0;
        for (segment seg : verticals) {
            if ((seg.first.first < i && seg.second.first < i) || (seg.first.first > i && seg.second.first > i)) {
                continue;
            }
            if (!inside || edge) {
                inside_since = seg.first.second + 1;
            } else if(!edge) {
                auto d = seg.first.second - inside_since;
                rep_d += d;
                rep_i = i + 1;
                inside_sum += d;
            }
            bool below;
            if (i == std::min(seg.first.first, seg.second.first)) {
                below = true;
            } else if (i == std::max(seg.first.first, seg.second.first)) {
                below = false; 
            } else {
                assert(!edge);
                inside = !inside;
                continue;
            }    
            if (edge) {
                if (below != e_below) {
                    inside = !inside;
                }
            } else {
                e_below = below;
            }
            edge = !edge; 
        }
        assert(!inside);
    }
    return inside_sum + dug_sum;
}

int main() {
    std::vector<std::tuple<std::pair<int64_t, int64_t>, int64_t, std::string>> plan;
    std::unordered_map<char, std::pair<int64_t, int64_t>> dirs = {
            {'R', {0, 1}},
            {'L', {0, -1}},
            {'U', {-1, 0}},
            {'D', {1, 0}},
    };
    for (std::string line; std::getline(std::cin, line);) {
        std::vector<std::string> line_parts = absl::StrSplit(line, " ");
        int64_t len;
        assert(absl::SimpleAtoi(line_parts[1], &len));
        auto instr = std::make_tuple(dirs[line_parts[0].at(0)], len, line_parts[2]);
        plan.push_back(instr);
    }

    int64_t r = solve(plan);
    std::cout << "part1: " << r << std::endl;

    std::unordered_map<char, std::pair<int64_t, int64_t>> dirs2 = {
            {'0', {0, 1}},
            {'1', {1, 0}},
            {'2', {0, -1}},
            {'3', {-1, 0}},
    };
    std::vector<std::tuple<std::pair<int64_t, int64_t>, int64_t, std::string>> plan2;
    for(const auto& old_instr : plan) {
        auto real_str = std::get<2>(old_instr);
        int64_t len;
        assert(absl::SimpleHexAtoi(real_str.substr(2, 5), &len));
        auto instr = std::make_tuple(dirs2[real_str.at(7)], len, "");
        plan2.push_back(instr);
    }
    r = solve(plan2);
    std::cout << "part2: " << r << std::endl;
    return 0;
}
