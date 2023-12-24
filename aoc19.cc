#include <iostream>
#include <string>

#include <absl/strings/str_split.h>
#include <absl/strings/numbers.h>

int main() {
    typedef struct {
        char cat;
        int min;
        int max;
        std::string dest;
    } rule_t;
    
    std::unordered_map<std::string, std::vector<rule_t>> wf_rules;
    std::unordered_map<std::string, std::vector<std::pair<std::string, int>>> backrefs;
    for (std::string line; std::getline(std::cin, line);) {
        if(line.size() == 0) {
            break;
        }
        std::vector<std::string> line_parts = absl::StrSplit(line, "{");
        auto wf_name = line_parts[0];
        std::vector<std::string> rule_str = absl::StrSplit(line_parts[1], absl::ByAnyChar("{,}"), absl::SkipEmpty());
        std::vector<rule_t> rules;
        for (const auto& str : rule_str) {
            rule_t rule = {'x', INT_MIN, INT_MAX, "FAIL"};
            std::vector<std::string> parts = absl::StrSplit(str, ":");
            if (parts.size() == 1) {
                rule.dest = str;
            } else {
                rule.cat = str[0]; 
                int val;
                assert(absl::SimpleAtoi(parts[0].substr(2), &val));
                if(str[1] == '>') {
                    rule.min = val;
                } else {
                    rule.max = val;
                }
                rule.dest = parts[1];
            }
            auto this_rule_idx = std::make_pair(wf_name, rules.size());
            backrefs[rule.dest].push_back(this_rule_idx);
            rules.push_back(rule);
        }
        wf_rules[wf_name] = rules;
    } 

    int total = 0;
    for (std::string line; std::getline(std::cin, line);) {
        std::vector<std::string> rating_str = absl::StrSplit(line, absl::ByAnyChar("{,}"), absl::SkipEmpty());
        std::map<char,int> rating;
        int r_sum = 0;
        for(const auto& str : rating_str) {
            std::vector<std::string> parts = absl::StrSplit(str, "=");
            int val;
            assert(absl::SimpleAtoi(parts[1], &val));
            rating[parts[0].at(0)] = val;
            r_sum += val;
        }

        std::string wf_name = "in";
        while (wf_name != "A" && wf_name != "R") {
            const auto& rules = wf_rules[wf_name];
            wf_name = std::find_if(rules.begin(), rules.end(), [&rating] (const auto& rule) {
                    return rating[rule.cat] < rule.max && rating[rule.cat] > rule.min;
                })->dest;
        }
        if (wf_name == "A") {
            total += r_sum;
        }
    }
    std::cout << "part1: " << total << std::endl;
    
    typedef struct {
        std::string wf_name;
        std::unordered_map<char, std::pair<int, int>> ranges;
    } pos_t;

    std::vector<pos_t> pos_q = { 
            { "A", {
                {'x', {0, 4001}},
                {'m', {0, 4001}},
                {'a', {0, 4001}},
                {'s', {0, 4001}},
            }}
     };

    int64_t total_combs = 0;
    while(pos_q.size() > 0) {
        const pos_t pos = pos_q.back();
        pos_q.pop_back();
        for(const auto& br : backrefs[pos.wf_name]) {
            pos_t new_pos = pos;
            const auto& rule = wf_rules[br.first][br.second];
            auto* range = &new_pos.ranges[rule.cat];
            range->first = std::max(range->first, rule.min);
            range->second = std::min(range->second, rule.max);
            for (int i = br.second - 1; i >= 0; i--) {
                const auto& rule = wf_rules[br.first][i];
                auto* range = &new_pos.ranges[rule.cat];
                if (rule.max != INT_MAX) {
                    range->first = std::max(range->first, rule.max - 1);
                }
                if (rule.min != INT_MIN) {
                    range->second = std::min(range->second, rule.min + 1);
                }
            }
            new_pos.wf_name = br.first;
            if (new_pos.wf_name == "in") {
                int64_t combs = 1;
                for (const auto& kv : new_pos.ranges) {
                    combs *= int64_t(kv.second.second - kv.second.first - 1);
                    if (combs <= 0) {
                        break;
                    }
                }
                if (combs > 0) {
                    total_combs += combs;
                }
            } else {
                pos_q.push_back(new_pos);
            }
        }
    }
    std::cout << "part2: " << total_combs << std::endl;
};
